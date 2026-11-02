# 📚 NanoGuard Curriculum & Engineering Handbook

A comprehensive, 6-volume educational curriculum for replicating the NanoGuard industrial nanoparticle pollutant detection platform from first principles.

---

### 📖 The Curriculum

1. **[Book 1: Physics, Nanotoxicology & Reaction Chemistry](file:///Users/yashaswivunnam/Desktop/NanoGuard/handbook/BOOK_01_PHYSICS_AND_REACTION_CHEMISTRY.md)**
   * What industrial nanoparticles are ($\text{TiO}_2$, $\text{ZnO}$, $\text{CuO}$, $\text{Ag-NP}$, Carbon Soot, $\text{SiO}_2$)
   * Toxicological pathways and human health hazards
   * Why optical particle counters fail ($d^6$ Rayleigh drop-off)
   * Chemiresistive surface reactions, oxygen ion exchange, and Langmuir rate kinetics
   * Localized Surface Plasmon Resonance (LSPR) dielectric shift physics

2. **[Book 2: Sensor Arrays & Signal Engineering](file:///Users/yashaswivunnam/Desktop/NanoGuard/handbook/BOOK_02_SENSOR_ARRAYS_AND_SIGNAL_ENGINEERING.md)**
   * Cross-reactive differential sensing arrays (the "Electronic Nose" concept)
   * The 8 transducer channels (`s1_sno2` to `s8_zno_nw`) and their material physics
   * Extracting features from continuous reaction waveforms ($R(t)/R_0$, $\tau_{90}$, $\tau_{10}$, slopes, $\Delta\lambda$)
   * Compensating for temperature drift, humidity interference, and duct velocity

3. **[Book 3: Machine Learning from First Principles](file:///Users/yashaswivunnam/Desktop/NanoGuard/handbook/BOOK_03_MACHINE_LEARNING_FROM_FIRST_PRINCIPLES.md)**
   * Decision tree mathematics: Gini impurity, candidate threshold evaluation, information gain
   * Random Forest architecture: bagging, variance reduction proof, random subspace sampling, class balancing
   * Gradient Boosted Trees: additive models, gradient descent in function space, pseudo-residuals, shrinkage
   * Evaluation metrics: Precision, Recall, F1, ROC-AUC, $R^2$, RMSE, MAE
   * Avoiding data leakage and conducting stratified K-fold cross-validation

4. **[Book 4: Dataset Curation & Synthetic Kinetics](file:///Users/yashaswivunnam/Desktop/NanoGuard/handbook/BOOK_04_DATASET_CURATION_AND_SYNTHESIS.md)**
   * Where to find open datasets (UCI Gas Sensor Array, Zenodo, Mendeley Data, Kaggle)
   * Formulating ordinary differential equations (ODEs) for Langmuir adsorption
   * Injecting realistic Gaussian noise, cross-talk, and humidity scaling
   * Dataset validation checklist

5. **[Book 5: Production Systems, Regulatory Compliance & SCADA Integration](file:///Users/yashaswivunnam/Desktop/NanoGuard/handbook/BOOK_05_PRODUCTION_SYSTEMS_AND_REGULATORY_SCADA.md)**
   * CPCB and OSHA regulatory thresholds for industrial ambient air
   * 4-Tier automated hazard escalation matrix (SAFE, MODERATE, HAZARDOUS, CRITICAL)
   * Class-specific engineering mitigation protocols (ESP voltage ramp, pulse-jet cleaning, damper interlocks)
   * Industrial protocols: Modbus TCP, MQTT, SCADA integration, and edge deployment

6. **[Book 6: Step-by-Step Replication Guide](file:///Users/yashaswivunnam/Desktop/NanoGuard/handbook/BOOK_06_STEP_BY_STEP_REPLICATION_GUIDE.md)**
   * End-to-end tutorial to build the entire pipeline from an empty directory
   * Directory structure, scripts, training runs, tests, and deployment
