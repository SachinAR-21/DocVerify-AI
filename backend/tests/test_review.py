from tests.conftest import create_complete_application, upload


def submitted_application(client, applicant):
    app_id = create_complete_application(client, applicant)
    client.post(f"/api/applications/{app_id}/submit", headers=applicant)
    return app_id


def test_applicant_can_not_open_review_queue(client, applicant):
    assert client.get("/api/review/queue", headers=applicant).status_code == 403


def test_queue_shows_submitted_applications(client, applicant, reviewer):
    client.post("/api/applications", headers=applicant, json={"programme": "Draft only"})
    app_id = submitted_application(client, applicant)
    queue = client.get("/api/review/queue", headers=reviewer).json()
    assert [a["id"] for a in queue] == [app_id]


def test_queue_filter_by_programme(client, applicant, reviewer):
    submitted_application(client, applicant)
    assert len(client.get("/api/review/queue?programme=data", headers=reviewer).json()) == 1
    assert client.get("/api/review/queue?programme=medicine", headers=reviewer).json() == []


def test_start_review_marks_in_progress(client, applicant, reviewer):
    app_id = submitted_application(client, applicant)
    response = client.post(f"/api/review/applications/{app_id}/start", headers=reviewer)
    assert response.json()["status"] == "in_review"
    assert response.json()["reviewer"]["email"] == "reviewer@example.com"


def test_accept_application(client, applicant, reviewer):
    app_id = submitted_application(client, applicant)
    response = client.post(
        f"/api/review/applications/{app_id}/decision", headers=reviewer, json={"decision": "accept"}
    )
    assert response.status_code == 200
    assert response.json()["status"] == "accepted"


def test_reject_needs_comment(client, applicant, reviewer):
    app_id = submitted_application(client, applicant)
    response = client.post(
        f"/api/review/applications/{app_id}/decision", headers=reviewer, json={"decision": "reject"}
    )
    assert response.status_code == 400


def test_request_documents_lets_applicant_upload_again(client, applicant, reviewer):
    app_id = submitted_application(client, applicant)
    response = client.post(
        f"/api/review/applications/{app_id}/decision",
        headers=reviewer,
        json={"decision": "request_documents", "comment": "Please upload a certified translation."},
    )
    assert response.json()["status"] == "needs_documents"

    detail = client.get(f"/api/applications/{app_id}", headers=applicant).json()
    assert detail["decisions"][0]["comment"] == "Please upload a certified translation."

    type_id = client.get("/api/document-types", headers=applicant).json()[1]["id"]
    assert upload(client, applicant, app_id, type_id).status_code == 201
    assert (
        client.post(f"/api/applications/{app_id}/submit", headers=applicant).json()["status"] == "submitted"
    )


def test_reviewer_can_download_document(client, applicant, reviewer):
    app_id = submitted_application(client, applicant)
    doc_id = client.get(f"/api/applications/{app_id}", headers=reviewer).json()["documents"][0]["id"]
    assert client.get(f"/api/documents/{doc_id}/file", headers=reviewer).status_code == 200
