import httpx
from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.config import get_settings
from app.database import get_db

router = APIRouter(prefix="/api", tags=["health"])


@router.get("/health")
def health(db: Session = Depends(get_db)):
    """Checks that the backend can reach the database and the vector database."""
    try:
        db.execute(text("SELECT 1"))
        database = "ok"
    except Exception:
        database = "unavailable"

    try:
        response = httpx.get(f"{get_settings().qdrant_url}/readyz", timeout=2)
        vector_db = "ok" if response.status_code == 200 else "unavailable"
    except httpx.HTTPError:
        vector_db = "unavailable"

    return {"status": "ok" if database == "ok" else "error", "database": database, "vector_db": vector_db}
