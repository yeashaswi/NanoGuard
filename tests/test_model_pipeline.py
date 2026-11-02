"""
Unit and integration tests for NanoGuard Nanoparticle Pollutant Detection Pipeline.
"""

import os
import unittest
import numpy as np
import pandas as pd
from data.dataset_generator import generate_sensor_time_series, SENSOR_NAMES, POLLUTANT_PROFILES
from models.inference import NanoGuardInferenceEngine

class TestNanoGuardPipeline(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        cls.models_dir = os.path.join(base_dir, "models")
        cls.data_path = os.path.join(base_dir, "data", "nanoparticle_reaction_dataset.csv")
        cls.engine = NanoGuardInferenceEngine(cls.models_dir)

    def test_dataset_exists_and_valid(self):
        self.assertTrue(os.path.exists(self.data_path), "Dataset CSV file must exist")
        df = pd.read_csv(self.data_path)
        self.assertGreaterEqual(len(df), 1000, "Dataset should have at least 1000 records")
        for col in self.engine.feature_cols:
            self.assertIn(col, df.columns, f"Feature {col} must be in dataset")
        self.assertIn("pollutant_type", df.columns)
        self.assertIn("concentration_ug_m3", df.columns)
        self.assertIn("hazard_level", df.columns)

    def test_sensor_reaction_kinetics(self):
        t, curves = generate_sensor_time_series(
            pollutant="TiO2",
            concentration_ug_m3=120.0,
            temp_c=30.0,
            humidity_pct=45.0,
            total_duration_s=60.0,
            dt=1.0
        )
        self.assertEqual(len(t), 60)
        for s in SENSOR_NAMES:
            self.assertIn(s, curves)
            self.assertEqual(len(curves[s]), 60)
            # Baseline should start near 1.0 (R/R0)
            self.assertAlmostEqual(curves[s][0], 1.0, delta=0.15)
            # Max response during exposure should exceed baseline for 120 ug/m3
            self.assertGreater(np.max(curves[s]), 1.0)

    def test_inference_single_prediction(self):
        sample = {col: 1.0 for col in self.engine.feature_cols}
        sample["s1_sno2"] = 15.0
        sample["s7_tio2_pt"] = 18.0
        sample["lspr_shift_nm"] = 5.0
        sample["peak_reaction_amplitude"] = 18.0
        
        result = self.engine.predict_single(sample)
        self.assertIn("pollutant", result)
        self.assertIn("confidence", result)
        self.assertIn("predicted_concentration_ug_m3", result)
        self.assertIn("hazard_level", result)
        self.assertIn("mitigation_plan", result)
        self.assertGreaterEqual(result["confidence"], 0.0)
        self.assertLessEqual(result["confidence"], 1.0)
        self.assertGreaterEqual(result["predicted_concentration_ug_m3"], 0.0)

    def test_batch_prediction(self):
        df = pd.read_csv(self.data_path).head(20)
        pred_df = self.engine.predict_dataframe(df)
        self.assertIn("pred_pollutant", pred_df.columns)
        self.assertIn("pred_concentration_ug_m3", pred_df.columns)
        self.assertIn("pred_hazard_level", pred_df.columns)
        self.assertEqual(len(pred_df), 20)

    def test_regulatory_escalation(self):
        # Clean air check
        clean_sample = {col: 0.05 for col in self.engine.feature_cols}
        clean_sample["peak_reaction_amplitude"] = 0.04
        clean_sample["lspr_shift_nm"] = 0.02
        res_clean = self.engine.predict_single(clean_sample)
        self.assertIn(res_clean["hazard_level"], ["SAFE", "MODERATE"])

if __name__ == "__main__":
    unittest.main()
