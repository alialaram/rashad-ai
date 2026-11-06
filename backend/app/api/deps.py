import uuid
from typing import Generator, List, Callable
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
import jwt
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.database import get_db
from app.models.user import User, UserRole, UserScope
from app.schemas.token import TokenPayload

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_STR}/auth/login")


def get_current_user(
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme),
) -> User:
    """استخراج المستخدم الحالي من رمز JWT والتحقق من صحته"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="تعذر التحقق من هوية المستخدم أو انتهت صلاحية الجلسة",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
        token_data = TokenPayload(sub=user_id, role=payload.get("role"))
    except jwt.PyJWTError:
        raise credentials_exception

    user = db.query(User).filter(User.id == uuid.UUID(token_data.sub)).first()
    if user is None:
        raise credentials_exception
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="حساب المستخدم معطل حالياً",
        )
    return user


def require_role(allowed_roles: List[UserRole]) -> Callable:
    """التحقق الصارم من صلاحية الدور (Role-Based Access Control)"""
    def role_checker(current_user: User = Depends(get_current_user)) -> User:
        if current_user.role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"غير مصرح لهذا الدور ({current_user.role.value}) بتنفيذ هذا الإجراء",
            )
        return current_user
    return role_checker


def get_user_scopes(user: User) -> List[str]:
    """استرجاع معرفات المديريات المصرح بها للمستخدم"""
    return [s.district_id for s in user.scopes]
