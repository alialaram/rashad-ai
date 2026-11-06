"""
RASHAD AI - Feature Engineering Pipeline
Extracts multi-dimensional vulnerability and socio-economic features
from household records and family members for Machine Learning models.
"""
import sys
from pathlib import Path
from typing import Dict, Any, List

import numpy as np
import pandas as pd

# Add backend to sys.path
backend_path = Path(__file__).resolve().parent.parent.parent / "backend"
if str(backend_path) not in sys.path:
    sys.path.insert(0, str(backend_path))

from app.core.database import SessionLocal
from app.models.household import Household, HouseholdMember, HousingType, HealthStatus, EmploymentStatus, RelationshipType

HOUSING_WEIGHTS = {
    HousingType.MAKSHA.value: 5.0,
    HousingType.DISPLACED_CAMP.value: 4.5,
    HousingType.SHARED.value: 3.0,
    HousingType.RENTED.value: 2.0,
    HousingType.OWNED.value: 0.5,
}

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


def extract_features_from_household(household: Household) -> Dict[str, float]:
    """
    Extracts a standardized numeric feature vector for a single household.
    """
    members = household.members or []
    num_members = max(1, len(members))
    monthly_income = float(household.monthly_income or 0.0)

    # Earners vs dependents
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

    # Head demographics
    head_member = next((m for m in members if m.relationship == RelationshipType.HEAD), None)
    is_female_headed = 1.0 if (head_member and head_member.gender == "FEMALE") else 0.0

    # Housing vulnerability
    housing_str = household.housing_type.value if hasattr(household.housing_type, "value") else str(household.housing_type)
    housing_vulnerability = HOUSING_WEIGHTS.get(housing_str, 2.0)

    # Documentation status
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


def extract_features_from_dict(h_dict: Dict[str, Any]) -> Dict[str, float]:
    """
    Extracts features from dictionary representation.
    """
    members = h_dict.get("members", [])
    num_members = max(1, len(members) if members else int(h_dict.get("num_members", 1)))
    monthly_income = float(h_dict.get("monthly_income", 0.0))

    earners = sum(1 for m in members if m.get("employment_status") == "EMPLOYED" or m.get("is_employed"))
    num_children = sum(1 for m in members if (m.get("approximate_age") is not None and m.get("approximate_age", 0) < 18) or (m.get("age") is not None and m.get("age", 0) < 18))
    num_elderly = sum(1 for m in members if (m.get("approximate_age") is not None and m.get("approximate_age", 0) >= 60) or (m.get("age") is not None and m.get("age", 0) >= 60))
    chronic_illness_count = sum(1 for m in members if m.get("health_status") == "CHRONIC_DISEASE" or m.get("has_chronic_illness"))
    disability_count = sum(1 for m in members if m.get("health_status") in ("DISABILITY", "SPECIAL_NEEDS") or m.get("disability_type") or m.get("has_disability"))

    dependents = num_children + num_elderly + disability_count
    dependency_ratio = dependents / max(1, num_members)
    income_per_capita = monthly_income / num_members

    head = next((m for m in members if m.get("relationship") == "HEAD"), None)
    is_female = 1.0 if (head and head.get("gender") == "FEMALE") else 0.0

    housing_str = h_dict.get("housing_type", "RENTED")
    housing_vulnerability = HOUSING_WEIGHTS.get(housing_str, 2.0)

    is_undoc = 1.0 if (h_dict.get("is_undocumented") or h_dict.get("id_type") == "TEMPORARY_ID") else 0.0

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
        "is_undocumented": float(is_undoc),
        "is_female_headed": float(is_female),
    }
