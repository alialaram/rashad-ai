import uuid
from typing import Optional, List
from pydantic import BaseModel
from app.models.user import UserRole


class UserScopeOut(BaseModel):
    district_id: str
    can_write: bool

    class Config:
        from_attributes = True


class UserOut(BaseModel):
    id: uuid.UUID
    username: str
    full_name: str
    role: UserRole
    is_active: bool
    scopes: List[UserScopeOut] = []

    class Config:
        from_attributes = True


class UserCreate(BaseModel):
    username: str
    full_name: str
    password: str
    role: UserRole
    district_ids: List[str] = []
