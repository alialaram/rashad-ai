import sys
from pathlib import Path

# Ensure UTF-8 output on Windows terminal
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

# Add backend directory to path
backend_path = Path(__file__).resolve().parent.parent.parent / "backend"
sys.path.append(str(backend_path))

from app.core.database import SessionLocal
from app.core.security import get_password_hash
from app.models.user import User, UserRole, UserScope

DEFAULT_USERS = [
    {
        "username": "admin",
        "password": "Admin@2026",
        "full_name": "المهندس مدير النظام التقني",
        "role": UserRole.SYSTEM_ADMIN,
        "scopes": [],
    },
    {
        "username": "researcher_sanaa",
        "password": "Sanaa@2026",
        "full_name": "الأستاذ علي أحمد الباحث الميداني (صنعاء)",
        "role": UserRole.FIELD_RESEARCHER,
        "scopes": ["YE-SA-01", "YE-SN-01"],
    },
    {
        "username": "beneficiary_officer",
        "password": "Register@2026",
        "full_name": "الأستاذة فاطمة موظفة تسجيل المستفيدين",
        "role": UserRole.BENEFICIARY_OFFICER,
        "scopes": ["YE-SA-01", "YE-SA-02", "YE-SA-03", "YE-SA-04"],
    },
    {
        "username": "programs_officer",
        "password": "Officer@2026",
        "full_name": "الأستاذ محمد موظف المصارف والبرامج",
        "role": UserRole.PROGRAMS_OFFICER,
        "scopes": [],
    },
    {
        "username": "auditor",
        "password": "Auditor@2026",
        "full_name": "الأستاذ يحيى المدقق والمراجع الداخلي",
        "role": UserRole.AUDITOR,
        "scopes": [],
    },
    {
        "username": "analyst",
        "password": "Analyst@2026",
        "full_name": "المهندس محلل البيانات والإحصاء",
        "role": UserRole.DATA_ANALYST,
        "scopes": [],
    },
]


def seed_users():
    """بذر الحسابات الافتراضية لكل دور في المنصة"""
    session = SessionLocal()
    try:
        created_count = 0
        for u_data in DEFAULT_USERS:
            user = session.query(User).filter_by(username=u_data["username"]).first()
            if not user:
                user = User(
                    username=u_data["username"],
                    password_hash=get_password_hash(u_data["password"]),
                    full_name=u_data["full_name"],
                    role=u_data["role"],
                    is_active=True,
                )
                session.add(user)
                session.flush()

                for dist_id in u_data["scopes"]:
                    scope = UserScope(
                        user_id=user.id,
                        district_id=dist_id,
                        can_write=True,
                    )
                    session.add(scope)

                created_count += 1

        session.commit()
        print(f"✅ Seeding Complete: {created_count} default institutional users created.")
    except Exception as e:
        session.rollback()
        print(f"❌ Error during users seeding: {e}")
        raise
    finally:
        session.close()


if __name__ == "__main__":
    seed_users()
