from sqlalchemy.orm import Session

from app.models import AuditLog


def log_action(
    db: Session,
    user_id: int | None,
    action: str,
    entity_type: str = "",
    entity_id: int | None = None,
    details: str = "",
    commit: bool = True,
) -> None:
    """Writes one entry to the audit log (who did what and when)."""
    db.add(
        AuditLog(
            user_id=user_id,
            action=action,
            entity_type=entity_type,
            entity_id=entity_id,
            details=details,
        )
    )
    if commit:
        db.commit()
