"""
NanoGuard: Model Training Pipeline for Nanoparticle Pollutant Detection
Trains and validates:
1. Multi-class Nanoparticle Pollutant Classifier (RandomForest / GradientBoosting)
2. Quantitative Concentration Regressor (GradientBoostingRegressor)
Evaluates and serializes all models, scaler, feature metadata, and metrics.
"""

import os
import json
import joblib
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split, cross_val_score, StratifiedKFold
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier, GradientBoostingRegressor, ExtraTreesClassifier
from sklearn.metrics import (
    classification_report,
    confusion_matrix,
    accuracy_score,
    f1_score,
    r2_score,
    mean_squared_error,
    mean_absolute_error,
    roc_auc_score
)

def train_pipeline(data_path: str, output_dir: str):
    os.makedirs(output_dir, exist_ok=True)
    
    print(f"Loading dataset from: {data_path}")
    df = pd.read_csv(data_path)
    
    feature_cols = [
        "temp_c",
        "humidity_pct",
        "flow_velocity_ms",
        "s1_sno2",
        "s2_wo3",
        "s3_graphene",
        "s4_au_nano",
        "s5_cnt",
        "s6_in2o3",
        "s7_tio2_pt",
        "s8_zno_nw",
        "peak_reaction_amplitude",
        "response_time_s",
        "recovery_time_s",
        "reaction_slope",
        "lspr_shift_nm"
    ]
    
    X = df[feature_cols].copy()
    y_class = df["pollutant_type"].copy()
    y_reg = df["concentration_ug_m3"].copy()
    
    # Stratified Train/Test split for balanced class validation
    X_train, X_test, y_class_train, y_class_test, y_reg_train, y_reg_test = train_test_split(
        X, y_class, y_reg, test_size=0.20, random_state=42, stratify=y_class
    )
    
    print(f"Training set: {len(X_train)} samples | Testing set: {len(X_test)} samples")
    
    # Feature Scaling
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    # ----------------------------------------------------
    # 1. CLASSIFIER: Nanoparticle Identification
    # ----------------------------------------------------
    print("\n--- Training Pollutant Classifier (Random Forest / ExtraTrees Ensemble) ---")
    clf = RandomForestClassifier(
        n_estimators=150,
        max_depth=16,
        min_samples_split=3,
        class_weight="balanced",
        random_state=42,
        n_jobs=-1
    )
    clf.fit(X_train_scaled, y_class_train)
    
    y_class_pred = clf.predict(X_test_scaled)
    y_class_proba = clf.predict_proba(X_test_scaled)
    
    clf_accuracy = accuracy_score(y_class_test, y_class_pred)
    clf_f1 = f1_score(y_class_test, y_class_pred, average="weighted")
    clf_classes = list(clf.classes_)
    
    # Cross-validation
    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
    cv_scores = cross_val_score(clf, X_train_scaled, y_class_train, cv=cv, scoring="accuracy")
    
    print(f"Classifier Accuracy: {clf_accuracy * 100:.2f}%")
    print(f"Classifier F1-Score: {clf_f1:.4f}")
    print(f"5-Fold CV Accuracy: {cv_scores.mean() * 100:.2f}% (+/- {cv_scores.std() * 100:.2f}%)")
    
    conf_mat = confusion_matrix(y_class_test, y_class_pred, labels=clf_classes)
    class_report = classification_report(y_class_test, y_class_pred, output_dict=True)
    
    feature_importances = dict(zip(feature_cols, [float(x) for x in clf.feature_importances_]))
    sorted_importances = dict(sorted(feature_importances.items(), key=lambda item: item[1], reverse=True))
    
    # ----------------------------------------------------
    # 2. REGRESSOR: Quantitative Concentration Estimator
    # ----------------------------------------------------
    print("\n--- Training Quantitative Regressor (Gradient Boosting) ---")
    reg = GradientBoostingRegressor(
        n_estimators=180,
        learning_rate=0.08,
        max_depth=5,
        subsample=0.85,
        random_state=42
    )
    reg.fit(X_train_scaled, y_reg_train)
    
    y_reg_pred = reg.predict(X_test_scaled)
    y_reg_pred = np.clip(y_reg_pred, 0.0, None) # Non-negative concentrations
    
    reg_r2 = r2_score(y_reg_test, y_reg_pred)
    reg_rmse = np.sqrt(mean_squared_error(y_reg_test, y_reg_pred))
    reg_mae = mean_absolute_error(y_reg_test, y_reg_pred)
    
    print(f"Regressor R2 Score: {reg_r2:.4f}")
    print(f"Regressor RMSE: {reg_rmse:.2f} ug/m3")
    print(f"Regressor MAE: {reg_mae:.2f} ug/m3")
    
    # ----------------------------------------------------
    # 3. SAVE ARTIFACTS
    # ----------------------------------------------------
    scaler_file = os.path.join(output_dir, "scaler.joblib")
    clf_file = os.path.join(output_dir, "classifier_model.joblib")
    reg_file = os.path.join(output_dir, "regressor_model.joblib")
    meta_file = os.path.join(output_dir, "feature_metadata.json")
    metrics_file = os.path.join(output_dir, "evaluation_metrics.json")
    
    joblib.dump(scaler, scaler_file)
    joblib.dump(clf, clf_file)
    joblib.dump(reg, reg_file)
    
    metadata = {
        "feature_cols": feature_cols,
        "classes": clf_classes,
        "num_features": len(feature_cols),
        "target_classification": "pollutant_type",
        "target_regression": "concentration_ug_m3",
        "feature_importances": sorted_importances
    }
    with open(meta_file, "w") as f:
        json.dump(metadata, f, indent=2)
        
    metrics = {
        "classifier": {
            "accuracy": float(clf_accuracy),
            "f1_score": float(clf_f1),
            "cv_accuracy_mean": float(cv_scores.mean()),
            "cv_accuracy_std": float(cv_scores.std()),
            "confusion_matrix": conf_mat.tolist(),
            "classes": clf_classes,
            "classification_report": class_report
        },
        "regressor": {
            "r2_score": float(reg_r2),
            "rmse": float(reg_rmse),
            "mae": float(reg_mae)
        }
    }
    with open(metrics_file, "w") as f:
        json.dump(metrics, f, indent=2)
        
    print("\nModels and metadata successfully saved!")
    print(f"Saved artifacts to {output_dir}")
    return metrics

if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_path = os.path.join(base_dir, "data", "nanoparticle_reaction_dataset.csv")
    output_dir = os.path.join(base_dir, "models")
    train_pipeline(data_path, output_dir)
