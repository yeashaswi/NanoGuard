"""
NanoGuard: Industrial Nanoparticle Pollutant Reaction Dataset Generator
Generates scientifically calibrated multi-sensor reaction time-series and steady-state 
features modeling factory exhaust / effluent detection.
"""

import numpy as np
import pandas as pd
import os
import json

POLLUTANT_PROFILES = {
    "TiO2": {
        "name": "Titanium Dioxide (TiO2)",
        "hazard_threshold_ug_m3": 100.0,
        "critical_threshold_ug_m3": 250.0,
        "base_affinity": [0.85, 0.45, 0.30, 0.25, 0.20, 0.40, 0.95, 0.35], # S1 to S8 sensitivities
        "resp_time_range": (14.0, 24.0),
        "rec_time_range": (35.0, 60.0),
        "lspr_factor": 0.045,
        "activation_energy": 28.5, # kJ/mol
        "common_source": "Pigment_Coating"
    },
    "ZnO": {
        "name": "Zinc Oxide (ZnO)",
        "hazard_threshold_ug_m3": 80.0,
        "critical_threshold_ug_m3": 200.0,
        "base_affinity": [0.40, 0.30, 0.50, 0.35, 0.45, 0.30, 0.35, 0.95],
        "resp_time_range": (8.0, 16.0),
        "rec_time_range": (20.0, 42.0),
        "lspr_factor": 0.060,
        "activation_energy": 22.0,
        "common_source": "Rubber_Synthetics"
    },
    "CuO": {
        "name": "Copper Oxide (CuO)",
        "hazard_threshold_ug_m3": 50.0,
        "critical_threshold_ug_m3": 150.0,
        "base_affinity": [0.90, 0.85, 0.40, 0.40, 0.30, 0.70, 0.40, 0.50],
        "resp_time_range": (10.0, 18.0),
        "rec_time_range": (25.0, 48.0),
        "lspr_factor": 0.075,
        "activation_energy": 25.0,
        "common_source": "Foundry_Smelter"
    },
    "Ag-NP": {
        "name": "Nano-Silver (Ag-NP)",
        "hazard_threshold_ug_m3": 25.0,
        "critical_threshold_ug_m3": 75.0,
        "base_affinity": [0.50, 0.40, 0.90, 0.98, 0.60, 0.45, 0.55, 0.40],
        "resp_time_range": (6.0, 14.0),
        "rec_time_range": (45.0, 80.0),
        "lspr_factor": 0.160, # Strong localized surface plasmon resonance
        "activation_energy": 18.0,
        "common_source": "Electronics_Fab"
    },
    "Carbon_Soot": {
        "name": "Carbon Nanoparticles / Soot",
        "hazard_threshold_ug_m3": 60.0,
        "critical_threshold_ug_m3": 180.0,
        "base_affinity": [0.35, 0.30, 0.80, 0.20, 0.95, 0.85, 0.25, 0.20],
        "resp_time_range": (12.0, 22.0),
        "rec_time_range": (60.0, 110.0), # Slow recovery due to strong chemisorption
        "lspr_factor": 0.020,
        "activation_energy": 32.0,
        "common_source": "Carbon_Furnace"
    },
    "SiO2": {
        "name": "Silica Nanoparticles (SiO2)",
        "hazard_threshold_ug_m3": 90.0,
        "critical_threshold_ug_m3": 220.0,
        "base_affinity": [0.20, 0.25, 0.35, 0.40, 0.30, 0.30, 0.25, 0.30], # Dielectric suppression
        "resp_time_range": (18.0, 30.0),
        "rec_time_range": (22.0, 40.0),
        "lspr_factor": 0.035,
        "activation_energy": 35.0,
        "common_source": "Glass_Ceramics"
    },
    "Clean_Air": {
        "name": "Nominal Filtered Air (Baseline)",
        "hazard_threshold_ug_m3": 10.0,
        "critical_threshold_ug_m3": 20.0,
        "base_affinity": [0.03, 0.03, 0.02, 0.02, 0.02, 0.03, 0.02, 0.02],
        "resp_time_range": (25.0, 40.0),
        "rec_time_range": (10.0, 20.0),
        "lspr_factor": 0.002,
        "activation_energy": 10.0,
        "common_source": "Ambient_Control"
    }
}

SENSOR_NAMES = [
    "s1_sno2",      # SnO2 nanocrystalline thick film
    "s2_wo3",       # WO3 porous nanoplates
    "s3_graphene",  # Functionalized Reduced Graphene Oxide (rGO)
    "s4_au_nano",   # Au Nano-island localized plasmonic resonator
    "s5_cnt",       # Carbon Nanotube bundle chemoresistor
    "s6_in2o3",     # In2O3 mesoporous nanospheres
    "s7_tio2_pt",   # Platinum-doped TiO2 catalytic sensor
    "s8_zno_nw"     # ZnO single-crystal nanowire array
]

def generate_sensor_time_series(pollutant: str, concentration_ug_m3: float, 
                                temp_c: float = 25.0, humidity_pct: float = 50.0, 
                                total_duration_s: float = 120.0, dt: float = 0.5):
    """
    Synthesizes the dynamic temporal reaction curves R(t)/R0 across all 8 sensors
    over exposure and recovery phases.
    """
    profile = POLLUTANT_PROFILES[pollutant]
    t = np.arange(0, total_duration_s, dt)
    n_points = len(t)
    
    # Exposure is applied between t = 10s and t = 60s
    t_start = 10.0
    t_end = 60.0
    
    # Arrhenius temperature correction factor
    R_gas = 8.314e-3 # kJ/(mol*K)
    T_kelvin = temp_c + 273.15
    k_temp = np.exp(-profile["activation_energy"] / (R_gas * T_kelvin)) / np.exp(-profile["activation_energy"] / (R_gas * 298.15))
    
    # Humidity interference
    humidity_factor = 1.0 - (humidity_pct - 50.0) * 0.002
    
    # Response and recovery time constants
    tau_resp = np.random.uniform(*profile["resp_time_range"]) / max(k_temp, 0.4)
    tau_rec = np.random.uniform(*profile["rec_time_range"])
    
    conc_power = 0.82 if pollutant != "Clean_Air" else 1.0
    signal_curves = {}
    
    for i, sensor_col in enumerate(SENSOR_NAMES):
        affinity = profile["base_affinity"][i]
        # Steady-state maximum response amplitude (percentage shift)
        if pollutant == "Clean_Air":
            delta_R_max = np.random.normal(0.02, 0.008)
        else:
            delta_R_max = affinity * (concentration_ug_m3 ** conc_power) * 0.28 * humidity_factor
            
        curve = np.zeros(n_points, dtype=np.float32)
        for idx, time_sec in enumerate(t):
            if time_sec < t_start:
                # Baseline pre-exposure
                curve[idx] = 1.0 + np.random.normal(0, 0.005)
            elif t_start <= time_sec < t_end:
                # Adsorption reaction phase: 1 - exp(-(t-t0)/tau)
                fraction = 1.0 - np.exp(-(time_sec - t_start) / tau_resp)
                curve[idx] = 1.0 + (delta_R_max * fraction) + np.random.normal(0, 0.008)
            else:
                # Desorption recovery phase: delta_R * exp(-(t-t1)/tau)
                peak_val = delta_R_max * (1.0 - np.exp(-(t_end - t_start) / tau_resp))
                fraction_rec = np.exp(-(time_sec - t_end) / tau_rec)
                curve[idx] = 1.0 + (peak_val * fraction_rec) + np.random.normal(0, 0.008)
                
        signal_curves[sensor_col] = curve
        
    return t, signal_curves

def generate_reaction_dataset(num_samples: int = 2500, random_seed: int = 42) -> pd.DataFrame:
    """
    Generates a high-quality tabular dataset of industrial reaction signals,
    capturing multi-sensor profiles, kinetic features, and environmental covariates.
    """
    np.random.seed(random_seed)
    records = []
    
    pollutants = list(POLLUTANT_PROFILES.keys())
    # Sampling distribution: industrial sectors with varying prevalence
    weights = [0.18, 0.16, 0.16, 0.14, 0.16, 0.10, 0.10]
    
    for idx in range(num_samples):
        pollutant = np.random.choice(pollutants, p=weights)
        profile = POLLUTANT_PROFILES[pollutant]
        
        # Determine concentration
        if pollutant == "Clean_Air":
            concentration = round(np.random.uniform(0.1, 5.0), 2)
        else:
            # Log-normal distribution of industrial emissions
            raw_conc = np.random.lognormal(mean=4.2, sigma=0.75)
            concentration = round(float(np.clip(raw_conc, 5.0, 480.0)), 2)
            
        # Environmental covariates
        temp_c = round(float(np.random.uniform(18.0, 75.0)), 1) # Factory stack or exhaust temp
        humidity_pct = round(float(np.random.uniform(20.0, 85.0)), 1)
        flow_velocity_ms = round(float(np.random.uniform(0.8, 5.5)), 2)
        
        # Kinetic parameters
        tau_resp = round(float(np.random.uniform(*profile["resp_time_range"]) * np.random.uniform(0.9, 1.1)), 2)
        tau_rec = round(float(np.random.uniform(*profile["rec_time_range"]) * np.random.uniform(0.9, 1.1)), 2)
        
        conc_power = 0.82 if pollutant != "Clean_Air" else 1.0
        humidity_factor = 1.0 - (humidity_pct - 50.0) * 0.0018
        
        # Sensor steady-state responses
        sensor_values = {}
        for s_idx, sensor_name in enumerate(SENSOR_NAMES):
            affinity = profile["base_affinity"][s_idx]
            if pollutant == "Clean_Air":
                val = max(0.01, np.random.normal(0.03, 0.012))
            else:
                base_resp = affinity * (concentration ** conc_power) * 0.28 * humidity_factor
                # Add sensor cross-talk and Gaussian noise
                noise = np.random.normal(0, base_resp * 0.04 + 0.02)
                val = max(0.02, base_resp + noise)
            sensor_values[sensor_name] = round(float(val), 4)
            
        peak_amp = max(sensor_values.values())
        reaction_slope = round(float(peak_amp / max(tau_resp, 1.0) * np.random.uniform(0.85, 1.15)), 4)
        
        # Optical LSPR wavelength peak shift (nm)
        if pollutant == "Clean_Air":
            lspr_shift = round(float(np.random.uniform(0.0, 0.3)), 3)
        else:
            lspr_shift = round(float(profile["lspr_factor"] * concentration + np.random.normal(0, 0.25)), 3)
            lspr_shift = max(0.1, lspr_shift)
            
        # Regulatory hazard assessment
        if concentration > profile["critical_threshold_ug_m3"]:
            hazard_level = "CRITICAL"
        elif concentration > profile["hazard_threshold_ug_m3"]:
            hazard_level = "HAZARDOUS"
        elif concentration > (profile["hazard_threshold_ug_m3"] * 0.4):
            hazard_level = "MODERATE"
        else:
            hazard_level = "SAFE"
            
        record = {
            "sample_id": f"SMP-{idx+1:05d}",
            "factory_source": profile["common_source"],
            "temp_c": temp_c,
            "humidity_pct": humidity_pct,
            "flow_velocity_ms": flow_velocity_ms,
            **sensor_values,
            "peak_reaction_amplitude": peak_amp,
            "response_time_s": tau_resp,
            "recovery_time_s": tau_rec,
            "reaction_slope": reaction_slope,
            "lspr_shift_nm": lspr_shift,
            "pollutant_type": pollutant,
            "concentration_ug_m3": concentration,
            "hazard_level": hazard_level
        }
        records.append(record)
        
    df = pd.DataFrame(records)
    return df

if __name__ == "__main__":
    current_dir = os.path.dirname(os.path.abspath(__file__))
    output_path = os.path.join(current_dir, "nanoparticle_reaction_dataset.csv")
    metadata_path = os.path.join(current_dir, "dataset_metadata.json")
    
    print("Synthesizing nanoparticle reaction dataset based on multi-sensor reaction kinetics...")
    df = generate_reaction_dataset(num_samples=3000, random_seed=42)
    df.to_csv(output_path, index=False)
    print(f"Dataset successfully saved to: {output_path} ({len(df)} records)")
    
    metadata = {
        "dataset_name": "NanoGuard Factory Emission Reaction Dataset",
        "description": "Multi-channel reaction kinetics and LSPR spectral shift for industrial nanoparticle pollutant detection",
        "num_records": len(df),
        "num_features": len(df.columns),
        "classes": list(POLLUTANT_PROFILES.keys()),
        "sensor_channels": SENSOR_NAMES,
        "class_distribution": df["pollutant_type"].value_counts().to_dict(),
        "concentration_stats": {
            "mean": float(df["concentration_ug_m3"].mean()),
            "std": float(df["concentration_ug_m3"].std()),
            "min": float(df["concentration_ug_m3"].min()),
            "max": float(df["concentration_ug_m3"].max())
        }
    }
    with open(metadata_path, "w") as f:
        json.dump(metadata, f, indent=2)
    print(f"Metadata saved to: {metadata_path}")
