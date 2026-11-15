from sqlalchemy import select
from sqlalchemy.orm import Session

from app.config import get_settings
from app.models import DocumentType, Role, User
from app.security import hash_password

DEFAULT_DOCUMENT_TYPES = [
    ("Degree certificate", "Bachelor or other university degree certificate", True),
    ("Transcript of records", "Grades, ECTS and GPA", True),
    ("Language certificate", "IELTS, TOEFL, TestDaF, Goethe, ...", True),
    ("Passport / ID card", "Use sample or test data only", True),
    ("CV", "Curriculum vitae", False),
    ("Other", "Any other supporting document", False),
]


def _ensure_user(db: Session, email: str, password: str, name: str, role: Role) -> None:
    if not email or not password:
        return
    if db.scalar(select(User).where(User.email == email.lower())):
        return
    db.add(User(email=email.lower(), full_name=name, password_hash=hash_password(password), role=role))


def seed(db: Session) -> None:
    """Creates the first admin, an optional demo reviewer and the default document types."""
    settings = get_settings()
    _ensure_user(db, settings.admin_email, settings.admin_password, "Administrator", Role.admin)
    _ensure_user(db, settings.reviewer_email, settings.reviewer_password, "Demo Reviewer", Role.reviewer)

    if db.scalar(select(DocumentType).limit(1)) is None:
        for name, description, required in DEFAULT_DOCUMENT_TYPES:
            db.add(DocumentType(name=name, description=description, is_required=required))
    db.commit()
