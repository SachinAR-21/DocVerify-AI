import os
import tempfile

import pytest

# use a temporary SQLite database and upload folder for the tests
_tmp = tempfile.mkdtemp()
os.environ.setdefault("DATABASE_URL", f"sqlite:///{_tmp}/test.db")
os.environ["UPLOAD_DIR"] = f"{_tmp}/uploads"
os.environ["QDRANT_URL"] = "http://127.0.0.1:1"  # not running during unit tests
os.environ["ADMIN_EMAIL"] = "admin@example.com"
os.environ["ADMIN_PASSWORD"] = "Admin12345"
os.environ["REVIEWER_EMAIL"] = "reviewer@example.com"
os.environ["REVIEWER_PASSWORD"] = "Review12345"

from fastapi.testclient import TestClient  # noqa: E402

from app.database import Base, SessionLocal, engine  # noqa: E402
from app.main import app  # noqa: E402
from app.seed import seed  # noqa: E402

PDF_BYTES = b"%PDF-1.4\n% test document\n%%EOF\n"
PNG_BYTES = b"\x89PNG\r\n\x1a\n" + b"\x00" * 20


@pytest.fixture()
def client():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    with SessionLocal() as db:
        seed(db)
    with TestClient(app) as c:
        yield c


def login(client, email, password):
    response = client.post("/api/auth/login", json={"email": email, "password": password})
    assert response.status_code == 200, response.text
    return {"Authorization": f"Bearer {response.json()['access_token']}"}


def register_and_login(client, email="priya@example.com", password="Secret123"):
    response = client.post(
        "/api/auth/register",
        json={"email": email, "full_name": "Priya Raman", "password": password},
    )
    assert response.status_code == 201, response.text
    return login(client, email, password)


@pytest.fixture()
def applicant(client):
    return register_and_login(client)


@pytest.fixture()
def reviewer(client):
    return login(client, "reviewer@example.com", "Review12345")


@pytest.fixture()
def admin(client):
    return login(client, "admin@example.com", "Admin12345")


def upload(client, headers, app_id, type_id, content=PDF_BYTES, name="file.pdf", notes=""):
    return client.post(
        f"/api/applications/{app_id}/documents",
        headers=headers,
        data={"document_type_id": str(type_id), "notes": notes},
        files={"file": (name, content, "application/octet-stream")},
    )


def create_complete_application(client, headers, programme="MSc Data Science"):
    """Creates an application with all required documents uploaded."""
    app_id = client.post("/api/applications", headers=headers, json={"programme": programme}).json()["id"]
    types = client.get("/api/document-types", headers=headers).json()
    for t in types:
        if t["is_required"]:
            assert upload(client, headers, app_id, t["id"]).status_code == 201
    return app_id
