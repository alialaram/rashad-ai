from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api import deps
from app.core.security import verify_password, create_access_token
from app.models.user import User
from app.schemas.token import Token, LoginRequest
from app.schemas.user import UserOut

router = APIRouter()


@router.post("/login", response_model=Token)
def login_for_access_token(
    login_data: LoginRequest,
    db: Session = Depends(deps.get_db),
) -> Token:
    """
    تسجيل الدخول وإصدار رمز الوصول JWT المشفر
    User Login and JWT Generation
    """
    user = db.query(User).filter(User.username == login_data.username).first()
    if not user or not verify_password(login_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="اسم المستخدم أو كلمة المرور غير صحيحة",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="حساب المستخدم معطل",
        )

    scopes = deps.get_user_scopes(user)
    access_token = create_access_token(subject=user.id, role=user.role.value)

    return Token(
        access_token=access_token,
        token_type="bearer",
        role=user.role.value,
        username=user.username,
        full_name=user.full_name,
        scopes=scopes,
    )


@router.get("/me", response_model=UserOut)
def read_current_user(
    current_user: User = Depends(deps.get_current_user),
) -> User:
    """
    استرجاع بيانات الحساب الحالي والصلاحيات والنطاق الجغرافي
    Get Current User Profile & Scopes
    """
    return current_user
