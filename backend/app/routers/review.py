from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.audit import log_action
from app.database import get_db
from app.deps import require_staff
from app.models import Application, ApplicationStatus, Decision, DecisionType, User
from app.routers.applications import to_detail, to_out
from app.schemas import ApplicationDetailOut, ApplicationOut, DecisionIn

router = APIRouter(prefix="/api/review", tags=["review"])

OPEN_STATUSES = [ApplicationStatus.submitted, ApplicationStatus.in_review]

DECISION_TO_STATUS = {
    DecisionType.accept: ApplicationStatus.accepted,
    DecisionType.reject: ApplicationStatus.rejected,
    DecisionType.request_documents: ApplicationStatus.needs_documents,
}

SORT_OPTIONS = {
    "oldest": Application.submitted_at.asc(),
    "newest": Application.submitted_at.desc(),
    "programme": Application.programme.asc(),
}


@router.get("/queue", response_model=list[ApplicationOut])
def review_queue(
    status_filter: ApplicationStatus | None = Query(default=None, alias="status"),
    programme: str | None = None,
    mine: bool = False,
    sort: str = "oldest",
    db: Session = Depends(get_db),
    user: User = Depends(require_staff),
):
    """Work queue for reviewers. Without a status filter it shows all open applications."""
    query = select(Application)
    if status_filter:
        query = query.where(Application.status == status_filter)
    else:
        query = query.where(Application.status.in_(OPEN_STATUSES))
    if programme:
        query = query.where(Application.programme.ilike(f"%{programme}%"))
    if mine:
        query = query.where(Application.reviewer_id == user.id)
    query = query.order_by(SORT_OPTIONS.get(sort, SORT_OPTIONS["oldest"]), Application.id)
    return [to_out(a) for a in db.scalars(query).all()]


def get_open_application(db: Session, app_id: int) -> Application:
    app = db.get(Application, app_id)
    if app is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Application not found")
    if app.status not in OPEN_STATUSES:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "This application is not open for review")
    return app


@router.post("/applications/{app_id}/start", response_model=ApplicationDetailOut)
def start_review(app_id: int, db: Session = Depends(get_db), user: User = Depends(require_staff)):
    """Assigns the application to the current reviewer, so others see it is in progress."""
    app = get_open_application(db, app_id)
    if app.reviewer_id and app.reviewer_id != user.id and app.status == ApplicationStatus.in_review:
        raise HTTPException(status.HTTP_409_CONFLICT, f"Already in review by {app.reviewer.full_name}")
    app.reviewer_id = user.id
    app.status = ApplicationStatus.in_review
    log_action(db, user.id, "review_started", "application", app.id, commit=False)
    db.commit()
    return to_detail(db, app)


@router.post("/applications/{app_id}/decision", response_model=ApplicationDetailOut)
def make_decision(
    app_id: int, data: DecisionIn, db: Session = Depends(get_db), user: User = Depends(require_staff)
):
    app = get_open_application(db, app_id)
    comment = data.comment.strip()
    if data.decision != DecisionType.accept and not comment:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Please write a comment for the applicant")

    db.add(Decision(application_id=app.id, reviewer_id=user.id, decision=data.decision, comment=comment))
    app.status = DECISION_TO_STATUS[data.decision]
    app.reviewer_id = user.id
    log_action(db, user.id, f"decision_{data.decision.value}", "application", app.id, comment, commit=False)
    db.commit()
    db.refresh(app)
    return to_detail(db, app)
