# Book 4: Dataset Curation & Synthetic Kinetics

When building machine learning systems for cutting-edge materials and environmental sensors, finding the right dataset is often the hardest challenge. This module outlines open repositories, literature extraction techniques, and how to build physically grounded synthetic simulators when experimental lab data is proprietary.

---

## 1. Where to Source Nanoparticle & Chemical Sensing Datasets

### 1.1 Open Scientific Repositories
* **UCI Machine Learning Repository**:
  * *Gas Sensor Array Drift Dataset*: 13,910 continuous multi-channel time-series measurements across 16 metal-oxide sensors exposed to 6 volatile chemicals over 36 months.
  * *Gas Sensor Array Under Dynamic Gas Mixtures*: High-speed 100 Hz continuous time-series capturing dynamic adsorption and flow modulation.
* **Zenodo (CERN / OpenAIRE)**:
  * *NanoGROC-Sens*: Open-source gold nanoparticle optical concentration tracking data.
  * *Nanotoxicity & Particle Sizing Repositories*: Tables of hydrodynamic size, surface charge ($\zeta$-potential), and catalytic dissolution rates for engineered metal oxides ($\text{TiO}_2$, $\text{ZnO}$, $\text{CuO}$, $\text{Ag-NP}$).
* **Mendeley Data & Figshare**:
  * Search keywords: `"chemiresistive sensor array"`, `"LSPR nanoparticle detection"`, `"SERS pollutant spectral dataset"`.
  * Researchers frequently deposit raw CSV/OriginLab files containing multi-sensor resistance curves and spectrometer extinction curves as supplementary materials.

---

## 2. The Physics-Grounded Kinetic Simulator

In industrial environmental telemetry, training data must cover extreme conditions (e.g., $75^\circ\text{C}$ stack temperatures, sudden 200 $\mu\text{g/m}^3$ spikes, filter tears) that factory operators cannot safely trigger on demand.

To address this, NanoGuard integrates a **Kinetic Reaction Generator** based on verified chemical adsorption differential equations.

### 2.1 The Differential Equation Formulation
For each sensor channel $s$ and target pollutant $p$, surface adsorption during exposure obeys:

$$\frac{d\theta_s(t)}{dt} = k_{\text{ads}}(T) \cdot C^\beta \cdot (1 - \theta_s(t)) - k_{\text{des}} \cdot \theta_s(t)$$

Solving with boundary condition $\theta_s(0) = 0$ yields the analytical expression used in [data/dataset_generator.py](file:///Users/yashaswivunnam/Desktop/NanoGuard/data/dataset_generator.py):

$$\theta_s(t) = \theta_{\text{eq}} \left(1 - e^{-t / \tau_{\text{resp}}}\right)$$

Where:
* **$\theta_{\text{eq}} = A_{p, s} \cdot C^\beta \cdot f(\text{Humidity})$**: The steady-state equilibrium coverage.
* **$A_{p, s} \in [0, 1]$**: The specific affinity coefficient of sensor $s$ for pollutant $p$.
* **$\beta \approx 0.82$**: The empirical Freundlich isotherm non-linearity exponent.
* **$\tau_{\text{resp}} = \frac{\tau_0}{k_{\text{Arrhenius}}(T)}$**: Temperature-accelerated response time constant.

### 2.2 Adding Realistic Experimental Noise
A synthetic dataset that is too clean causes ML models to overfit and fail on physical hardware. We inject three realistic noise regimes:
1. **Gaussian Measurement Noise**: $\mathcal{N}(0, \sigma^2)$ representing electronic amplifier and analog-to-digital converter (ADC) thermal noise.
2. **Sensor Cross-Talk**: Off-diagonal coupling representing secondary reactions from ambient VOCs.
3. **Humidity Scaling**: $f(RH) = 1.0 - (RH - 50.0) \times 0.0018$, reflecting competitive water vapor chemisorption on metal oxide surfaces.

---

## 3. Dataset Validation Checklist
Before training an ML model on your dataset, verify:
* **Class Balance**: Verify that every pollutant class has sufficient representation (in our dataset: $\sim 400-550$ samples per class).
* **Concentration Range**: Check that values span from trace levels ($< 5\ \mu\text{g/m}^3$) to emergency leak levels ($> 250\ \mu\text{g/m}^3$).
* **Physical Sanity Bounds**: Ensure no negative concentrations or resistance values exist.
* **Feature Correlations**: Inspect pairwise Pearson correlation coefficients to verify that sensors exhibit orthogonal, non-redundant responses.
