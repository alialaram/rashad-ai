import enum
import uuid
from typing import List, Optional
from sqlalchemy import String, Boolean, Enum, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID

from app.core.database import BaseModel


class UserRole(str, enum.Enum):
    SYSTEM_ADMIN = "SYSTEM_ADMIN"
    FIELD_RESEARCHER = "FIELD_RESEARCHER"
    BENEFICIARY_OFFICER = "BENEFICIARY_OFFICER"
    PROGRAMS_OFFICER = "PROGRAMS_OFFICER"
    DATA_ANALYST = "DATA_ANALYST"
    AUDITOR = "AUDITOR"
    MANAGER = "MANAGER"


class User(BaseModel):
    """جدول حسابات المستخدمين والموظفين"""
    __tablename__ = "users"

    username: Mapped[str] = mapped_column(String(50), unique=True, index=True, nullable=False)
    full_name: Mapped[str] = mapped_column(String(150), nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[UserRole] = mapped_column(
        Enum(UserRole, name="user_role_enum", native_enum=False),
        nullable=False,
        default=UserRole.FIELD_RESEARCHER,
    )
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    scopes: Mapped[List["UserScope"]] = relationship("UserScope", back_populates="user", cascade="all, delete-orphan")


class UserScope(BaseModel):
    """النطاق الجغرافي المصرح به للمستخدم"""
    __tablename__ = "user_scopes"

    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    district_id: Mapped[str] = mapped_column(ForeignKey("districts.id"), nullable=False, index=True)
    can_write: Mapped[bool] = mapped_column(Boolean, default=True)

    user: Mapped["User"] = relationship("User", back_populates="scopes")
