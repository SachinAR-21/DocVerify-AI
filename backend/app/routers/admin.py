from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.audit import log_action
from app.database import get_db
from app.deps import require_admin
from app.models import Application, AuditLog, Document, DocumentType, User
from app.schemas import (
    AuditLogOut,
    DocumentTypeIn,
    DocumentTypeOut,
    DocumentTypeUpdateIn,
    StatsOut,
    UserCreateIn,
    UserOut,
    UserUpdateIn,
)
from app.security import check_password_policy, hash_password

router = APIRouter(prefix="/api/admin", tags=["admin"])


# ---------- users ----------
@router.get("/users", response_model=list[UserOut])
def list_users(db: Session = Depends(get_db), admin: User = Depends(require_admin)):
    return db.scalars(select(User).order_by(User.id)).all()


@router.post("/users", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def create_user(data: UserCreateIn, db: Session = Depends(get_db), admin: User = Depends(require_admin)):
    error = check_password_policy(data.password)
    if error:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, error)
    if db.scalar(select(User).where(User.email == data.email.lower())):
        raise HTTPException(status.HTTP_409_CONFLICT, "An account with this email already exists")
    user = User(
        email=data.email.lower(),
        full_name=data.full_name.strip(),
        password_hash=hash_password(data.password),
        role=data.role,
    )
    db.add(user)
    db.commit()
    log_action(db, admin.id, "user_created", "user", user.id, f"role={user.role.value}")
    return user


@router.patch("/users/{user_id}", response_model=UserOut)
def update_user(
    user_id: int, data: UserUpdateIn, db: Session = Depends(get_db), admin: User = Depends(require_admin)
):
    user = db.get(User, user_id)
    if user is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "User not found")
    if user.id == admin.id:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "You can not change your own account here")

    changes = []
    if data.role is not None and data.role != user.role:
        changes.append(f"role {user.role.value} -> {data.role.value}")
        user.role = data.role
    if data.is_active is not None and data.is_active != user.is_active:
        changes.append("activated" if data.is_active else "deactivated")
        user.is_active = data.is_active
    if changes:
        log_action(db, admin.id, "user_updated", "user", user.id, ", ".join(changes), commit=False)
    db.commit()
    return user


# ---------- document types ----------
@router.get("/document-types", response_model=list[DocumentTypeOut])
def list_document_types(db: Session = Depends(get_db), admin: User = Depends(require_admin)):
    return db.scalars(select(DocumentType).order_by(DocumentType.id)).all()


@router.post("/document-types", response_model=DocumentTypeOut, status_code=status.HTTP_201_CREATED)
def create_document_type(
    data: DocumentTypeIn, db: Session = Depends(get_db), admin: User = Depends(require_admin)
):
    if db.scalar(select(DocumentType).where(func.lower(DocumentType.name) == data.name.lower())):
        raise HTTPException(status.HTTP_409_CONFLICT, "A document type with this name already exists")
    doc_type = DocumentType(**data.model_dump())
    db.add(doc_type)
    db.commit()
    log_action(db, admin.id, "document_type_created", "document_type", doc_type.id, doc_type.name)
    return doc_type


@router.patch("/document-types/{type_id}", response_model=DocumentTypeOut)
def update_document_type(
    type_id: int,
    data: DocumentTypeUpdateIn,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin),
):
    doc_type = db.get(DocumentType, type_id)
    if doc_type is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Document type not found")
    for field, value in data.model_dump(exclude_none=True).items():
        setattr(doc_type, field, value)
    log_action(
        db, admin.id, "document_type_updated", "document_type", doc_type.id, doc_type.name, commit=False
    )
    db.commit()
    return doc_type


# ---------- audit log and stats ----------
@router.get("/audit-log", response_model=list[AuditLogOut])
def audit_log(
    action: str | None = None,
    limit: int = Query(default=100, ge=1, le=1000),
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin),
):
    query = select(AuditLog).order_by(AuditLog.id.desc()).limit(limit)
    if action:
        query = query.where(AuditLog.action == action)
    return db.scalars(query).all()


@router.get("/stats", response_model=StatsOut)
def stats(db: Session = Depends(get_db), admin: User = Depends(require_admin)):
    users = db.execute(select(User.role, func.count()).group_by(User.role)).all()
    apps = db.execute(select(Application.status, func.count()).group_by(Application.status)).all()
    return StatsOut(
        users_by_role={role.value: count for role, count in users},
        applications_by_status={s.value: count for s, count in apps},
        documents_total=db.scalar(select(func.count()).select_from(Document)) or 0,
    )
