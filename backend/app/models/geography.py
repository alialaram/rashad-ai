import uuid
from typing import List, Optional
from sqlalchemy import String, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID

from app.core.database import Base


class Governorate(Base):
    """المحافظة"""
    __tablename__ = "governorates"

    id: Mapped[str] = mapped_column(String(10), primary_key=True)  # e.g. "YE-SN"
    name_ar: Mapped[str] = mapped_column(String(100), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    districts: Mapped[List["District"]] = relationship("District", back_populates="governorate")


class District(Base):
    """المديرية"""
    __tablename__ = "districts"

    id: Mapped[str] = mapped_column(String(15), primary_key=True)  # e.g. "YE-SN-01"
    governorate_id: Mapped[str] = mapped_column(ForeignKey("governorates.id"), nullable=False, index=True)
    name_ar: Mapped[str] = mapped_column(String(100), nullable=False)

    governorate: Mapped["Governorate"] = relationship("Governorate", back_populates="districts")
    uzlahs: Mapped[List["Uzlah"]] = relationship("Uzlah", back_populates="district")


class Uzlah(Base):
    """العزلة الإدارية"""
    __tablename__ = "uzlahs"

    id: Mapped[str] = mapped_column(String(20), primary_key=True)  # e.g. "YE-SN-01-01"
    district_id: Mapped[str] = mapped_column(ForeignKey("districts.id"), nullable=False, index=True)
    name_ar: Mapped[str] = mapped_column(String(100), nullable=False)

    district: Mapped["District"] = relationship("District", back_populates="uzlahs")
    villages: Mapped[List["Village"]] = relationship("Village", back_populates="uzlah")


class Village(Base):
    """القرية أو الحارة السكنية"""
    __tablename__ = "villages"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    uzlah_id: Mapped[str] = mapped_column(ForeignKey("uzlahs.id"), nullable=False, index=True)
    name_ar: Mapped[str] = mapped_column(String(150), nullable=False)

    uzlah: Mapped["Uzlah"] = relationship("Uzlah", back_populates="villages")
