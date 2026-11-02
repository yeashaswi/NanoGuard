"""
NanoGuard: Real-Time Inference Engine
Loads trained models, scales features, runs pollutant classification, concentration
regression, regulatory hazard checks, and generates mitigation guidance.
"""

import os
import json
import joblib
import numpy as np
import pandas as pd
from typing import Dict, Any, Tuple

HAZARD_STANDARDS = {
    "TiO2": {
        "standard_cpcb": 100.0,
        "osha_pel": 250.0,
        "mitigation": "Increase electrostatic precipitator voltage; engage PTFE secondary micro-filter."
    },
    "ZnO": {
        "standard_cpcb": 80.0,
        "osha_pel": 200.0,
        "mitigation": "Activate wet scrubbers with alkaline neutralizer; inspect baghouse filter seals."
    },
    "CuO": {
        "standard_cpcb": 50.0,
        "osha_pel": 150.0,
        "mitigation": "Urgent: Halt smelting furnace feed; activate high-efficiency particulate air (HEPA) line."
    },
    "Ag-NP": {
        "standard_cpcb": 25.0,
        "osha_pel": 75.0,
        "mitigation": "Critical containment breach: Isolate cleanroom air duct; engage catalytic carbon bed."
    },
    "Carbon_Soot": {
        "standard_cpcb": 60.0,
        "osha_pel": 180.0,
        "mitigation": "Adjust combustion air-to-fuel ratio; pulse-jet clean fabric filter compartments."
    },
    "SiO2": {
        "standard_cpcb": 90.0,
        "osha_pel": 220.0,
        "mitigation": "Initiate continuous water mist suppression; check cyclone separator pressure drop."
    },
    "Clean_Air": {
        "standard_cpcb": 15.0,
        "osha_pel": 50.0,
        "mitigation": "Nominal operations: All industrial filtration systems operating within WHO/CPCB limits."
    }
}

class NanoGuardInferenceEngine:
    def __init__(self, models_dir: str = None):
        if models_dir is None:
            models_dir = os.path.dirname(os.path.abspath(__file__))
            
        self.models_dir = models_dir
        self.scaler = joblib.load(os.path.join(models_dir, "scaler.joblib"))
        self.classifier = joblib.load(os.path.join(models_dir, "classifier_model.joblib"))
        self.regressor = joblib.load(os.path.join(models_dir, "regressor_model.joblib"))
        
        with open(os.path.join(models_dir, "feature_metadata.json"), "r") as f:
            self.metadata = json.load(f)
            
        with open(os.path.join(models_dir, "evaluation_metrics.json"), "r") as f:
            self.metrics = json.load(f)
            
        self.feature_cols = self.metadata["feature_cols"]
        self.classes = self.metadata["classes"]
        
    def predict_single(self, feature_dict: Dict[str, float]) -> Dict[str, Any]:
        """
        Runs dual inference on a single sensor reaction snapshot.
        """
        row_values = [feature_dict.get(col, 0.0) for col in self.feature_cols]
        X = pd.DataFrame([row_values], columns=self.feature_cols)
        X_scaled = self.scaler.transform(X)
        
        # Classification
        pred_class = str(self.classifier.predict(X_scaled)[0])
        probas = self.classifier.predict_proba(X_scaled)[0]
        class_probas = {cls_name: float(p) for cls_name, p in zip(self.classes, probas)}
        confidence = float(max(probas))
        
        # Regression
        pred_conc = float(max(0.0, self.regressor.predict(X_scaled)[0]))
        if pred_class == "Clean_Air":
            pred_conc = min(pred_conc, 5.0)
            
        # Hazard & Regulatory evaluation
        rules = HAZARD_STANDARDS.get(pred_class, HAZARD_STANDARDS["Clean_Air"])
        cpcb_limit = rules["standard_cpcb"]
        osha_limit = rules["osha_pel"]
        
        if pred_conc > osha_limit:
            hazard = "CRITICAL"
            badge_color = "#dc2626" # Red
            status_text = "Severe Emission Ceiling Breach (Action Required)"
        elif pred_conc > cpcb_limit:
            hazard = "HAZARDOUS"
            badge_color = "#ea580c" # Orange
            status_text = "Exceeds Environmental Standard (CPCB Threshold)"
        elif pred_conc > (cpcb_limit * 0.5):
            hazard = "MODERATE"
            badge_color = "#ca8a04" # Yellow
            status_text = "Elevated Trace Emission (Monitor Closely)"
        else:
            hazard = "SAFE"
            badge_color = "#16a34a" # Green
            status_text = "Nominal Compliant Operation"
            
        return {
            "pollutant": pred_class,
            "confidence": confidence,
            "probabilities": class_probas,
            "predicted_concentration_ug_m3": round(pred_conc, 2),
            "hazard_level": hazard,
            "badge_color": badge_color,
            "status_text": status_text,
            "cpcb_limit": cpcb_limit,
            "osha_limit": osha_limit,
            "mitigation_plan": rules["mitigation"]
        }
        
    def predict_dataframe(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Runs batch predictions on a DataFrame with required sensor columns.
        """
        missing = [c for c in self.feature_cols if c not in df.columns]
        if missing:
            raise ValueError(f"Missing required sensor feature columns: {missing}")
            
        X = df[self.feature_cols].copy()
        X_scaled = self.scaler.transform(X)
        
        classes = self.classifier.predict(X_scaled)
        concs = np.clip(self.regressor.predict(X_scaled), 0.0, None)
        probas = np.max(self.classifier.predict_proba(X_scaled), axis=1)
        
        result_df = df.copy()
        result_df["pred_pollutant"] = classes
        result_df["pred_confidence"] = np.round(probas * 100, 1)
        result_df["pred_concentration_ug_m3"] = np.round(concs, 2)
        
        # Hazard levels
        hazards = []
        for p, c in zip(classes, concs):
            std = HAZARD_STANDARDS.get(p, HAZARD_STANDARDS["Clean_Air"])["standard_cpcb"]
            pel = HAZARD_STANDARDS.get(p, HAZARD_STANDARDS["Clean_Air"])["osha_pel"]
            if c > pel:
                hazards.append("CRITICAL")
            elif c > std:
                hazards.append("HAZARDOUS")
            elif c > (std * 0.5):
                hazards.append("MODERATE")
            else:
                hazards.append("SAFE")
                
        result_df["pred_hazard_level"] = hazards
        return result_df
