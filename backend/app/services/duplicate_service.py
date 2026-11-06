import uuid
import re
from difflib import SequenceMatcher
from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session

from app.models.household import Household, HouseholdStatus
from app.models.duplicate import DuplicateSuspicion, MatchType, ResolutionStatus


class DuplicateDetectionEngine:
    """
    محرك كشف السجلات المتشابهة والمحتمل تكرارها
    Duplicate Detection & Entity Resolution Engine

    المبدأ الرقابي الحاكم:
    رصد وتنبيه اشتباه فقط -- لا يجوز الدمج أو الحذف الآلي دون مراجعة بشرية واعتماد ثنائي.
    """

    @staticmethod
    def normalize_arabic_text(text: str) -> str:
        """توحيد الأشكال الكتابية للحروف العربية لتحسين دقة المطابقة"""
        if not text:
            return ""
        # إزالة التشكيل
        text = re.sub(r"[\u064B-\u0652]", "", text)
        # توحيد الألف
        text = re.sub(r"[إأآا]", "ا", text)
        # توحيد الياء والتاء المربوطة
        text = re.sub(r"ى", "ي", text)
        text = re.sub(r"ة", "ه", text)
        # توحيد المسافات
        text = re.sub(r"\s+", " ", text).strip()
        return text

    @classmethod
    def calculate_name_similarity(cls, name1: str, name2: str) -> float:
        """حساب نسبة التشابه النصي بين اسمين بعد توحيد الحروف"""
        norm1 = cls.normalize_arabic_text(name1)
        norm2 = cls.normalize_arabic_text(name2)
        if norm1 == norm2:
            return 100.0
        matcher = SequenceMatcher(None, norm1, norm2)
        return round(matcher.ratio() * 100, 2)

    @classmethod
    def scan_household_duplicates(cls, db: Session, target_household: Household) -> List[DuplicateSuspicion]:
        """
        فحص ملف أسرة ومقارنته بكافة الأسر النشطة الأخرى لاكتشاف أي تشابه
        """
        suspicions = []

        # استعلام الأسر النشطة الأخرى فقط
        candidates = db.query(Household).filter(
            Household.id != target_household.id,
            Household.status == HouseholdStatus.ACTIVE,
        ).all()

        for candidate in candidates:
            # -------------------------------------------------------------
            # الحالة 1: تطابق دقيق في الرقم الوطني أو رقم الوثيقة (Exact ID)
            # -------------------------------------------------------------
            if (
                target_household.id_number
                and candidate.id_number
                and target_household.id_number.strip() == candidate.id_number.strip()
            ):
                suspicion = DuplicateSuspicion(
                    source_household_id=target_household.id,
                    matched_household_id=candidate.id,
                    match_type=MatchType.EXACT_NATIONAL_ID,
                    similarity_score=100.0,
                    match_details={
                        "matched_field": "id_number",
                        "matched_value": target_household.id_number,
                        "source_name": target_household.head_full_name,
                        "candidate_name": candidate.head_full_name,
                        "reason_ar": "تطابق دقيق برقم الهوية/الوثيقة",
                    },
                    resolution_status=ResolutionStatus.PENDING,
                )
                suspicions.append(suspicion)
                continue  # تم رصد التطابق القطعي، ننتقل للمرشح التالي

            # -------------------------------------------------------------
            # الحالة 2: تطابق دقيق برقم الهاتف (Exact Phone Match)
            # -------------------------------------------------------------
            if (
                target_household.phone_number
                and candidate.phone_number
                and target_household.phone_number.strip() == candidate.phone_number.strip()
            ):
                suspicion = DuplicateSuspicion(
                    source_household_id=target_household.id,
                    matched_household_id=candidate.id,
                    match_type=MatchType.EXACT_PHONE,
                    similarity_score=95.0,
                    match_details={
                        "matched_field": "phone_number",
                        "matched_value": target_household.phone_number,
                        "source_name": target_household.head_full_name,
                        "candidate_name": candidate.head_full_name,
                        "reason_ar": "تطابق دقيق برقم الهاتف المسجل",
                    },
                    resolution_status=ResolutionStatus.PENDING,
                )
                suspicions.append(suspicion)
                continue

            # -------------------------------------------------------------
            # الحالة 3: مطابقة احتمالية بالاسم الرباعي (Fuzzy Name Matching)
            # -------------------------------------------------------------
            name_sim = cls.calculate_name_similarity(
                target_household.head_full_name, candidate.head_full_name
            )

            # إذا كانت نسبة تشابه الاسم >= 85%، نتحقق من الموقع
            if name_sim >= 85.0:
                is_same_village = (target_household.village_id == candidate.village_id)
                final_score = name_sim if not is_same_village else min(name_sim + 5.0, 99.0)

                suspicion = DuplicateSuspicion(
                    source_household_id=target_household.id,
                    matched_household_id=candidate.id,
                    match_type=MatchType.FUZZY_NAME_GEO,
                    similarity_score=final_score,
                    match_details={
                        "matched_field": "head_full_name",
                        "name_similarity_pct": name_sim,
                        "source_name": target_household.head_full_name,
                        "candidate_name": candidate.head_full_name,
                        "same_village": is_same_village,
                        "reason_ar": f"تشابه مرتفع في الاسم بنسبة {name_sim}% مع تقارب جغرافي",
                    },
                    resolution_status=ResolutionStatus.PENDING,
                )
                suspicions.append(suspicion)

        # حفظ التنبيهات المكتشفة في قاعدة البيانات
        if suspicions:
            db.add_all(suspicions)
            db.commit()

        return suspicions

    @classmethod
    def scan_all_database(cls, db: Session) -> Dict[str, Any]:
        """فحص شامل لجميع الأسر في قاعدة البيانات ورصد التكرارات"""
        households = db.query(Household).filter_by(status=HouseholdStatus.ACTIVE).all()
        total_suspicions = 0
        exact_id_count = 0
        exact_phone_count = 0
        fuzzy_count = 0

        # تفريغ حالات الاشتباه السابقة غير المعالجة لتحديث الفحص
        db.query(DuplicateSuspicion).filter_by(resolution_status=ResolutionStatus.PENDING).delete()
        db.commit()

        seen_pairs = set()

        for h in households:
            candidates = db.query(Household).filter(
                Household.id > h.id,  # تجنب التكرار العكسي (A, B) مقابل (B, A)
                Household.status == HouseholdStatus.ACTIVE,
            ).all()

            for cand in candidates:
                pair_key = tuple(sorted([str(h.id), str(cand.id)]))
                if pair_key in seen_pairs:
                    continue

                susp = None
                if h.id_number and cand.id_number and h.id_number.strip() == cand.id_number.strip():
                    susp = DuplicateSuspicion(
                        source_household_id=h.id,
                        matched_household_id=cand.id,
                        match_type=MatchType.EXACT_NATIONAL_ID,
                        similarity_score=100.0,
                        match_details={"source": h.file_number, "candidate": cand.file_number, "reason": "Exact ID match"},
                    )
                    exact_id_count += 1
                elif h.phone_number and cand.phone_number and h.phone_number.strip() == cand.phone_number.strip():
                    susp = DuplicateSuspicion(
                        source_household_id=h.id,
                        matched_household_id=cand.id,
                        match_type=MatchType.EXACT_PHONE,
                        similarity_score=95.0,
                        match_details={"source": h.file_number, "candidate": cand.file_number, "reason": "Exact Phone match"},
                    )
                    exact_phone_count += 1
                else:
                    name_sim = cls.calculate_name_similarity(h.head_full_name, cand.head_full_name)
                    if name_sim >= 85.0:
                        susp = DuplicateSuspicion(
                            source_household_id=h.id,
                            matched_household_id=cand.id,
                            match_type=MatchType.FUZZY_NAME_GEO,
                            similarity_score=name_sim,
                            match_details={"source": h.file_number, "candidate": cand.file_number, "name_sim": name_sim},
                        )
                        fuzzy_count += 1

                if susp:
                    seen_pairs.add(pair_key)
                    db.add(susp)
                    total_suspicions += 1

        db.commit()
        return {
            "total_suspicions": total_suspicions,
            "exact_id_matches": exact_id_count,
            "exact_phone_matches": exact_phone_count,
            "fuzzy_matches": fuzzy_count,
        }
