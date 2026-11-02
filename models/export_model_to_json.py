"""
Exports trained model parameters to JSON for zero-dependency client-side inference.
"""

import os
import json
import joblib
import numpy as np

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
models_dir = os.path.join(base_dir, "models")

scaler = joblib.load(os.path.join(models_dir, "scaler.joblib"))
clf = joblib.load(os.path.join(models_dir, "classifier_model.joblib"))
reg = joblib.load(os.path.join(models_dir, "regressor_model.joblib"))

with open(os.path.join(models_dir, "feature_metadata.json")) as f:
    meta = json.load(f)

# Extract class-wise feature profiles / centroids in scaled space
data_path = os.path.join(base_dir, "data", "nanoparticle_reaction_dataset.csv")
import pandas as pd
df = pd.read_csv(data_path)

profiles = {}
for p in meta["classes"]:
    sub = df[df["pollutant_type"] == p]
    mean_feat = sub[meta["feature_cols"]].mean().to_dict()
    profiles[p] = mean_feat

export_data = {
    "feature_cols": meta["feature_cols"],
    "classes": meta["classes"],
    "scaler_mean": scaler.mean_.tolist(),
    "scaler_scale": scaler.scale_.tolist(),
    "profiles": profiles
}

out_path = os.path.join(models_dir, "exported_model_params.json")
with open(out_path, "w") as f:
    json.dump(export_data, f, indent=2)

print(f"Exported model parameters to {out_path}")
