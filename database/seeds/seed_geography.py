import sys
from pathlib import Path

# Ensure UTF-8 output on Windows terminal
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

# Add backend directory to path so models can be imported
backend_path = Path(__file__).resolve().parent.parent.parent / "backend"
sys.path.append(str(backend_path))

from app.core.database import SessionLocal, engine, Base
from app.models.geography import Governorate, District, Uzlah, Village

# Comprehensive official geographic seed data for Yemen
YEMEN_GEOGRAPHY = [
    {
        "id": "YE-SA",
        "name_ar": "أمانة العاصمة",
        "districts": [
            {
                "id": "YE-SA-01",
                "name_ar": "مديرية التحرير",
                "uzlahs": [
                    {
                        "id": "YE-SA-01-01",
                        "name_ar": "عزلة التحرير",
                        "villages": ["حي علي عبدالمغني", "حي القاع", "حي الزراعة", "حي بئر العزب"],
                    }
                ],
            },
            {
                "id": "YE-SA-02",
                "name_ar": "مديرية السبعين",
                "uzlahs": [
                    {
                        "id": "YE-SA-02-01",
                        "name_ar": "عزلة السبعين",
                        "villages": ["حي بيت بوس", "حي حدة", "حي الأصبحي", "حي القادسية"],
                    }
                ],
            },
            {
                "id": "YE-SA-03",
                "name_ar": "مديرية معين",
                "uzlahs": [
                    {
                        "id": "YE-SA-03-01",
                        "name_ar": "عزلة معين",
                        "villages": ["حي الدائري الغربي", "حي هائل", "حي مذبح", "حي السنينة"],
                    }
                ],
            },
            {
                "id": "YE-SA-04",
                "name_ar": "مديرية الثورة",
                "uzlahs": [
                    {
                        "id": "YE-SA-04-01",
                        "name_ar": "عزلة الثورة",
                        "villages": ["حي الجراف الغربي", "حي الحصبة", "حي التلفزيون", "حي النهضة"],
                    }
                ],
            },
        ],
    },
    {
        "id": "YE-SN",
        "name_ar": "محافظة صنعاء",
        "districts": [
            {
                "id": "YE-SN-01",
                "name_ar": "مديرية سنحان وبني بهلول",
                "uzlahs": [
                    {
                        "id": "YE-SN-01-01",
                        "name_ar": "عزلة وادي الأجبار",
                        "villages": ["قرية بيت حاضر", "قرية دار الحيد", "قرية ريمة حميد"],
                    },
                    {
                        "id": "YE-SN-01-02",
                        "name_ar": "عزلة الربع الشرقي",
                        "villages": ["قرية مقولة", "قرية قاع القيضي", "قرية حزيز"],
                    },
                ],
            },
            {
                "id": "YE-SN-02",
                "name_ar": "مديرية همدان",
                "uzlahs": [
                    {
                        "id": "YE-SN-02-01",
                        "name_ar": "عزلة وادعة",
                        "villages": ["قرية ضلاع همدان", "قرية الجاهلية", "قرية حاز"],
                    }
                ],
            },
        ],
    },
    {
        "id": "YE-AD",
        "name_ar": "محافظة عدن",
        "districts": [
            {
                "id": "YE-AD-01",
                "name_ar": "مديرية صيرة (كريتر)",
                "uzlahs": [
                    {
                        "id": "YE-AD-01-01",
                        "name_ar": "عزلة كريتر القديمة",
                        "villages": ["حي الميدان", "حي الخساف", "حي شعب العيدروس"],
                    }
                ],
            },
            {
                "id": "YE-AD-02",
                "name_ar": "مديرية الشيخ عثمان",
                "uzlahs": [
                    {
                        "id": "YE-AD-02-01",
                        "name_ar": "عزلة الشيخ عثمان",
                        "villages": ["حي السيلة", "حي الممدارة", "حي كود عثمان"],
                    }
                ],
            },
        ],
    },
    {
        "id": "YE-TA",
        "name_ar": "محافظة تعز",
        "districts": [
            {
                "id": "YE-TA-01",
                "name_ar": "مديرية المظفر",
                "uzlahs": [
                    {
                        "id": "YE-TA-01-01",
                        "name_ar": "عزلة المظفر",
                        "villages": ["حي النسيم", "حي الحصب", "حي المناخ"],
                    }
                ],
            },
            {
                "id": "YE-TA-02",
                "name_ar": "مديرية القاهرة",
                "uzlahs": [
                    {
                        "id": "YE-TA-02-01",
                        "name_ar": "عزلة القاهرة",
                        "villages": ["حي المسبح", "حي كلابة", "حي ديلوكس"],
                    }
                ],
            },
        ],
    },
    {
        "id": "YE-HD",
        "name_ar": "محافظة الحديدة",
        "districts": [
            {
                "id": "YE-HD-01",
                "name_ar": "مديرية الحوك",
                "uzlahs": [
                    {
                        "id": "YE-HD-01-01",
                        "name_ar": "عزلة الحوك",
                        "villages": ["حي غليل", "حي الربصة", "حي الكورنيش"],
                    }
                ],
            },
            {
                "id": "YE-HD-02",
                "name_ar": "مديرية بيت الفقيه",
                "uzlahs": [
                    {
                        "id": "YE-HD-02-01",
                        "name_ar": "عزلة بني محمد",
                        "villages": ["قرية التحيتا الشرقية", "قرية المشاريح", "قرية الجروبة"],
                    }
                ],
            },
        ],
    },
]


def seed_geography():
    """بذر البيانات الجغرافية الرسمية في قاعدة البيانات"""
    Base.metadata.create_all(bind=engine)
    session = SessionLocal()

    gov_count = 0
    dist_count = 0
    uzlah_count = 0
    village_count = 0

    try:
        for gov_data in YEMEN_GEOGRAPHY:
            gov = session.query(Governorate).filter_by(id=gov_data["id"]).first()
            if not gov:
                gov = Governorate(id=gov_data["id"], name_ar=gov_data["name_ar"])
                session.add(gov)
                session.flush()
                gov_count += 1

            for dist_data in gov_data["districts"]:
                dist = session.query(District).filter_by(id=dist_data["id"]).first()
                if not dist:
                    dist = District(
                        id=dist_data["id"],
                        governorate_id=gov.id,
                        name_ar=dist_data["name_ar"],
                    )
                    session.add(dist)
                    session.flush()
                    dist_count += 1

                for uzlah_data in dist_data["uzlahs"]:
                    uzlah = session.query(Uzlah).filter_by(id=uzlah_data["id"]).first()
                    if not uzlah:
                        uzlah = Uzlah(
                            id=uzlah_data["id"],
                            district_id=dist.id,
                            name_ar=uzlah_data["name_ar"],
                        )
                        session.add(uzlah)
                        session.flush()
                        uzlah_count += 1

                    for village_name in uzlah_data["villages"]:
                        village = session.query(Village).filter_by(uzlah_id=uzlah.id, name_ar=village_name).first()
                        if not village:
                            village = Village(
                                uzlah_id=uzlah.id,
                                name_ar=village_name,
                            )
                            session.add(village)
                            village_count += 1

        session.commit()
        print(f"✅ Seeding Complete: {gov_count} Governorates, {dist_count} Districts, {uzlah_count} Uzlahs, {village_count} Villages.")
    except Exception as e:
        session.rollback()
        print(f"❌ Error during geography seeding: {e}")
        raise
    finally:
        session.close()


if __name__ == "__main__":
    seed_geography()
