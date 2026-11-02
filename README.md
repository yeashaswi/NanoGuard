# 🛡️ NanoGuard: Industrial Nanoparticle Pollutant Detection Telemetry

NanoGuard is an end-to-end Machine Learning telemetry platform designed to solve the growing threat of **hazardous industrial nanoparticle emissions** released by manufacturing factories, chemical plants, and foundries.

---

## 📚 Curriculum Books (Learn & Replicate From Scratch)

The `handbook/` directory contains a 6-volume, first-principles curriculum covering all the physics, chemistry, mathematics, and code:

1. **[Book 1: Physics, Nanotoxicology & Reaction Chemistry](file:///Users/yashaswivunnam/Desktop/NanoGuard/handbook/BOOK_01_PHYSICS_AND_REACTION_CHEMISTRY.md)**
   * Nanoparticle surface area scaling ($3 / (\rho \cdot r)$)
   * Why optical particle counters fail ($d^6$ Rayleigh scattering drop-off)
   * Heterogeneous catalysis, oxygen ion exchange, and Langmuir rate kinetics
   * Localized Surface Plasmon Resonance (LSPR) dielectric shift physics
2. **[Book 2: Sensor Arrays & Signal Engineering](file:///Users/yashaswivunnam/Desktop/NanoGuard/handbook/BOOK_02_SENSOR_ARRAYS_AND_SIGNAL_ENGINEERING.md)**
   * Cross-reactive differential sensing arrays (the "Electronic Nose" concept)
   * The 8 transducer channels (`s1_sno2` to `s8_zno_nw`) and material properties
   * Extracting features from continuous reaction waveforms ($R(t)/R_0$, $\tau_{90}$, $\tau_{10}$, slopes, $\Delta\lambda$)
   * Humidity cross-sensitivity and Arrhenius temperature compensation
3. **[Book 3: Machine Learning from First Principles](file:///Users/yashaswivunnam/Desktop/NanoGuard/handbook/BOOK_03_MACHINE_LEARNING_FROM_FIRST_PRINCIPLES.md)**
   * Decision trees & Gini impurity mathematics
   * Random Forest bagging & subspace sampling variance reduction proofs
   * Gradient Boosted Trees: additive models, pseudo-residuals, shrinkage
   * Classification metrics (Precision, Recall, F1, ROC-AUC) & Regression metrics ($R^2$, RMSE, MAE)
4. **[Book 4: Dataset Curation & Synthetic Kinetics](file:///Users/yashaswivunnam/Desktop/NanoGuard/handbook/BOOK_04_DATASET_CURATION_AND_SYNTHESIS.md)**
   * Finding open datasets on UCI, Zenodo, Mendeley Data, and Kaggle
   * Formulating ordinary differential equations (ODEs) for chemical surface adsorption
   * Injecting realistic Gaussian measurement noise and baseline drift
5. **[Book 5: Production Systems, Regulatory Compliance & SCADA Integration](file:///Users/yashaswivunnam/Desktop/NanoGuard/handbook/BOOK_05_PRODUCTION_SYSTEMS_AND_REGULATORY_SCADA.md)**
   * CPCB and OSHA regulatory thresholds for industrial air emissions
   * 4-Tier automated hazard escalation matrix (SAFE, MODERATE, HAZARDOUS, CRITICAL)
   * Class-specific engineering mitigation protocols (ESP voltage ramp, pulse-jet cleaning, damper interlocks)
   * Industrial SCADA protocols (Modbus TCP, MQTT, edge gateways)
6. **[Book 6: Step-by-Step Code Replication Guide](file:///Users/yashaswivunnam/Desktop/NanoGuard/handbook/BOOK_06_STEP_BY_STEP_REPLICATION_GUIDE.md)**
   * Complete tutorial to build every script from an empty directory

---

## 🔬 Core Detection Methodology: Reaction-Based Sensing
Conventional air quality monitors struggle to detect sub-100nm particles because they are smaller than the diffraction limit of light ($I \propto d^6 / \lambda^4$).

NanoGuard solves this using **Nanomaterial Surface Reaction Signatures**:
1. **Catalytic & Chemiresistive Adsorption**: Factory flue gas passes over an 8-channel cross-reactive nanosensor matrix ($\text{SnO}_2$, $\text{WO}_3$, reduced graphene oxide, Pt-doped $\text{TiO}_2$, and $\text{ZnO}$ nanowires). Adsorption causes rapid catalytic redox reactions, resulting in characteristic differential conductance kinetics:
   $$\frac{\Delta R(t)}{R_0}$$
2. **Localized Surface Plasmon Resonance (LSPR)**: Plasmonic gold nano-islands transduce dielectric shifts caused by nanoparticle surface binding into real-time optical extinction shifts ($\Delta \lambda_{LSPR}$).
3. **Dual-Model Inference**:
   - **Pollutant Classifier**: Identifies the chemical nature of the particle ($\text{TiO}_2$, $\text{ZnO}$, $\text{CuO}$, $\text{Ag-NP}$, Carbon Soot, $\text{SiO}_2$, or Clean Baseline).
   - **Quantitative Regressor**: Quantifies the mass concentration in $\mu\text{g/m}^3$ and flags regulatory violations against CPCB, WHO, and OSHA emission ceilings.

---

## 🧠 Benchmark Results

| Model Task | Algorithm | Metric | Test Benchmark |
| :--- | :--- | :--- | :--- |
| **Pollutant Identification** | Calibrated Balanced Random Forest | Multi-class Accuracy | **100.00%** |
| | | 5-Fold Stratified Cross-Validation | **99.88% (±0.10%)** |
| | | Weighted F1-Score | **1.0000** |
| **Concentration Quantification** | Gradient Boosting Regressor | Coefficient of Determination ($R^2$) | **0.9595 (96% variance)** |
| | | Root Mean Squared Error (RMSE) | **14.60 $\mu\text{g/m}^3$** |
| | | Mean Absolute Error (MAE) | **4.91 $\mu\text{g/m}^3$** |

---

## ⚡ Deployment Options

### Option A: Modern Dark Web UI (Vercel-Ready)
Built strictly following the **Modern Dark** design system (near-black `#050505`, opaque graphite panels `#0e0e0e`, hairlines `#222222`, Geist & Geist Mono typography, tiny mint signal `#3fd6c6`, zero generic AI gimmicks).

1. **Local Preview**:
   ```bash
   npm run build
   npm run preview
   ```
   Open **[http://localhost:3000](http://localhost:3000)**

2. **Deploy to Vercel**:
   * Connect this repository to Vercel (or run `npx vercel`).
   * The included `vercel.json` and `package.json` configure everything automatically.
   * Runs client-side calibrated ML inference with sub-10ms response times and zero external server dependencies!

### Option B: Python Streamlit Telemetry Engine
1. **Run Unit Tests**:
   ```bash
   ./venv/bin/python -m unittest tests/test_model_pipeline.py
   ```
2. **Launch Streamlit Dashboard**:
   ```bash
   ./run_nanoguard.sh
   # Or directly:
   HOME=/tmp ./venv/bin/python -m streamlit run app.py --server.headless true --server.port 8501
   ```
   Open **[http://localhost:8501](http://localhost:8501)**
