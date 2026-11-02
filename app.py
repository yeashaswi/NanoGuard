"""
NanoGuard AI: Industrial Nanoparticle Pollutant Detection & Telemetry Platform
A minimalistic, high-performance platform for detecting factory nanoparticle emissions
via multi-channel chemical and optical reaction signatures.
"""

import os
import json
import numpy as np
import pandas as pd
import streamlit as st
import plotly.graph_objects as go
import plotly.express as px

from models.inference import NanoGuardInferenceEngine, HAZARD_STANDARDS
from data.dataset_generator import (
    generate_sensor_time_series,
    POLLUTANT_PROFILES,
    SENSOR_NAMES
)

# ==========================================
# 1. PAGE SETUP & MINIMALIST THEMING
# ==========================================
st.set_page_config(
    page_title="NanoGuard AI | Nanoparticle Pollutant Detection",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Minimalist CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    
    /* Clean Cards */
    .metric-card {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 12px;
        padding: 18px 22px;
        margin-bottom: 15px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.04);
    }
    
    .status-pill {
        display: inline-block;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.78rem;
        font-weight: 600;
        letter-spacing: 0.03em;
        text-transform: uppercase;
    }
    
    .pill-safe { background: rgba(34, 197, 94, 0.15); color: #22c55e; border: 1px solid rgba(34, 197, 94, 0.3); }
    .pill-moderate { background: rgba(234, 179, 8, 0.15); color: #eab308; border: 1px solid rgba(234, 179, 8, 0.3); }
    .pill-hazardous { background: rgba(249, 115, 22, 0.15); color: #f97316; border: 1px solid rgba(249, 115, 22, 0.3); }
    .pill-critical { background: rgba(239, 68, 68, 0.15); color: #ef4444; border: 1px solid rgba(239, 68, 68, 0.3); }
    
    /* Remove unnecessary spacing */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 2. CACHED ENGINE LOADER
# ==========================================
@st.cache_resource
def get_engine():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    models_dir = os.path.join(base_dir, "models")
    return NanoGuardInferenceEngine(models_dir)

engine = get_engine()

# ==========================================
# 3. SIDEBAR NAVIGATION & INDUSTRIAL SCENARIOS
# ==========================================
with st.sidebar:
    st.markdown("### 🛡️ **NanoGuard AI**")
    st.caption("Industrial Nanoparticle Reaction Telemetry")
    st.markdown("---")
    
    app_mode = st.radio(
        "Navigation",
        [
            "⚡ Live Reaction Detector",
            "📁 Batch Sensor Audit",
            "🧠 Model Diagnostics & ROC",
            "🔬 Brownian Motion Optical Lab"
        ],
        index=0
    )
    
    st.markdown("---")
    st.caption("🌿 **Sensing Mechanism:** Multi-channel chemoresistive catalytic adsorption & Localized Surface Plasmon Resonance (LSPR) kinetics.")

# ==========================================
# 4. VIEW: LIVE REACTION DETECTOR
# ==========================================
if app_mode == "⚡ Live Reaction Detector":
    st.markdown("## ⚡ Nanoparticle Reaction Signal Detector")
    st.caption("Observe real-time sensor reaction kinetics, detect pollutant identity, and assess factory emission compliance.")
    
    # Factory Preset Scenarios
    col_preset, col_slider1, col_slider2 = st.columns([1.2, 1, 1])
    
    PRESETS = {
        "🏭 Titanium Dioxide Surge (Pigment Plant)": {
            "pollutant": "TiO2", "conc": 145.0, "temp": 42.0, "hum": 48.0, "flow": 2.8
        },
        "🚗 Zinc Oxide Aerosol (Rubber/Vulcanization)": {
            "pollutant": "ZnO", "conc": 110.0, "temp": 38.0, "hum": 55.0, "flow": 2.2
        },
        "🔥 Copper Oxide Toxic Spike (Foundry/Smelter)": {
            "pollutant": "CuO", "conc": 85.0, "temp": 68.0, "hum": 32.0, "flow": 3.4
        },
        "🧪 Nano-Silver Release (Electronics Fab)": {
            "pollutant": "Ag-NP", "conc": 48.0, "temp": 24.0, "hum": 40.0, "flow": 1.5
        },
        "🏭 Carbon Soot Emission (Furnace Kiln)": {
            "pollutant": "Carbon_Soot", "conc": 130.0, "temp": 75.0, "hum": 25.0, "flow": 4.1
        },
        "🧱 Silica Particulate Breach (Ceramics/Foundry)": {
            "pollutant": "SiO2", "conc": 105.0, "temp": 30.0, "hum": 60.0, "flow": 2.0
        },
        "🍃 Nominal Scrubbed Exhaust (Ambient Baseline)": {
            "pollutant": "Clean_Air", "conc": 1.8, "temp": 25.0, "hum": 50.0, "flow": 1.8
        }
    }
    
    with col_preset:
        preset_choice = st.selectbox(
            "Select Factory Emission Scenario",
            list(PRESETS.keys()),
            index=0
        )
        selected_preset = PRESETS[preset_choice]
        
    with col_slider1:
        sim_conc = st.slider(
            "Particle Load (μg/m³)",
            min_value=0.5,
            max_value=350.0,
            value=float(selected_preset["conc"]),
            step=1.0
        )
        sim_temp = st.slider(
            "Exhaust Temp (°C)",
            min_value=15.0,
            max_value=90.0,
            value=float(selected_preset["temp"]),
            step=1.0
        )

    with col_slider2:
        sim_hum = st.slider(
            "Relative Humidity (%)",
            min_value=15.0,
            max_value=90.0,
            value=float(selected_preset["hum"]),
            step=1.0
        )
        sim_flow = st.slider(
            "Duct Flow Speed (m/s)",
            min_value=0.5,
            max_value=6.0,
            value=float(selected_preset["flow"]),
            step=0.1
        )
        
    # Generate Reaction Dynamics
    target_pollutant = selected_preset["pollutant"]
    t, curves = generate_sensor_time_series(
        pollutant=target_pollutant,
        concentration_ug_m3=sim_conc,
        temp_c=sim_temp,
        humidity_pct=sim_hum,
        total_duration_s=80.0,
        dt=0.5
    )
    
    # Calculate steady-state features for ML inference
    profile = POLLUTANT_PROFILES[target_pollutant]
    sensor_features = {}
    for s_name in SENSOR_NAMES:
        # Measure peak relative shift during exposure
        peak_val = float(np.max(curves[s_name]) - 1.0)
        sensor_features[s_name] = max(0.01, round(peak_val, 4))
        
    peak_amp = float(max(sensor_features.values()))
    tau_resp = float(np.random.uniform(*profile["resp_time_range"]))
    tau_rec = float(np.random.uniform(*profile["rec_time_range"]))
    reaction_slope = round(peak_amp / max(tau_resp, 1.0), 4)
    
    if target_pollutant == "Clean_Air":
        lspr_shift = 0.05
    else:
        lspr_shift = round(float(profile["lspr_factor"] * sim_conc), 3)
        
    input_features = {
        "temp_c": sim_temp,
        "humidity_pct": sim_hum,
        "flow_velocity_ms": sim_flow,
        **sensor_features,
        "peak_reaction_amplitude": peak_amp,
        "response_time_s": tau_resp,
        "recovery_time_s": tau_rec,
        "reaction_slope": reaction_slope,
        "lspr_shift_nm": lspr_shift
    }
    
    # Run ML Inference
    inference_result = engine.predict_single(input_features)
    pred_pollutant = inference_result["pollutant"]
    confidence = inference_result["confidence"]
    pred_conc = inference_result["predicted_concentration_ug_m3"]
    hazard_level = inference_result["hazard_level"]
    badge_color = inference_result["badge_color"]
    status_text = inference_result["status_text"]
    mitigation_plan = inference_result["mitigation_plan"]
    
    st.markdown("---")
    
    # Top Metrics Row
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.markdown(f"""
        <div class="metric-card">
            <span style="font-size:0.8rem; color:#94a3b8; text-transform:uppercase;">Detected Pollutant</span>
            <h3 style="margin:4px 0 0 0; font-size:1.4rem; color:#f8fafc;">{POLLUTANT_PROFILES[pred_pollutant]['name']}</h3>
            <span style="font-size:0.85rem; color:#38bdf8;">Confidence: {confidence * 100:.1f}%</span>
        </div>
        """, unsafe_allow_html=True)
        
    with m2:
        st.markdown(f"""
        <div class="metric-card">
            <span style="font-size:0.8rem; color:#94a3b8; text-transform:uppercase;">Estimated Concentration</span>
            <h3 style="margin:4px 0 0 0; font-size:1.4rem; color:#f8fafc;">{pred_conc:.1f} <span style="font-size:0.9rem; color:#94a3b8;">μg/m³</span></h3>
            <span style="font-size:0.85rem; color:#94a3b8;">CPCB Limit: {inference_result['cpcb_limit']} μg/m³</span>
        </div>
        """, unsafe_allow_html=True)
        
    with m3:
        pill_class = f"pill-{hazard_level.lower()}"
        st.markdown(f"""
        <div class="metric-card">
            <span style="font-size:0.8rem; color:#94a3b8; text-transform:uppercase;">Regulatory Compliance</span>
            <div style="margin-top:6px;">
                <span class="status-pill {pill_class}">{hazard_level}</span>
            </div>
            <span style="font-size:0.82rem; color:#94a3b8; display:block; margin-top:6px;">{status_text}</span>
        </div>
        """, unsafe_allow_html=True)
        
    with m4:
        st.markdown(f"""
        <div class="metric-card">
            <span style="font-size:0.8rem; color:#94a3b8; text-transform:uppercase;">LSPR Optical Peak Shift</span>
            <h3 style="margin:4px 0 0 0; font-size:1.4rem; color:#f8fafc;">Δλ {lspr_shift:.2f} <span style="font-size:0.9rem; color:#94a3b8;">nm</span></h3>
            <span style="font-size:0.85rem; color:#94a3b8;">Peak ΔR/R₀: +{peak_amp*100:.1f}%</span>
        </div>
        """, unsafe_allow_html=True)
        
    # Prescriptive Action Banner
    if hazard_level in ["HAZARDOUS", "CRITICAL"]:
        st.error(f"🚨 **Industrial Hazard Protocol Activated:** {mitigation_plan}")
    elif hazard_level == "MODERATE":
        st.warning(f"⚠️ **Precautionary Advisory:** {mitigation_plan}")
    else:
        st.success(f"✅ **Compliance Cleared:** {mitigation_plan}")

    # Visualizations: Real-Time Signal Reaction Curves + Array Radar
    col_plot1, col_plot2 = st.columns([1.6, 1])
    
    with col_plot1:
        st.markdown("#### 📈 Multi-Sensor Reaction Kinetics: $R(t) / R_0$")
        fig_kinetics = go.Figure()
        
        sensor_display_map = {
            "s1_sno2": "SnO₂ Film",
            "s2_wo3": "WO₃ Plates",
            "s3_graphene": "rGO Nanoflakes",
            "s4_au_nano": "Au Plasmonic",
            "s5_cnt": "CNT Bundles",
            "s6_in2o3": "In₂O₃ Spheres",
            "s7_tio2_pt": "Pt-TiO₂ Catalytic",
            "s8_zno_nw": "ZnO Nanowires"
        }
        
        colors = ["#38bdf8", "#818cf8", "#a855f7", "#ec4899", "#f43f5e", "#f97316", "#eab308", "#10b981"]
        for idx, (col_key, label) in enumerate(sensor_display_map.items()):
            fig_kinetics.add_trace(go.Scatter(
                x=t,
                y=curves[col_key],
                mode='lines',
                name=label,
                line=dict(color=colors[idx % len(colors)], width=2.0)
            ))
            
        fig_kinetics.add_vrect(x0=10, x1=60, fillcolor="rgba(56, 189, 248, 0.08)", line_width=0, annotation_text="Adsorption / Reaction Exposure Phase", annotation_position="top left")
        fig_kinetics.update_layout(
            height=360,
            margin=dict(l=20, r=20, t=30, b=20),
            xaxis_title="Time Elapsed (seconds)",
            yaxis_title="Relative Resistance (R/R₀)",
            template="plotly_dark",
            legend=dict(orientation="h", yanchor="bottom", y=-0.35, xanchor="center", x=0.5),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)'
        )
        st.plotly_chart(fig_kinetics, use_container_width=True)
        
    with col_plot2:
        st.markdown("#### 🎯 Pollutant Probability Profile")
        prob_df = pd.DataFrame({
            "Pollutant": [POLLUTANT_PROFILES[k]["name"] for k in inference_result["probabilities"].keys()],
            "Probability": [v * 100 for v in inference_result["probabilities"].values()]
        }).sort_values(by="Probability", ascending=True)
        
        fig_bar = px.bar(
            prob_df,
            x="Probability",
            y="Pollutant",
            orientation="h",
            color="Probability",
            color_continuous_scale="Blues",
            text_auto=".1f"
        )
        fig_bar.update_layout(
            height=360,
            margin=dict(l=10, r=20, t=30, b=20),
            xaxis_title="Confidence (%)",
            yaxis_title="",
            template="plotly_dark",
            coloraxis_showscale=False,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)'
        )
        st.plotly_chart(fig_bar, use_container_width=True)

# ==========================================
# 5. VIEW: BATCH SENSOR AUDIT
# ==========================================
elif app_mode == "📁 Batch Sensor Audit":
    st.markdown("## 📁 Batch Industrial Sensor Audit")
    st.caption("Upload historical factory sensor logs or run automated evaluation over testing batches.")
    
    tab_sample, tab_upload = st.tabs(["🧪 Benchmark Validation Set", "📤 Upload Custom Factory CSV"])
    
    with tab_sample:
        data_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "nanoparticle_reaction_dataset.csv")
        if os.path.exists(data_path):
            df_full = pd.read_csv(data_path)
            num_rows = st.slider("Select Audit Batch Size", min_value=10, max_value=200, value=30, step=10)
            sample_df = df_full.sample(n=num_rows, random_state=42).copy()
            
            with st.spinner("Running batch machine learning inference..."):
                results_df = engine.predict_dataframe(sample_df)
                
            col_b1, col_b2, col_b3 = st.columns(3)
            acc = (results_df["pollutant_type"] == results_df["pred_pollutant"]).mean() * 100
            mae = np.mean(np.abs(results_df["concentration_ug_m3"] - results_df["pred_concentration_ug_m3"]))
            crit_count = (results_df["pred_hazard_level"] == "CRITICAL").sum()
            
            col_b1.metric("Batch Classification Accuracy", f"{acc:.1f}%")
            col_b2.metric("Mean Absolute Concentration Error", f"{mae:.2f} μg/m³")
            col_b3.metric("Critical Hazards Flagged", f"{crit_count} events")
            
            # Display Table
            display_cols = [
                "sample_id", "factory_source", "pollutant_type", "pred_pollutant",
                "pred_confidence", "concentration_ug_m3", "pred_concentration_ug_m3",
                "pred_hazard_level"
            ]
            st.dataframe(results_df[display_cols], use_container_width=True)
            
            # Download predicted batch
            csv = results_df.to_csv(index=False).encode('utf-8')
            st.download_button(
                "📥 Download Annotated Telemetry CSV",
                data=csv,
                file_name="nanoguard_audited_emissions.csv",
                mime="text/csv"
            )

    with tab_upload:
        uploaded_file = st.file_uploader("Upload Factory Multi-Sensor Telemetry CSV", type=["csv"])
        if uploaded_file is not None:
            user_df = pd.read_csv(uploaded_file)
            st.success(f"Loaded {len(user_df)} sensor records from file.")
            try:
                evaluated_df = engine.predict_dataframe(user_df)
                st.dataframe(evaluated_df, use_container_width=True)
            except Exception as e:
                st.error(f"Error parsing uploaded telemetry: {str(e)}")

# ==========================================
# 6. VIEW: MODEL DIAGNOSTICS & METRICS
# ==========================================
elif app_mode == "🧠 Model Diagnostics & ROC":
    st.markdown("## 🧠 Machine Learning Diagnostics & Validation")
    st.caption("Inspect training performance, 5-fold cross-validation, confusion matrix, and sensor feature importance.")
    
    metrics = engine.metrics
    clf_metrics = metrics["classifier"]
    reg_metrics = metrics["regressor"]
    
    d1, d2, d3, d4 = st.columns(4)
    d1.metric("Classifier Accuracy", f"{clf_metrics['accuracy'] * 100:.2f}%")
    d2.metric("5-Fold CV Accuracy", f"{clf_metrics['cv_accuracy_mean'] * 100:.2f}%")
    d3.metric("Regressor R² Score", f"{reg_metrics['r2_score']:.4f}")
    d4.metric("Regressor RMSE", f"{reg_metrics['rmse']:.2f} μg/m³")
    
    st.markdown("---")
    
    col_conf, col_fi = st.columns([1, 1.2])
    
    with col_conf:
        st.markdown("#### 🎯 Confusion Matrix (Test Set: 600 Samples)")
        cm = np.array(clf_metrics["confusion_matrix"])
        classes = clf_metrics["classes"]
        
        fig_cm = px.imshow(
            cm,
            labels=dict(x="Predicted Class", y="Ground Truth", color="Count"),
            x=classes,
            y=classes,
            color_continuous_scale="Blues",
            text_auto=True
        )
        fig_cm.update_layout(
            height=420,
            margin=dict(l=20, r=20, t=30, b=20),
            template="plotly_dark",
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)'
        )
        st.plotly_chart(fig_cm, use_container_width=True)
        
    with col_fi:
        st.markdown("#### 📊 Sensor Array Feature Importance")
        fi_dict = engine.metadata["feature_importances"]
        fi_df = pd.DataFrame(list(fi_dict.items()), columns=["Feature", "Importance"]).head(10)
        fi_df = fi_df.sort_values(by="Importance", ascending=True)
        
        fig_fi = px.bar(
            fi_df,
            x="Importance",
            y="Feature",
            orientation="h",
            color="Importance",
            color_continuous_scale="Teal",
            text_auto=".3f"
        )
        fig_fi.update_layout(
            height=420,
            margin=dict(l=20, r=20, t=30, b=20),
            template="plotly_dark",
            coloraxis_showscale=False,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)'
        )
        st.plotly_chart(fig_fi, use_container_width=True)

# ==========================================
# 7. VIEW: BROWNIAN MOTION OPTICAL LAB
# ==========================================
elif app_mode == "🔬 Brownian Motion Optical Lab":
    st.markdown("## 🔬 Stokes-Einstein Brownian Tracking Lab")
    st.caption("Supplementary physical microscopy module: Simulates Brownian motion of nanoparticles and tracks hydrodynamic diameter via Stokes-Einstein diffusion.")
    
    from scipy.ndimage import maximum_filter
    from scipy.optimize import linear_sum_assignment
    import cv2
    
    K_B = 1.380649e-23
    
    def get_water_viscosity(temp_celsius: float) -> float:
        return 2.414e-5 * (10 ** (247.8 / ((temp_celsius + 273.15) - 140.0)))
        
    c1, c2, c3 = st.columns(3)
    target_mat = c1.selectbox("Nanomaterial", ["Titanium Dioxide (TiO2)", "Zinc Oxide (ZnO)", "Nano-Silver (Ag-NP)"])
    nominal_size = {"Titanium Dioxide (TiO2)": 50.0, "Zinc Oxide (ZnO)": 65.0, "Nano-Silver (Ag-NP)": 35.0}[target_mat]
    temp_sim = c2.slider("Fluid Temp (°C)", 15.0, 45.0, 25.0)
    num_particles = c3.slider("Particle Count", 5, 40, 15)
    
    visc = get_water_viscosity(temp_sim)
    
    # Generate 15 frames
    temp_k = temp_sim + 273.15
    radius_m = (nominal_size * 1e-9) / 2.0
    dt = 1.0 / 30.0
    D_m2_s = (K_B * temp_k) / (6 * np.pi * visc * radius_m)
    D_um2_s = D_m2_s * 1e12
    step_std_px = np.sqrt(2 * D_um2_s * dt) / 0.1
    
    img_size = 200
    positions = np.random.uniform(20, img_size - 20, size=(num_particles, 2))
    grid_x, grid_y = np.meshgrid(np.arange(img_size), np.arange(img_size))
    
    frames = []
    for _ in range(25):
        frame = np.full((img_size, img_size), 20.0, dtype=np.float32)
        for px, py in positions:
            dist_sq = (grid_x - px)**2 + (grid_y - py)**2
            frame += 180.0 * np.exp(-dist_sq / (2 * (1.8**2)))
        noisy = np.clip(frame + np.random.normal(0, 10, (img_size, img_size)), 0, 255).astype(np.uint8)
        frames.append(noisy)
        positions = np.clip(positions + np.random.normal(0, step_std_px, size=(num_particles, 2)), 5, img_size - 5)
        
    st.image(frames[-1], caption=f"Microscopy Frame Sample (Brownian Trajectories of {target_mat})", width=380)
    st.info(f"Calculated Stokes-Einstein Diffusion Coefficient: **{D_um2_s:.4f} μm²/s** (Dynamic Viscosity: **{visc*1000:.3f} mPa·s**)")
