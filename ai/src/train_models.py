"""
RASHAD AI - Machine Learning Training Pipeline
Trains:
1. Unsupervised K-Means clustering for household vulnerability archetypes.
2. Supervised Random Forest Classifier for needs priority prediction with explainable feature importance.
3. Resource Demand Regressor for aid budget forecasting.
Exports serialized models (.joblib) and governance metadata (.json) to ai/models/
"""
import json
import sys
from pathlib import Path
from typing import Dict, Any

import joblib
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.metrics import classification_report, confusion_matrix, r2_score, mean_absolute_error, silhouette_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

# Add backend to sys.path
backend_path = Path(__file__).resolve().parent.parent.parent / "backend"
if str(backend_path) not in sys.path:
    sys.path.insert(0, str(backend_path))

from app.core.database import SessionLocal
from app.models.household import Household
from app.services.needs_service import NeedsAssessmentEngine
from feature_engineering import extract_features_from_household, FEATURE_COLUMNS

MODELS_DIR = Path(__file__).resolve().parent.parent / "models"
MODELS_DIR.mkdir(parents=True, exist_ok=True)


CLUSTER_DEFINITIONS = {
    0: {
        "title_ar": "أسر نازحة ومعدمة شديدة الهشاشة",
        "title_en": "Displaced & Destitute Severe Vulnerability",
        "recommended_intervention": "صرف إغاثة طارئة عاجلة + سلة غذائية + بدل إيواء",
        "description": "أسر تعاني من فقدان المأوى أو النزوح مع انعدام شبه تام للدخل ونقص الوثائق الثبوتية."
    },
    1: {
        "title_ar": "أسر ذات أعباء صحية وإعاقات مزمنة",
        "title_en": "Severe Health & Chronic Disability Burden",
        "recommended_intervention": "كفالة علاجية شهرية + إعانة نقدية للمعاقين",
        "description": "أسر يثقل كاهلها وجود أفراد يعانون من أمراض مزمنة أو إعاقات حركية وذهنية مستديمة."
    },
    2: {
        "title_ar": "أسر كبيرة بمعدل إعالة ودخل شحيح",
        "title_en": "Large High-Dependency Households",
        "recommended_intervention": "مساعدة نقدية متعددة الأغراض موسعة + كفالة أيتام",
        "description": "أسر تضم عدداً كبيراً من الأطفال والأيتام مع عائل وحيد بدخل متدنٍ للغاية."
    },
    3: {
        "title_ar": "أسر محدودة الدخل مع استقرار نسبي",
        "title_en": "Low-Income Moderate Need",
        "recommended_intervention": "مشاريع تمكين اقتصادي أصغر + دعم موسمي",
        "description": "أسر تمتلك سكناً أو إيجاراً مستقراً ودخلاً محدوداً، مؤهلة لمشاريع الإقراض الحسن والتمكين."
    }
}


def prepare_training_dataset():
    """
    Loads households from DB, extracts ML features and baseline target labels.
    """
    db = SessionLocal()
    try:
        households = db.query(Household).all()
        if not households:
            raise ValueError("No households found in database! Seed database first.")

        records = []
        for h in households:
            feat = extract_features_from_household(h)
            # Evaluate baseline assessment
            assessment = NeedsAssessmentEngine.evaluate_household(h, h.members)
            tier_val = assessment["priority_tier"].value if hasattr(assessment["priority_tier"], "value") else str(assessment["priority_tier"])
            feat["priority_tier"] = tier_val
            feat["composite_score"] = float(assessment["calculated_score"])
            # Target for aid regressor (standardized estimated emergency grant)
            base_amount = 40000.0 + (feat["num_members"] * 12000.0) + (feat["chronic_illness_count"] * 25000.0) + (feat["disability_count"] * 30000.0)
            if feat["housing_vulnerability"] >= 4.0:
                base_amount += 35000.0
            feat["estimated_aid_amount"] = round(base_amount, -2)
            records.append(feat)

        df = pd.DataFrame(records)
        return df
    finally:
        db.close()


def train_all_models():
    if sys.platform == "win32":
        sys.stdout.reconfigure(encoding="utf-8")

    print("==========================================================")
    print("   RASHAD AI - Machine Learning Training Pipeline")
    print("==========================================================")

    df = prepare_training_dataset()
    print(f"Loaded {len(df)} household records for ML training.")

    X = df[FEATURE_COLUMNS]
    y_class = df["priority_tier"]
    y_reg = df["estimated_aid_amount"]

    # 1. Feature Scaler
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    joblib.dump(scaler, MODELS_DIR / "scaler.joblib")
    print("[1/4] Feature Scaler fitted and saved.")

    # 2. Unsupervised Clustering (K-Means)
    kmeans = KMeans(n_clusters=4, random_state=42, n_init=10)
    clusters = kmeans.fit_predict(X_scaled)
    df["cluster"] = clusters
    sil_score = float(silhouette_score(X_scaled, clusters))
    joblib.dump(kmeans, MODELS_DIR / "vulnerability_kmeans.joblib")
    print(f"[2/4] K-Means Clustering trained (K=4, Silhouette Score: {sil_score:.3f}).")

    # Analyze cluster centers for archetype mapping
    cluster_stats = {}
    for c_id in range(4):
        c_subset = df[df["cluster"] == c_id]
        cluster_stats[c_id] = {
            "size": int(len(c_subset)),
            "percentage": round(float(len(c_subset) / len(df) * 100), 1),
            "avg_income": round(float(c_subset["monthly_income"].mean()), 2),
            "avg_members": round(float(c_subset["num_members"].mean()), 1),
            "avg_chronic": round(float(c_subset["chronic_illness_count"].mean()), 2),
            "avg_disability": round(float(c_subset["disability_count"].mean()), 2),
            "avg_housing_vuln": round(float(c_subset["housing_vulnerability"].mean()), 2),
            "info": CLUSTER_DEFINITIONS[c_id]
        }

    # 3. Supervised Classification (Random Forest)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y_class, test_size=0.25, random_state=42, stratify=y_class
    )

    clf = RandomForestClassifier(
        n_estimators=100,
        max_depth=6,
        random_state=42,
        class_weight="balanced"
    )
    clf.fit(X_train, y_train)
    y_pred = clf.predict(X_test)

    acc = float(clf.score(X_test, y_test))
    report = classification_report(y_test, y_pred, output_dict=True, zero_division=0)
    joblib.dump(clf, MODELS_DIR / "needs_random_forest.joblib")
    print(f"[3/4] Random Forest Classifier trained (Test Accuracy: {acc*100:.1f}%).")

    # Feature Importances
    importances = dict(zip(FEATURE_COLUMNS, [float(x) for x in clf.feature_importances_]))
    sorted_importances = dict(sorted(importances.items(), key=lambda item: item[1], reverse=True))

    # 4. Supervised Regression (Demand / Resource Forecasting)
    X_reg_train, X_reg_test, y_reg_train, y_reg_test = train_test_split(
        X, y_reg, test_size=0.25, random_state=42
    )
    regressor = RandomForestRegressor(n_estimators=100, max_depth=6, random_state=42)
    regressor.fit(X_reg_train, y_reg_train)
    y_reg_pred = regressor.predict(X_reg_test)

    r2 = float(r2_score(y_reg_test, y_reg_pred))
    mae = float(mean_absolute_error(y_reg_test, y_reg_pred))
    joblib.dump(regressor, MODELS_DIR / "demand_regressor.joblib")
    print(f"[4/4] Demand Regressor trained (R2 Score: {r2:.3f}, MAE: {mae:,.0f} YER).")

    # Export Model Metadata & Governance Report
    metadata = {
        "model_engine": "RASHAD_AI_ML_SUITE_V1.0",
        "trained_at": "2026-11-07",
        "random_seed": 42,
        "dataset_size": len(df),
        "features": FEATURE_COLUMNS,
        "clustering": {
            "algorithm": "K-Means",
            "n_clusters": 4,
            "silhouette_score": sil_score,
            "clusters": cluster_stats
        },
        "classifier": {
            "algorithm": "Random Forest Classifier",
            "n_estimators": 100,
            "max_depth": 6,
            "test_accuracy": acc,
            "classification_report": report,
            "feature_importances": sorted_importances
        },
        "demand_forecaster": {
            "algorithm": "Random Forest Regressor",
            "r2_score": r2,
            "mae_yer": mae
        },
        "governance_disclaimer": "مخرجات نماذج تعلم الآلة هي مؤشرات إحصائية وتحليلية مساندة للتصنيف واكتشاف الأنماط، ولا تمثل حكماً شرعياً أو قانونياً بالاستحقاق أو الحرمان."
    }

    metadata_path = MODELS_DIR / "model_metadata.json"
    with open(metadata_path, "w", encoding="utf-8") as f:
        json.dump(metadata, f, ensure_ascii=False, indent=2)

    print(f"\nMetadata and governance report exported to: {metadata_path}")
    print("Top 5 Predictive Features:")
    for feat, imp in list(sorted_importances.items())[:5]:
        print(f"  - {feat}: {imp*100:.2f}%")
    print("\nAll models trained and persisted successfully.")


if __name__ == "__main__":
    train_all_models()
