import uuid
from pathlib import Path

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile, status
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from app.audit import log_action
from app.config import get_settings
from app.database import get_db
from app.deps import get_current_user, require_applicant
from app.models import Document, DocumentType, Role, User
from app.routers.applications import EDITABLE, get_application_for_user
from app.schemas import DocumentOut

router = APIRouter(prefix="/api", tags=["documents"])

# extension -> (content type, first bytes of a valid file)
ALLOWED_FILES = {
    ".pdf": ("application/pdf", [b"%PDF"]),
    ".png": ("image/png", [b"\x89PNG\r\n\x1a\n"]),
    ".jpg": ("image/jpeg", [b"\xff\xd8\xff"]),
    ".jpeg": ("image/jpeg", [b"\xff\xd8\xff"]),
}


def upload_dir() -> Path:
    path = Path(get_settings().upload_dir)
    path.mkdir(parents=True, exist_ok=True)
    return path


@router.post(
    "/applications/{app_id}/documents",
    response_model=DocumentOut,
    status_code=status.HTTP_201_CREATED,
)
async def upload_document(
    app_id: int,
    document_type_id: int = Form(...),
    notes: str = Form(""),
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    user: User = Depends(require_applicant),
):
    app = get_application_for_user(db, app_id, user)
    if app.status not in EDITABLE:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Documents can not be changed right now")

    doc_type = db.get(DocumentType, document_type_id)
    if doc_type is None or not doc_type.is_active:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Unknown document type")

    filename = file.filename or "upload"
    ext = Path(filename).suffix.lower()
    if ext not in ALLOWED_FILES:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Only PDF, JPG and PNG files are allowed")

    max_bytes = get_settings().max_upload_mb * 1024 * 1024
    content = await file.read(max_bytes + 1)
    if len(content) == 0:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "The file is empty")
    if len(content) > max_bytes:
        raise HTTPException(
            status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            f"File is too big (max {get_settings().max_upload_mb} MB)",
        )

    content_type, signatures = ALLOWED_FILES[ext]
    if not any(content.startswith(sig) for sig in signatures):
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST, "The file seems to be damaged or is not a real " + ext[1:].upper()
        )

    stored_name = f"{uuid.uuid4().hex}{ext}"
    (upload_dir() / stored_name).write_bytes(content)

    doc = Document(
        application_id=app.id,
        document_type_id=doc_type.id,
        original_filename=filename[:255],
        stored_filename=stored_name,
        content_type=content_type,
        size_bytes=len(content),
        notes=notes.strip(),
    )
    db.add(doc)
    db.commit()
    db.refresh(doc)
    log_action(db, user.id, "document_uploaded", "document", doc.id, f"{doc_type.name}: {filename}")
    return doc


@router.delete("/documents/{doc_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_document(doc_id: int, db: Session = Depends(get_db), user: User = Depends(require_applicant)):
    doc = db.get(Document, doc_id)
    if doc is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Document not found")
    app = get_application_for_user(db, doc.application_id, user)
    if app.status not in EDITABLE:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Documents can not be changed right now")

    (upload_dir() / doc.stored_filename).unlink(missing_ok=True)
    db.delete(doc)
    log_action(db, user.id, "document_deleted", "document", doc_id, doc.original_filename, commit=False)
    db.commit()


@router.get("/documents/{doc_id}/file")
def download_document(doc_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    doc = db.get(Document, doc_id)
    if doc is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Document not found")
    get_application_for_user(db, doc.application_id, user)  # permission check

    path = upload_dir() / doc.stored_filename
    if not path.exists():
        raise HTTPException(status.HTTP_404_NOT_FOUND, "File is missing on the server")
    if user.role != Role.applicant:
        log_action(db, user.id, "document_viewed", "document", doc.id)
    return FileResponse(path, media_type=doc.content_type, filename=doc.original_filename)
