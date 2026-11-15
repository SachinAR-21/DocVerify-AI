def test_health(client):
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json()["database"] == "ok"


def test_vector_db_not_running_in_unit_tests(client):
    # Qdrant only runs in docker compose, so here it is reported as unavailable
    assert client.get("/api/health").json()["vector_db"] == "unavailable"


def test_default_document_types_are_created(client):
    from app.database import SessionLocal
    from app.models import DocumentType

    with SessionLocal() as db:
        names = [t.name for t in db.query(DocumentType).all()]
    assert "Transcript of records" in names
