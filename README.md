# NanoGuard 🛡️

A simulation telemetry dashboard and machine learning study exploring industrial nanoparticle pollutant detection.

---

## What This Project Is

NanoGuard is an exploratory machine learning and data science project investigating how multi-channel sensor arrays could theoretically detect and quantify airborne nanoparticle emissions (such as metal oxides $\text{TiO}_2$, $\text{ZnO}$, and carbon soot) released in industrial flue gas.

The repository includes:
- **Synthetic Sensor Kinetics Generator (`data/dataset_generator.py`):** Models simulated differential resistance responses ($\Delta R(t)/R_0$) and optical extinction shifts based on chemical adsorption kinetics.
- **ML Models (`models/`):** A Random Forest classifier for pollutant identification and a Gradient Boosting regressor for mass concentration estimates ($\mu\text{g/m}^3$).
- **Interactive Streamlit Dashboard (`app.py`):** A local dashboard to simulate sensor time-series, run inference, and visualize response curves.
- **Web Frontend (`src/`):** A client-side web interface demonstrating telemetry monitoring.
- **Curriculum Notes (`handbook/`):** A 6-part set of study notes exploring the theoretical physics, chemistry, and ML mathematics behind sensor arrays.

---

## ⚠️ Important Reality Check & Limitations

1. **The Dataset is 100% Synthetic:** The data used to train and test these models is generated programmatically in `dataset_generator.py` using idealized mathematical formulas and Gaussian noise.
2. **Why Test Accuracy is ~100%:** The benchmark metrics (e.g. 99.9%+ cross-validation score) occur because the test set follows the exact same mathematical equations used to generate the training set. This is a known artifact of synthetic data and does **not** indicate real-world performance.
3. **No Physical Hardware Deployment:** The sensor array ($\text{SnO}_2$, $\text{WO}_3$, $\text{ZnO}$, LSPR nano-islands) has **not** been physically fabricated or field-tested in an actual industrial smoke stack or factory.
4. **Real-World Complexities:** Real factory exhaust contains high moisture, sensor-poisoning contaminants, severe baseline drift, and temperature swings that would significantly reduce accuracy without active recalibration and physical filtering.
5. **Educational Scope:** This project serves as an educational simulation of sensor telemetry and multi-channel signal processing.

---

## Tech Stack

- **Python:** Streamlit, scikit-learn, NumPy, Pandas, Plotly
- **Web Frontend:** React, Vite, Tailwind CSS

---

## How to Run

### Python Streamlit Dashboard

```bash
# Set up virtual environment
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt  # or: pip install streamlit scikit-learn pandas plotly

# Run tests
python -m unittest tests/test_model_pipeline.py

# Launch dashboard
streamlit run app.py
```

Open [http://localhost:8501](http://localhost:8501) in your browser.

### Web Frontend

```bash
npm install
npm run dev
```

Open [http://localhost:5173](http://localhost:5173) in your browser.

---

## License

MIT
