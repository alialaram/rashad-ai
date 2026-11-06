"""
RASHAD AI - Machine Learning Inference & Decision Support Service
Loads trained models (K-Means, Random Forest Classifier, Demand Regressor)
and generates real-time predictions, clustering archetypes, and explainability metrics.
"""
import json
import logging
from pathlib import Path
from typing import Dict, Any, Optional

import joblib
import numpy as np
import pandas as pd

from app.models.household import (
    Household,
    HouseholdMember,
    HousingType,
    HealthStatus,
    EmploymentStatus,
    RelationshipType,
)

logger = logging.getLogger("rashad_ai.ml")

# Locate models dir
MODELS_DIR = Path(__file__).resolve().parent.parent.parent.parent / "ai" / "models"

FEATURE_COLUMNS = [
    "monthly_income",
    "num_members",
    "income_per_capita",
    "dependency_ratio",
    "num_earners",
    "num_children",
    "num_elderly",
    "chronic_illness_count",
    "disability_count",
    "housing_vulnerability",
    "is_undocumented",
    "is_female_headed",
]

FEATURE_LABELS_AR = {
    "monthly_income": "إجمالي الدخل الشهري",
    "num_members": "عدد أفراد الأسرة",
    "income_per_capita": "نصيب الفرد من الدخل",
    "dependency_ratio": "نسبة الإعالة الأسرية",
    "num_earners": "عدد العاملين الفعليين",
    "num_children": "عدد الأطفال دون 18",
    "num_elderly": "عدد كبار السن فوق 60",
    "chronic_illness_count": "حالات الأمراض المزمنة",
    "disability_count": "حالات الإعاقة المستديمة",
    "housing_vulnerability": "هشاشة السكن والمأوى",
    "is_undocumented": "غياب الوثائق الرسمية",
    "is_female_headed": "أسرة تعولها امرأة",
}

HOUSING_WEIGHTS = {
    HousingType.MAKSHA.value: 5.0,
    HousingType.DISPLACED_CAMP.value: 4.5,
    HousingType.SHARED.value: 3.0,
    HousingType.RENTED.value: 2.0,
    HousingType.OWNED.value: 0.5,
}


def extract_features_from_household(household: Household) -> Dict[str, float]:
    """
    Extracts a standardized numeric feature vector for a single household.
    """
    members = household.members or []
    num_members = max(1, len(members))
    monthly_income = float(household.monthly_income or 0.0)

    earners = 0
    dependents = 0
    num_children = 0
    num_elderly = 0
    chronic_illness_count = 0
    disability_count = 0

    for m in members:
        age = m.approximate_age or 30
        if age < 18:
            num_children += 1
            dependents += 1
        elif age >= 60:
            num_elderly += 1
            dependents += 1
        elif m.health_status == HealthStatus.DISABILITY or m.disability_type:
            dependents += 1

        if m.employment_status == EmploymentStatus.EMPLOYED:
            earners += 1

        if m.health_status == HealthStatus.CHRONIC_DISEASE:
            chronic_illness_count += 1
        elif m.health_status == HealthStatus.DISABILITY or m.disability_type:
            disability_count += 1

    dependency_ratio = dependents / max(1, num_members)
    income_per_capita = monthly_income / num_members

    head_member = next((m for m in members if m.relationship == RelationshipType.HEAD), None)
    is_female_headed = 1.0 if (head_member and head_member.gender == "FEMALE") else 0.0

    housing_str = household.housing_type.value if hasattr(household.housing_type, "value") else str(household.housing_type)
    housing_vulnerability = HOUSING_WEIGHTS.get(housing_str, 2.0)
    is_undocumented = 1.0 if (household.id_type and household.id_type.value == "TEMPORARY_ID") else 0.0

    return {
        "monthly_income": monthly_income,
        "num_members": float(num_members),
        "income_per_capita": float(income_per_capita),
        "dependency_ratio": float(dependency_ratio),
        "num_earners": float(earners),
        "num_children": float(num_children),
        "num_elderly": float(num_elderly),
        "chronic_illness_count": float(chronic_illness_count),
        "disability_count": float(disability_count),
        "housing_vulnerability": float(housing_vulnerability),
        "is_undocumented": float(is_undocumented),
        "is_female_headed": float(is_female_headed),
    }


class MLService:
    _instance = None

    def __init__(self):
        self.scaler = None
        self.kmeans = None
        self.clf = None
        self.regressor = None
        self.metadata = {}
        self.load_models()

    @classmethod
    def get_instance(cls) -> "MLService":
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def load_models(self):
        try:
            if (MODELS_DIR / "scaler.joblib").exists():
                self.scaler = joblib.load(MODELS_DIR / "scaler.joblib")
                self.kmeans = joblib.load(MODELS_DIR / "vulnerability_kmeans.joblib")
                self.clf = joblib.load(MODELS_DIR / "needs_random_forest.joblib")
                self.regressor = joblib.load(MODELS_DIR / "demand_regressor.joblib")
                with open(MODELS_DIR / "model_metadata.json", "r", encoding="utf-8") as f:
                    self.metadata = json.load(f)
                logger.info("RASHAD AI: Successfully loaded all ML models and metadata.")
            else:
                logger.warning(f"ML models not found at {MODELS_DIR}. Run train_models.py first.")
        except Exception as e:
            logger.error(f"Error loading ML models: {e}")

    def is_ready(self) -> bool:
        return self.clf is not None and self.kmeans is not None

    def predict(self, household: Household) -> Dict[str, Any]:
        """
        Runs ML inference:
        - Random Forest priority prediction with probabilities
        - K-Means vulnerability cluster archetype
        - Demand forecasting for emergency aid
        - Top local contributing factors
        """
        if not self.is_ready():
            return {
                "status": "UNAVAILABLE",
                "message_ar": "نماذج تعلم الآلة قيد المعايرة أو لم يتم تدريبها بعد."
            }

        features = extract_features_from_household(household)
        df_feat = pd.DataFrame([features])[FEATURE_COLUMNS]

        # 1. Random Forest Classification
        probs = self.clf.predict_proba(df_feat)[0]
        classes = self.clf.classes_
        predicted_tier = self.clf.predict(df_feat)[0]
        prob_dict = {cls_name: round(float(p) * 100, 1) for cls_name, p in zip(classes, probs)}
        confidence = float(np.max(probs))

        # 2. K-Means Clustering (scaled features)
        scaled_feat = self.scaler.transform(df_feat)
        cluster_id = int(self.kmeans.predict(scaled_feat)[0])
        cluster_info = self.metadata.get("clustering", {}).get("clusters", {}).get(str(cluster_id), {}).get("info", {})

        # 3. Demand Forecasting (estimated recommended aid)
        predicted_aid = float(self.regressor.predict(df_feat)[0])

        # 4. Feature Importance ranking
        global_importances = self.metadata.get("classifier", {}).get("feature_importances", {})
        top_factors = []
        for feat_name, imp in list(global_importances.items())[:4]:
            val = features.get(feat_name, 0.0)
            top_factors.append({
                "feature": feat_name,
                "label_ar": FEATURE_LABELS_AR.get(feat_name, feat_name),
                "value": val,
                "importance_pct": round(float(imp) * 100, 1)
            })

        return {
            "status": "AVAILABLE",
            "model_version": self.metadata.get("model_engine", "RASHAD_AI_ML_SUITE_V1.0"),
            "predicted_tier": predicted_tier,
            "confidence_pct": round(confidence * 100, 1),
            "tier_probabilities": prob_dict,
            "cluster": {
                "id": cluster_id,
                "title_ar": cluster_info.get("title_ar", f"عنقود رقم {cluster_id}"),
                "title_en": cluster_info.get("title_en", f"Cluster {cluster_id}"),
                "description": cluster_info.get("description", ""),
                "recommended_intervention": cluster_info.get("recommended_intervention", "")
            },
            "demand_forecast": {
                "estimated_aid_amount_yer": round(predicted_aid, -2),
                "currency": "ريال يمني (YER)"
            },
            "top_contributing_factors": top_factors,
            "extracted_features": features,
            "disclaimer_ar": self.metadata.get("governance_disclaimer", "")
        }

    def get_system_metrics(self) -> Dict[str, Any]:
        """
        Returns full governance and performance metrics of trained ML models.
        """
        return self.metadata


ml_service = MLService.get_instance()
