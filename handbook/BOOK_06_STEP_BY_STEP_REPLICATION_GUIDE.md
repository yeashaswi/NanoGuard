# Book 6: Step-by-Step Replication Guide

This guide walks you through replicating the complete NanoGuard system from an empty directory.

---

## Phase 1: Environment Setup

Create an isolated Python 3.10+ virtual environment and install core packages:

```bash
mkdir my-nanoguard && cd my-nanoguard
python3 -m venv venv
source venv/bin/activate

# Install scientific, ML, and dashboard dependencies
pip install numpy pandas scipy scikit-learn joblib matplotlib plotly streamlit
```

---

## Phase 2: Create Directory Architecture

```bash
mkdir -p data models tests
```

---

## Phase 3: Synthesize Reaction Dataset (`data/dataset_generator.py`)

1. Define the 8 sensor channels (`s1_sno2` to `s8_zno_nw`).
2. Define pollutant profiles with their chemical affinities, response times, and LSPR factors.
3. Implement `generate_sensor_time_series()` to compute $R(t)/R_0$ using the Langmuir rate equation.
4. Implement `generate_reaction_dataset(num_samples=3000)` and write output to `data/nanoparticle_reaction_dataset.csv`.
5. Run the generator:
   ```bash
   python data/dataset_generator.py
   ```

---

## Phase 4: Model Training Pipeline (`models/train.py`)

1. Load `data/nanoparticle_reaction_dataset.csv`.
2. Extract the 16 feature columns:
   ```python
   feature_cols = [
       "temp_c", "humidity_pct", "flow_velocity_ms",
       "s1_sno2", "s2_wo3", "s3_graphene", "s4_au_nano",
       "s5_cnt", "s6_in2o3", "s7_tio2_pt", "s8_zno_nw",
       "peak_reaction_amplitude", "response_time_s", "recovery_time_s",
       "reaction_slope", "lspr_shift_nm"
   ]
   ```
3. Perform a stratified 80/20 train/test split:
   ```python
   X_train, X_test, y_class_train, y_class_test, y_reg_train, y_reg_test = train_test_split(
       X, y_class, y_reg, test_size=0.20, random_state=42, stratify=y_class
   )
   ```
4. Fit `StandardScaler` strictly on `X_train` and transform both splits.
5. Train the `RandomForestClassifier` (150 trees, balanced weights).
6. Train the `GradientBoostingRegressor` (180 trees, learning rate 0.08, max depth 5).
7. Compute evaluation metrics (Classification accuracy, Confusion Matrix, 5-Fold Stratified CV, $R^2$, RMSE, MAE).
8. Save artifacts using `joblib.dump`:
   * `models/scaler.joblib`
   * `models/classifier_model.joblib`
   * `models/regressor_model.joblib`
   * `models/feature_metadata.json`
   * `models/evaluation_metrics.json`
9. Run training:
   ```bash
   python models/train.py
   ```

---

## Phase 5: Production Inference Engine (`models/inference.py`)

1. Create a class `NanoGuardInferenceEngine` that loads saved artifacts.
2. Implement `predict_single(feature_dict)`:
   - Scale input values.
   - Run classifier `predict()` and `predict_proba()`.
   - Run regressor `predict()`.
   - Evaluate against CPCB and OSHA thresholds to assign `SAFE`, `MODERATE`, `HAZARDOUS`, or `CRITICAL`.
   - Return structured dictionary with predictions, hazard levels, and mitigation steps.
3. Implement `predict_dataframe(df)` for batch auditing.

---

## Phase 6: Automated Test Suite (`tests/test_model_pipeline.py`)

Write unit tests verifying:
* Dataset presence and non-emptiness.
* Time-series output physical sanity bounds ($R(t)/R_0 \ge 1.0$).
* Single sample inference execution.
* Batch prediction DataFrame output format.
* Regulatory status escalation when concentration exceeds limits.

Run the tests:
```bash
python -m unittest tests/test_model_pipeline.py
```

---

## Phase 7: Web UI Deployment

* **For local telemetry / R&D**: Run the Streamlit app:
  ```bash
  streamlit run app.py
  ```
* **For production / Vercel**: Export model parameters to a lightweight client-side engine in Next.js / TypeScript, following the **Modern Dark** design system.
