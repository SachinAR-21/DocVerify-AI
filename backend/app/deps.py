from fastapi import Depends, HTTPException, Request, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from app.audit import log_action
from app.database import get_db
from app.models import Role, User
from app.security import decode_access_token

bearer = HTTPBearer(auto_error=False)


def get_current_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer),
    db: Session = Depends(get_db),
) -> User:
    if credentials is None:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Not logged in")
    payload = decode_access_token(credentials.credentials)
    if payload is None:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Invalid or expired token")
    user = db.get(User, int(payload["sub"]))
    if user is None or not user.is_active:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "User not found or disabled")
    return user


def require_roles(*roles: Role):
    """Dependency that only lets users with one of the given roles through.
    Denied requests are written to the audit log (US-12)."""

    def checker(
        request: Request,
        user: User = Depends(get_current_user),
        db: Session = Depends(get_db),
    ) -> User:
        if user.role not in roles:
            log_action(db, user.id, "access_denied", details=f"{request.method} {request.url.path}")
            raise HTTPException(status.HTTP_403_FORBIDDEN, "You are not allowed to do this")
        return user

    return checker


require_applicant = require_roles(Role.applicant)
require_staff = require_roles(Role.reviewer, Role.admin)
require_admin = require_roles(Role.admin)
