"""
RASHAD AI - Synthetic Data Generator
مولد البيانات الاصطناعية للأسر والمستفيدين والطلبات في الجمهورية اليمنية

تحذير علمي ومؤسسي:
هذه البيانات اصطناعية مولدة برمجياً 100% لأغراض التطوير والاختبار المعماري والبرمجي.
لا ترتبط بأي أشخاص حقيقيين، ولا تمثل بيانات الهيئة العامة للزكاة.
"""

import sys
import random
import uuid
import json
from datetime import date, timedelta
from pathlib import Path
from typing import List, Dict, Any

# Ensure UTF-8 output on Windows terminal
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

# Add backend directory to path
backend_path = Path(__file__).resolve().parent.parent.parent / "backend"
sys.path.append(str(backend_path))

from app.core.database import SessionLocal
from app.models.geography import Village, Uzlah, District, Governorate
from app.models.household import (
    Household,
    HouseholdMember,
    IdType,
    IdVerificationStatus,
    HousingType,
    HouseholdStatus,
    RelationshipType,
    HealthStatus,
    EmploymentStatus,
)
from app.models.request import AssistanceRequest, ProgramType, RequestStatus

# Arabic First and Family Names common in Yemen for realistic generation
MALE_FIRST_NAMES = [
    "محمد", "أحمد", "علي", "عبدالله", "يحيى", "حسين", "صالح", "إبراهيم", "عمر", "خالد",
    "عبدالرحمن", "ناصر", "منصور", "فواد", "جميل", "ماجد", "توفيق", "سلطان", "وليد", "صقر"
]

FEMALE_FIRST_NAMES = [
    "فاطمة", "مريم", "زينب", "عائشة", "أمل", "سارة", "بلقيس", "ياسمين", "منى", "سميرة",
    "نجاة", "وفاء", "هدى", "ذكرى", "سمية", "روان", "أروى", "رحمة", "إشراق", "أماني"
]

FAMILY_NAMES = [
    "الهمداني", "الصنعاني", "الزبيدي", "الأنسي", "الذماري", "الحيدري", "العدني", "التعزي",
    "الحكيمي", "الرازحي", "المتوكل", "الشامي", "المروني", "الشرعبي", "الحديدي", "الوائلي",
    "الريمي", "الجوفي", "البيضاني", "الحاشدي", "البكاري", "السعدي", "المخلافي", "القدسي"
]

CHRONIC_DISEASES = [
    "الفشل الكلوي", "السكري المزمن", "ارتفاع ضغط الدم", "أمراض القلب", "الربو الحاد", "التهاب المفاصل الروماتويدي"
]

DISABILITY_TYPES = [
    "إعاقة حركية (شلل سفلي)", "إعاقة بصرية كف بصري", "إعاقة سمعية ونطقية", "إعاقة ذهنية متوسطة", "بتر طرف سفلي"
]

COMMUNITY_SOURCES = [
    "عاقل حارة القاع: الشيخ يحيى محمد الضبيبي - تلفون: 771234501",
    "رئيس اللجنة المجتمعية بحي السنينة: الأستاذ عبدالله الصليحي - تلفون: 772345602",
    "عاقل قرية بيت حاضر: الشيخ صالح أحمد الأجبار - تلفون: 773456703",
    "منسق الإغاثة بمديرية صيرة: الشيخ علي منصور العدني - تلفون: 774567804",
    "عاقل حارة النسيم بالمظفر: الأستاذ محمد عبدالجليل - تلفون: 775678905",
]


class SyntheticDataGenerator:
    def __init__(self, seed: int = 42):
        self.seed = seed
        random.seed(seed)
        self.session = SessionLocal()
        self.villages = self.session.query(Village).all()
        if not self.villages:
            raise ValueError("No villages found in database! Please run database/seeds/seed_geography.py first.")

    def close(self):
        self.session.close()

    def generate_arabic_name(self, gender: str = "MALE") -> str:
        first = random.choice(MALE_FIRST_NAMES) if gender == "MALE" else random.choice(FEMALE_FIRST_NAMES)
        father = random.choice(MALE_FIRST_NAMES)
        grandfather = random.choice(MALE_FIRST_NAMES)
        family = random.choice(FAMILY_NAMES)
        return f"{first} {father} {grandfather} {family}"

    def generate_national_id(self) -> str:
        # Standard 11-digit synthetic format starting with 01
        return f"01{random.randint(100000000, 999999999)}"

    def generate_temporary_id(self, gov_code: str, index: int) -> str:
        # Structured temporary identifier
        return f"TMP-{gov_code}-2026-{index:05d}"

    def generate_dataset(self, num_households: int = 150) -> Dict[str, Any]:
        """
        توليد عينة أسر متنوعة تشمل كافة الحالات الميدانية وحالات الاختبار
        """
        print(f"Generating {num_households} synthetic households (Seed={self.seed})...")
        generated_records = []

        # We will deliberately reserve specific indices for intentional duplicate testing
        # Record 10 will duplicate Record 0's national ID
        # Record 20 will duplicate Record 1's phone number
        # Record 30 will duplicate Record 2's name and approximate age (Fuzzy duplicate)
        
        for i in range(num_households):
            village = random.choice(self.villages)
            uzlah = self.session.query(Uzlah).filter_by(id=village.uzlah_id).first()
            district = self.session.query(District).filter_by(id=uzlah.district_id).first()
            gov = self.session.query(Governorate).filter_by(id=district.governorate_id).first()

            file_number = f"SYN-RSH-2026-{i+1:05d}"
            pseudo_id = f"ANON-YE-{(i+1)*17 % 99999:05d}"

            # 20% of cases are undocumented (Temporary ID) to test the missing-documents flow
            is_undocumented = (i % 5 == 0)

            if is_undocumented:
                id_type = IdType.TEMPORARY_ID
                id_number = self.generate_temporary_id(gov.id, i + 1)
                verification_status = IdVerificationStatus.LOCAL_ATTESTATION
                attestation_source = random.choice(COMMUNITY_SOURCES)
            else:
                id_type = IdType.NATIONAL_ID
                id_number = self.generate_national_id()
                verification_status = IdVerificationStatus.VERIFIED_OFFICIAL
                attestation_source = None

            # Test Case Injections (Duplicates for detection validation)
            if i == 10 and len(generated_records) > 0:
                # Exact National ID Duplicate
                id_type = IdType.NATIONAL_ID
                id_number = generated_records[0]["id_number"]
            elif i == 20 and len(generated_records) > 1:
                # Duplicate Phone Number
                phone_number = generated_records[1]["phone_number"]
            else:
                phone_number = f"77{random.randint(1000000, 9999999)}"

            # Head of Household
            gender = "FEMALE" if random.random() < 0.25 else "MALE"  # 25% female-headed (widows/orphans)
            
            if i == 30 and len(generated_records) > 2:
                # Fuzzy duplicate name
                head_full_name = generated_records[2]["head_full_name"]
            else:
                head_full_name = self.generate_arabic_name(gender)

            # Socioeconomic profile
            housing_type = random.choices(
                [HousingType.RENTED, HousingType.DISPLACED_CAMP, HousingType.OWNED, HousingType.SHARED, HousingType.MAKSHA],
                weights=[0.45, 0.25, 0.15, 0.10, 0.05],
            )[0]

            # Income: 35% zero income, 45% ultra-low (20,000 - 60,000 YER), 20% low (60,000 - 120,000 YER)
            income_category = random.choices(["ZERO", "ULTRA_LOW", "LOW"], weights=[0.35, 0.45, 0.20])[0]
            if income_category == "ZERO":
                monthly_income = 0.0
            elif income_category == "ULTRA_LOW":
                monthly_income = round(random.uniform(20000, 60000), -3)
            else:
                monthly_income = round(random.uniform(60000, 120000), -3)

            # Create Household DB Record
            household = Household(
                file_number=file_number,
                pseudo_id=pseudo_id,
                head_full_name=head_full_name,
                id_type=id_type,
                id_number=id_number,
                id_verification_status=verification_status,
                attestation_source=attestation_source,
                phone_number=phone_number,
                village_id=village.id,
                address_details=f"{gov.name_ar} - {district.name_ar} - {uzlah.name_ar} - {village.name_ar} (بيانات اصطناعية تجريبية)",
                housing_type=housing_type,
                monthly_income=monthly_income,
                status=HouseholdStatus.ACTIVE,
            )
            self.session.add(household)
            self.session.flush()

            # Create Household Members (Family structure: 2 to 8 members)
            num_members = random.randint(2, 8)
            members_data = []

            # Add Head of household as member
            head_member = HouseholdMember(
                household_id=household.id,
                full_name=head_full_name,
                relationship=RelationshipType.HEAD,
                gender=gender,
                approximate_age=random.randint(28, 70),
                health_status=HealthStatus.HEALTHY if random.random() > 0.3 else HealthStatus.CHRONIC_DISEASE,
                disability_type=random.choice(DISABILITY_TYPES) if random.random() < 0.08 else None,
                employment_status=EmploymentStatus.UNEMPLOYED if monthly_income == 0 else EmploymentStatus.EMPLOYED,
            )
            self.session.add(head_member)
            members_data.append({"name": head_full_name, "rel": "HEAD", "gender": gender})

            # Add other family members
            for m in range(num_members - 1):
                m_gender = "MALE" if random.random() < 0.5 else "FEMALE"
                rel = random.choices(
                    [RelationshipType.WIFE, RelationshipType.SON, RelationshipType.DAUGHTER, RelationshipType.PARENT],
                    weights=[0.25, 0.35, 0.35, 0.05],
                )[0]

                # Special condition: Chronic diseases or disabilities
                has_chronic = random.random() < 0.15
                has_disability = random.random() < 0.07

                m_name = self.generate_arabic_name(m_gender)
                member = HouseholdMember(
                    household_id=household.id,
                    full_name=m_name,
                    relationship=rel,
                    gender=m_gender,
                    approximate_age=random.randint(1, 22) if rel in [RelationshipType.SON, RelationshipType.DAUGHTER] else random.randint(20, 65),
                    health_status=HealthStatus.DISABILITY if has_disability else (HealthStatus.CHRONIC_DISEASE if has_chronic else HealthStatus.HEALTHY),
                    disability_type=random.choice(DISABILITY_TYPES) if has_disability else None,
                    employment_status=EmploymentStatus.UNEMPLOYED,
                )
                self.session.add(member)
                members_data.append({"name": m_name, "rel": rel.value, "gender": m_gender})

            # Add an initial assistance request for each household
            program_type = random.choices(
                [ProgramType.POOR_AND_NEEDY, ProgramType.MEDICAL_AID, ProgramType.DISASTER_RELIEF],
                weights=[0.70, 0.20, 0.10],
            )[0]
            request = AssistanceRequest(
                request_number=f"REQ-SYN-2026-{i+1:05d}",
                household_id=household.id,
                program_type=program_type,
                current_status=RequestStatus.SUBMITTED,
                requested_amount=100000.0,
            )
            self.session.add(request)

            generated_records.append({
                "file_number": file_number,
                "pseudo_id": pseudo_id,
                "head_full_name": head_full_name,
                "id_type": id_type.value,
                "id_number": id_number,
                "phone_number": phone_number,
                "governorate": gov.name_ar,
                "district": district.name_ar,
                "village": village.name_ar,
                "housing_type": housing_type.value,
                "monthly_income": monthly_income,
                "num_members": num_members,
                "is_undocumented": is_undocumented,
                "is_synthetic": True,
            })

        self.session.commit()
        print(f"Successfully committed {len(generated_records)} synthetic households to PostgreSQL database!")

        # Save synthetic dataset to ai/data/synthetic/synthetic_households_v1.json
        output_file = Path(__file__).resolve().parent.parent / "data" / "synthetic" / "synthetic_households_v1.json"
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(
                {
                    "metadata": {
                        "generated_at": str(date.today()),
                        "seed": self.seed,
                        "total_households": len(generated_records),
                        "description": "Synthetic dataset for testing RASHAD AI needs assessment, duplicate resolution, and reporting.",
                        "license_notice": "SYNTHETIC GENERATED TEST DATA ONLY - DO NOT USE FOR REAL BENEFICIARY DECISIONS",
                    },
                    "records": generated_records,
                },
                f,
                ensure_ascii=False,
                indent=2,
            )
        print(f"Exported JSON dataset to: {output_file}")
        return {"count": len(generated_records), "output_file": str(output_file)}


if __name__ == "__main__":
    generator = SyntheticDataGenerator(seed=42)
    try:
        generator.generate_dataset(num_households=150)
    finally:
        generator.close()
