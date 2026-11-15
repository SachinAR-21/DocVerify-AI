from tests.conftest import PNG_BYTES, create_complete_application, register_and_login, upload


def first_type(client, headers):
    return client.get("/api/document-types", headers=headers).json()[0]["id"]


def test_create_and_list_application(client, applicant):
    response = client.post("/api/applications", headers=applicant, json={"programme": "MSc Data Science"})
    assert response.status_code == 201
    assert response.json()["status"] == "draft"
    apps = client.get("/api/applications", headers=applicant).json()
    assert len(apps) == 1


def test_upload_pdf_and_png(client, applicant):
    app_id = client.post("/api/applications", headers=applicant, json={"programme": "MSc"}).json()["id"]
    type_id = first_type(client, applicant)
    assert upload(client, applicant, app_id, type_id, notes="My degree").status_code == 201
    assert upload(client, applicant, app_id, type_id, PNG_BYTES, "scan.png").status_code == 201

    detail = client.get(f"/api/applications/{app_id}", headers=applicant).json()
    assert detail["document_count"] == 2
    assert detail["documents"][0]["notes"] == "My degree"


def test_upload_rejects_wrong_file_type(client, applicant):
    app_id = client.post("/api/applications", headers=applicant, json={"programme": "MSc"}).json()["id"]
    response = upload(client, applicant, app_id, first_type(client, applicant), b"hello", "virus.exe")
    assert response.status_code == 400


def test_upload_rejects_fake_pdf(client, applicant):
    app_id = client.post("/api/applications", headers=applicant, json={"programme": "MSc"}).json()["id"]
    response = upload(client, applicant, app_id, first_type(client, applicant), b"not a pdf", "fake.pdf")
    assert response.status_code == 400


def test_upload_rejects_too_big_file(client, applicant, monkeypatch):
    from app.config import get_settings

    monkeypatch.setattr(get_settings(), "max_upload_mb", 0)
    app_id = client.post("/api/applications", headers=applicant, json={"programme": "MSc"}).json()["id"]
    response = upload(client, applicant, app_id, first_type(client, applicant))
    assert response.status_code == 413


def test_submit_needs_all_required_documents(client, applicant):
    app_id = client.post("/api/applications", headers=applicant, json={"programme": "MSc"}).json()["id"]
    response = client.post(f"/api/applications/{app_id}/submit", headers=applicant)
    assert response.status_code == 400
    assert "Missing required documents" in response.json()["detail"]


def test_submit_complete_application(client, applicant):
    app_id = create_complete_application(client, applicant)
    response = client.post(f"/api/applications/{app_id}/submit", headers=applicant)
    assert response.status_code == 200
    assert response.json()["status"] == "submitted"
    # after submitting, documents can not be changed anymore
    type_id = first_type(client, applicant)
    assert upload(client, applicant, app_id, type_id).status_code == 400


def test_applicant_can_not_see_other_applications(client, applicant):
    app_id = client.post("/api/applications", headers=applicant, json={"programme": "MSc"}).json()["id"]
    other = register_and_login(client, "other@example.com", "Other12345")
    assert client.get(f"/api/applications/{app_id}", headers=other).status_code == 404
    assert client.get("/api/applications", headers=other).json() == []


def test_download_and_delete_document(client, applicant):
    app_id = client.post("/api/applications", headers=applicant, json={"programme": "MSc"}).json()["id"]
    doc_id = upload(client, applicant, app_id, first_type(client, applicant)).json()["id"]
    response = client.get(f"/api/documents/{doc_id}/file", headers=applicant)
    assert response.status_code == 200
    assert response.content.startswith(b"%PDF")
    assert client.delete(f"/api/documents/{doc_id}", headers=applicant).status_code == 204
