# Book 2: Sensor Arrays & Signal Engineering

In this module, you will learn how multi-channel sensor arrays transduce chemical reactions into digital feature vectors, how to engineer features from continuous reaction waveforms, and how to compensate for industrial environmental noise.

---

## 1. The Cross-Reactive Array Philosophy

A single chemical sensor is rarely 100% selective. In real factory exhaust, volatile organics, moisture, and temperature fluctuations interfere with single-channel readings.

To overcome this, NanoGuard employs **Cross-Reactive Differential Sensing** (inspired by mammalian olfactory systems):
* Instead of building one sensor that responds exclusively to $\text{TiO}_2$, we construct an **array of 8 diverse nanomaterial sensors**.
* Each sensor has a different chemical composition, doping level, and surface morphology.
* Every target pollutant produces a **unique multivariate reaction pattern** across the 8 channels.

```
Factory Exhaust Stream
       │
       ▼
┌────────────────────────────────────────────────────────┐
│               NanoGuard 8-Channel Sensor Array         │
│  [S1: SnO2]  [S2: WO3]  [S3: rGO]     [S4: Au Plasmon] │
│  [S5: CNT]   [S6: In2O3][S7: Pt-TiO2] [S8: ZnO NW]    │
└────────────────────────────────────────────────────────┘
       │
       ▼
  8 Parallel Reaction Waveforms R_i(t)
       │
       ▼
  Feature Extraction Pipeline (16-D Feature Vector)
```

---

## 2. Channel Specifications & Transducer Physics

| Channel | Sensor Transducer Material | Sensing Physics | Primary Affinity Target |
| :--- | :--- | :--- | :--- |
| **`s1_sno2`** | Nanocrystalline $\text{SnO}_2$ thick film | Wide-bandgap semiconductor ($E_g = 3.6\text{ eV}$); oxygen ion exchange | Broad sensitivity; $\text{TiO}_2$ & $\text{CuO}$ |
| **`s2_wo3`** | Porous $\text{WO}_3$ nanoplates | n-type transition oxide with rich surface oxygen vacancies | Copper oxide ($\text{CuO}$) & acid vapors |
| **`s3_graphene`**| Reduced Graphene Oxide (rGO) | 2D ballistic carrier transport; aromatic $\pi$-electron stacking | Nano-Silver ($\text{Ag-NP}$) & Carbon Soot |
| **`s4_au_nano`** | Au Nano-island thin film | Localized Surface Plasmon Resonance (LSPR) optical extinction | High dielectric metal NPs ($\text{Ag-NP}$, $\text{CuO}$) |
| **`s5_cnt`** | Multi-walled Carbon Nanotubes (MWCNT)| 1D ballistic conductance; interstitial adsorption channels | Carbonaceous soot & organic aerosols |
| **`s6_in2o3`** | Mesoporous $\text{In}_2\text{O}_3$ nanospheres| High surface-to-volume ratio; redox surface catalytic exchange | $\text{CuO}$ & high-temperature exhaust |
| **`s7_tio2_pt`**| Platinum-doped $\text{TiO}_2$ nanocrystals | Catalytic spillover effect; noble metal catalytic enhancement | Titanium Dioxide ($\text{TiO}_2$) self-affinity |
| **`s8_zno_nw`** | Single-crystal $\text{ZnO}$ nanowire array | 1D electron transport with polar (0001) crystal faces | Zinc Oxide ($\text{ZnO}$) aerosols |

---

## 3. Extracting Features from Continuous Waveforms

Raw sensor data streams arrive as continuous voltage or resistance time-series $R(t)$ sampled at $2-10\text{ Hz}$. A machine learning model requires compact, informative feature representations.

```
       Relative
      Resistance
       (R/R0)
         ▲
         │                 Peak Reaction Amplitude
         │                         ▲
   R_max ┼─────────────────────────┼──────┐
         │                        /       │ \
         │                       /        │  \
         │     Initial Slope    /         │   \    Recovery Phase
         │     d(ΔR)/dt        /          │    \   (Desorption)
         │       ▲            /           │     \
         │      /            /            │      \
     1.0 ┼─────┴────────────┘             │       └─────────────
         │    Baseline       │◄─- τ_90 ──►│◄──── τ_10 ────►│
         └────┬──────────────┬────────────┬────────────────────►
              t0             t_start      t_peak               Time (s)
```

### Feature 1: Baseline Normalization ($\Delta R / R_0$)
To eliminate sensor-to-sensor manufacturing tolerances and baseline drift:

$$S_i(t) = \frac{R_i(t) - R_{0, i}}{R_{0, i}}$$

Where $R_{0, i}$ is the steady-state baseline resistance measured in pure carrier air prior to exhaust exposure.

### Feature 2: Peak Reaction Amplitude ($\Delta R_{\max}$)
The maximum steady-state response achieved during the exposure phase:

$$\Delta R_{\max} = \max_{t \in [t_{\text{start}}, t_{\text{end}}]} S_i(t)$$

This parameter scales monotonically with the target pollutant concentration via the Freundlich/Langmuir isotherm:

$$\Delta R_{\max} \approx k \cdot C^\beta \quad (\text{with } 0.7 \le \beta \le 1.0)$$

### Feature 3: Reaction Rise Time ($\tau_{90}$)
The elapsed time required for the sensor to transition from $10\%$ to $90\%$ of its peak response:

$$\tau_{90} = t_{0.9 \cdot \Delta R_{\max}} - t_{0.1 \cdot \Delta R_{\max}}$$

* Highly catalytic particles ($\text{Ag-NP}$, $\text{ZnO}$) trigger rapid electron transfer ($\tau_{90} \approx 6-14\text{s}$).
* Sluggish, larger agglomerates or dielectric particles ($\text{SiO}_2$) have slower diffusion kinetics ($\tau_{90} \approx 18-30\text{s}$).

### Feature 4: Desorption Recovery Time ($\tau_{10}$)
The elapsed time required for the sensor to return to $10\%$ above baseline after particle exposure ceases:

$$\tau_{10} = t_{0.1 \cdot \Delta R_{\max}\text{ (recovery)}} - t_{\text{exhaust shutoff}}$$

* Deep chemisorption (e.g., Carbon Soot on CNTs) binds tightly, resulting in prolonged recovery ($\tau_{10} > 60\text{s}$).
* Reversible physisorption exhibits swift clearing ($\tau_{10} < 25\text{s}$).

### Feature 5: Initial Reaction Slope ($\left.\frac{d(\Delta R)}{dt}\right|_{t=0}$)
Approximated over the initial $3-5$ seconds of exposure:

$$\text{Slope} \approx \frac{\Delta R(t_0 + \Delta t) - \Delta R(t_0)}{\Delta t}$$

Proportional to the initial molecular/particulate collision rate per unit area (Arrhenius kinetic velocity).

### Feature 6: LSPR Optical Wavelength Peak Shift ($\Delta \lambda$)
Extracted from a mini-spectrometer monitoring the gold nano-island resonance peak:

$$\Delta \lambda = \lambda_{\text{exposed peak}} - \lambda_{\text{baseline peak}} \quad (\text{nm})$$

---

## 4. Environmental Confounding & Compensation

Industrial environments introduce three primary confounding factors:

### 4.1 Relative Humidity ($RH\%$) Interference
Water vapor adsorbs onto metal oxide surfaces:

$$\text{H}_2\text{O}_{\text{(gas)}} + \text{Sn}_{\text{Sn}} + \text{O}_{\text{O}} \rightleftharpoons (\text{Sn}_{\text{Sn}}^+ - \text{OH}^-) + (\text{O}_{\text{O}}\text{H})^+ + e^-$$

This donates electrons and lowers baseline resistance, mimicking reducing pollutants. By including `humidity_pct` as an explicit input feature, the ML algorithm learns the nonlinear compensation surface directly.

### 4.2 Flue Exhaust Temperature ($T_{\text{exhaust}}$)
Higher temperatures accelerate reaction kinetics according to the Arrhenius relation ($e^{-E_a / RT}$). Measuring `temp_c` directly allows the tree-based models to partition temperature regimes.

### 4.3 Duct Flow Velocity ($v_{\text{duct}}$)
Exhaust duct flow velocity ($0.8 - 5.5\text{ m/s}$) modulates the boundary layer thickness $\delta$ above the sensor surface. Higher velocities thin the boundary layer and enhance mass transport rate.
