import uuid
from typing import Dict, Any, List
from sqlalchemy.orm import Session

from app.models.household import Household, HouseholdMember, HousingType, HealthStatus, RelationshipType
from app.models.needs_assessment import NeedsAssessment, PriorityTier


class NeedsAssessmentEngine:
    """
    محرك تقييم الاحتياج الوصفي الشفاف والقابل للتفسير
    Explainable Rule-Based Needs Assessment Engine (Version: RULE_ENGINE_V1.0)
    
    المبدأ: مؤشر تحليلي إحصائي استرشادي لمساندة الباحثين في تحديد أولويات التدخل،
    وليس حكماً شرعياً أو قراراً نهائياً بالاستحقاق.
    """
    VERSION = "RULE_ENGINE_V1.0"
    DISCLAIMER_AR = (
        "مؤشر إحصائي تجريبي استرشادي -- لا يمثل قراراً شرعياً أو قانونياً بالاستحقاق، "
        "وتظل القرارات النهائية بيد اللجان والمختصين وفق اللوائح المعتمدة."
    )

    @classmethod
    def evaluate_household(cls, household: Household, members: List[HouseholdMember]) -> Dict[str, Any]:
        """
        حساب مؤشر الاحتياج للأسر وتوليد تفصيل العوامل المساهمة (Explainability Card)
        """
        factors = {}
        total_score = 0.0

        num_members = max(len(members), 1)

        # ---------------------------------------------------------
        # العامل 1: الدخل ونصيب الفرد الشهري (الحد الأقصى: 30 نقطة)
        # ---------------------------------------------------------
        monthly_income = float(household.monthly_income or 0.0)
        per_capita_income = monthly_income / num_members

        if monthly_income <= 0:
            income_points = 30.0
            income_reason = "انعدام كلي للدخل الشهري المثبت"
        elif per_capita_income < 10000:
            income_points = 25.0
            income_reason = f"دخل الفرد الشهري منخفض جداً ({per_capita_income:,.0f} ريال)"
        elif per_capita_income < 25000:
            income_points = 15.0
            income_reason = f"دخل الفرد الشهري تحت خط الفقر الحرج ({per_capita_income:,.0f} ريال)"
        elif per_capita_income < 50000:
            income_points = 8.0
            income_reason = f"دخل الفرد الشهري محدود ({per_capita_income:,.0f} ريال)"
        else:
            income_points = 2.0
            income_reason = f"دخل الفرد الشهري نسبي ({per_capita_income:,.0f} ريال)"

        total_score += income_points
        factors["income_vulnerability"] = {
            "name_ar": "مستوى الدخل ونصيب الفرد",
            "weight_max": 30,
            "awarded_points": income_points,
            "monthly_income": monthly_income,
            "per_capita_income": round(per_capita_income, 2),
            "reason_ar": income_reason,
        }

        # ---------------------------------------------------------
        # العامل 2: نسبة الإعالة وحجم الأسرة (الحد الأقصى: 25 نقطة)
        # ---------------------------------------------------------
        # المعالون: الأطفال دون سن 18 وكبار السن فوق سن 60 أو العاجزون عن العمل
        dependents = 0
        working_members = 0
        for m in members:
            age = m.approximate_age or 30
            if age < 18 or age >= 60 or m.health_status == HealthStatus.DISABILITY:
                dependents += 1
            elif m.employment_status.value == "EMPLOYED":
                working_members += 1

        dependency_ratio = dependents / num_members

        dependency_points = 0.0
        if dependency_ratio >= 0.8:
            dependency_points += 15.0
        elif dependency_ratio >= 0.5:
            dependency_points += 10.0
        else:
            dependency_points += 5.0

        # نقاط إضافية لكبر حجم الأسرة
        if num_members >= 7:
            dependency_points += 10.0
        elif num_members >= 4:
            dependency_points += 6.0
        else:
            dependency_points += 2.0

        dependency_points = min(dependency_points, 25.0)
        total_score += dependency_points
        factors["dependency_vulnerability"] = {
            "name_ar": "نسبة الإعالة والتركيبة الأسرية",
            "weight_max": 25,
            "awarded_points": dependency_points,
            "total_members": num_members,
            "dependents_count": dependents,
            "dependency_ratio_pct": round(dependency_ratio * 100, 1),
            "reason_ar": f"عدد المعالين {dependents} من أصل {num_members} أفراد بنسبة إعالة {round(dependency_ratio*100)}%",
        }

        # ---------------------------------------------------------
        # العامل 3: الظروف الصحية والإعاقات (الحد الأقصى: 25 نقطة)
        # ---------------------------------------------------------
        health_points = 0.0
        disabled_count = 0
        chronic_count = 0

        for m in members:
            if m.health_status == HealthStatus.DISABILITY or m.disability_type:
                disabled_count += 1
                health_points += 15.0
            elif m.health_status == HealthStatus.CHRONIC_DISEASE:
                chronic_count += 1
                health_points += 8.0

        health_points = min(health_points, 25.0)
        total_score += health_points
        factors["health_vulnerability"] = {
            "name_ar": "الوضع الصحي والاحتياجات الطبية",
            "weight_max": 25,
            "awarded_points": health_points,
            "disabled_count": disabled_count,
            "chronic_disease_count": chronic_count,
            "reason_ar": f"وجود {disabled_count} حالة إعاقة و {chronic_count} حالة أمراض مزمنة بالأسرة",
        }

        # ---------------------------------------------------------
        # العامل 4: المسكن والاستقرار المعيشي (الحد الأقصى: 20 نقطة)
        # ---------------------------------------------------------
        housing_points = 0.0
        housing_map = {
            HousingType.DISPLACED_CAMP: (20.0, "مخيم نزوح / لجوء طارئ"),
            HousingType.MAKSHA: (18.0, "سكن عشوائي / مقشة غير آمنة"),
            HousingType.SHARED: (15.0, "سكن مشترك مع أسر أخرى"),
            HousingType.RENTED: (12.0, "سكن مستأجر يثقل كاهل الأسرة بالالتزامات"),
            HousingType.OWNED: (3.0, "سكن ملك مستقل"),
        }
        pts, h_reason = housing_map.get(household.housing_type, (5.0, "سكن اعتيادي"))
        housing_points = pts
        total_score += housing_points

        factors["housing_vulnerability"] = {
            "name_ar": "طبيعة المسكن والاستقرار",
            "weight_max": 20,
            "awarded_points": housing_points,
            "housing_type": household.housing_type.value,
            "reason_ar": h_reason,
        }

        # تحديد فئة الأولوية
        final_score = round(min(max(total_score, 0.0), 100.0), 2)
        if final_score >= 75.0:
            priority_tier = PriorityTier.CRITICAL
            tier_label_ar = "تدخل طارئ عاجل / أولوية قصوى"
        elif final_score >= 55.0:
            priority_tier = PriorityTier.HIGH
            tier_label_ar = "أولوية مرتفعة"
        elif final_score >= 35.0:
            priority_tier = PriorityTier.MEDIUM
            tier_label_ar = "أولوية متوسطة"
        else:
            priority_tier = PriorityTier.LOW
            tier_label_ar = "أولوية منخفضة / متابعة دورية"

        return {
            "household_id": household.id,
            "calculated_score": final_score,
            "priority_tier": priority_tier,
            "tier_label_ar": tier_label_ar,
            "model_version": cls.VERSION,
            "factors_breakdown": factors,
            "disclaimer_text_ar": cls.DISCLAIMER_AR,
            "disclaimer_acknowledged": True,
        }

    @classmethod
    def evaluate_and_store(cls, db: Session, household_id: uuid.UUID) -> NeedsAssessment:
        """احتساب التقييم وتخزينه في جدول needs_assessments"""
        household = db.query(Household).filter_by(id=household_id).first()
        if not household:
            raise ValueError(f"Household {household_id} not found.")

        result = cls.evaluate_household(household, household.members)

        assessment = NeedsAssessment(
            household_id=household.id,
            calculated_score=result["calculated_score"],
            priority_tier=result["priority_tier"],
            model_version=result["model_version"],
            factors_breakdown=result["factors_breakdown"],
            disclaimer_acknowledged=True,
        )
        db.add(assessment)
        db.commit()
        db.refresh(assessment)
        return assessment
