from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.audit import log_action
from app.config import get_settings
from app.database import get_db
from app.deps import get_current_user
from app.models import Role, User, utcnow
from app.schemas import LoginIn, RegisterIn, TokenOut, UserOut
from app.security import check_password_policy, create_access_token, hash_password, verify_password

router = APIRouter(prefix="/api/auth", tags=["auth"])


@router.post("/register", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def register(data: RegisterIn, db: Session = Depends(get_db)):
    """Self-registration is only for applicants. Staff accounts are created by an admin."""
    error = check_password_policy(data.password)
    if error:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, error)
    email = data.email.lower()
    if db.scalar(select(User).where(User.email == email)):
        raise HTTPException(status.HTTP_409_CONFLICT, "An account with this email already exists")

    user = User(
        email=email,
        full_name=data.full_name.strip(),
        password_hash=hash_password(data.password),
        role=Role.applicant,
    )
    db.add(user)
    db.commit()
    log_action(db, user.id, "user_registered", "user", user.id)
    return user


@router.post("/login", response_model=TokenOut)
def login(data: LoginIn, db: Session = Depends(get_db)):
    settings = get_settings()
    user = db.scalar(select(User).where(User.email == data.email.lower()))
    wrong = HTTPException(status.HTTP_401_UNAUTHORIZED, "Wrong email or password")
    if user is None:
        raise wrong
    if not user.is_active:
        raise HTTPException(status.HTTP_403_FORBIDDEN, "This account is disabled")
    if user.locked_until and user.locked_until > utcnow():
        raise HTTPException(status.HTTP_423_LOCKED, "Too many failed logins. Please try again later.")

    if not verify_password(data.password, user.password_hash):
        user.failed_logins += 1
        if user.failed_logins >= settings.max_failed_logins:
            user.locked_until = utcnow() + timedelta(minutes=settings.lock_minutes)
            user.failed_logins = 0
            log_action(db, user.id, "account_locked", "user", user.id, commit=False)
        db.commit()
        raise wrong

    user.failed_logins = 0
    user.locked_until = None
    log_action(db, user.id, "login", "user", user.id, commit=False)
    db.commit()
    return TokenOut(access_token=create_access_token(user.id, user.role.value), user=user)


@router.get("/me", response_model=UserOut)
def me(user: User = Depends(get_current_user)):
    return user
