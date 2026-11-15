from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field

from app.models import ApplicationStatus, DecisionType, DocumentStatus, Role


class ORMModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)


# ---------- users / auth ----------
class RegisterIn(BaseModel):
    email: EmailStr
    full_name: str = Field(min_length=2, max_length=200)
    password: str


class LoginIn(BaseModel):
    email: EmailStr
    password: str


class UserOut(ORMModel):
    id: int
    email: str
    full_name: str
    role: Role
    is_active: bool
    created_at: datetime


class TokenOut(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserOut


class UserCreateIn(RegisterIn):
    role: Role = Role.reviewer


class UserUpdateIn(BaseModel):
    role: Role | None = None
    is_active: bool | None = None


# ---------- document types ----------
class DocumentTypeIn(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    description: str = ""
    is_required: bool = False


class DocumentTypeUpdateIn(BaseModel):
    name: str | None = Field(default=None, min_length=2, max_length=100)
    description: str | None = None
    is_required: bool | None = None
    is_active: bool | None = None


class DocumentTypeOut(ORMModel):
    id: int
    name: str
    description: str
    is_required: bool
    is_active: bool


# ---------- applications ----------
class ApplicationIn(BaseModel):
    programme: str = Field(min_length=2, max_length=200)


class DocumentOut(ORMModel):
    id: int
    document_type: DocumentTypeOut
    original_filename: str
    content_type: str
    size_bytes: int
    notes: str
    status: DocumentStatus
    uploaded_at: datetime


class DecisionOut(ORMModel):
    id: int
    decision: DecisionType
    comment: str
    created_at: datetime
    reviewer: UserOut


class ApplicationOut(ORMModel):
    id: int
    programme: str
    status: ApplicationStatus
    created_at: datetime
    updated_at: datetime
    submitted_at: datetime | None
    applicant: UserOut
    reviewer: UserOut | None
    document_count: int = 0


class ApplicationDetailOut(ApplicationOut):
    documents: list[DocumentOut]
    decisions: list[DecisionOut]
    missing_document_types: list[DocumentTypeOut] = []


class DecisionIn(BaseModel):
    decision: DecisionType
    comment: str = ""


# ---------- admin ----------
class AuditLogOut(ORMModel):
    id: int
    action: str
    entity_type: str
    entity_id: int | None
    details: str
    created_at: datetime
    user: UserOut | None


class StatsOut(BaseModel):
    users_by_role: dict[str, int]
    applications_by_status: dict[str, int]
    documents_total: int
