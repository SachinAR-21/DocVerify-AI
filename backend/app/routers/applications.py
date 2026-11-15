from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.audit import log_action
from app.database import get_db
from app.deps import get_current_user, require_applicant
from app.models import Application, ApplicationStatus, DocumentType, Role, User, utcnow
from app.schemas import ApplicationDetailOut, ApplicationIn, ApplicationOut, DocumentTypeOut

router = APIRouter(prefix="/api", tags=["applications"])

# applicants can only change an application in these states
EDITABLE = {ApplicationStatus.draft, ApplicationStatus.needs_documents}


def missing_required_types(db: Session, app: Application) -> list[DocumentType]:
    uploaded = {d.document_type_id for d in app.documents}
    required = db.scalars(select(DocumentType).where(DocumentType.is_required, DocumentType.is_active)).all()
    return [t for t in required if t.id not in uploaded]


def to_out(app: Application) -> ApplicationOut:
    out = ApplicationOut.model_validate(app)
    out.document_count = len(app.documents)
    return out


def to_detail(db: Session, app: Application) -> ApplicationDetailOut:
    out = ApplicationDetailOut.model_validate(app)
    out.document_count = len(app.documents)
    out.missing_document_types = [DocumentTypeOut.model_validate(t) for t in missing_required_types(db, app)]
    return out


def get_application_for_user(db: Session, app_id: int, user: User) -> Application:
    """Loads an application and checks that the user is allowed to see it."""
    app = db.get(Application, app_id)
    if app is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Application not found")
    if user.role == Role.applicant and app.applicant_id != user.id:
        log_action(db, user.id, "access_denied", "application", app_id)
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Application not found")
    return app


@router.get("/document-types", response_model=list[DocumentTypeOut])
def list_active_document_types(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    return db.scalars(select(DocumentType).where(DocumentType.is_active).order_by(DocumentType.id)).all()


@router.post("/applications", response_model=ApplicationOut, status_code=status.HTTP_201_CREATED)
def create_application(
    data: ApplicationIn, db: Session = Depends(get_db), user: User = Depends(require_applicant)
):
    app = Application(applicant_id=user.id, programme=data.programme.strip())
    db.add(app)
    db.commit()
    db.refresh(app)
    log_action(db, user.id, "application_created", "application", app.id)
    return to_out(app)


@router.get("/applications", response_model=list[ApplicationOut])
def list_applications(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    query = select(Application).order_by(Application.created_at.desc())
    if user.role == Role.applicant:
        query = query.where(Application.applicant_id == user.id)
    return [to_out(a) for a in db.scalars(query).all()]


@router.get("/applications/{app_id}", response_model=ApplicationDetailOut)
def get_application(app_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    app = get_application_for_user(db, app_id, user)
    return to_detail(db, app)


@router.post("/applications/{app_id}/submit", response_model=ApplicationDetailOut)
def submit_application(app_id: int, db: Session = Depends(get_db), user: User = Depends(require_applicant)):
    app = get_application_for_user(db, app_id, user)
    if app.status not in EDITABLE:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "This application was already submitted")
    missing = missing_required_types(db, app)
    if missing:
        names = ", ".join(t.name for t in missing)
        raise HTTPException(status.HTTP_400_BAD_REQUEST, f"Missing required documents: {names}")

    app.status = ApplicationStatus.submitted
    app.submitted_at = utcnow()
    log_action(db, user.id, "application_submitted", "application", app.id, commit=False)
    db.commit()
    return to_detail(db, app)
