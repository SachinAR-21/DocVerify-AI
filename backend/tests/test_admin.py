def test_only_admin_can_list_users(client, applicant, reviewer, admin):
    assert client.get("/api/admin/users", headers=applicant).status_code == 403
    assert client.get("/api/admin/users", headers=reviewer).status_code == 403
    assert client.get("/api/admin/users", headers=admin).status_code == 200


def test_access_denied_is_logged(client, applicant, admin):
    client.get("/api/admin/users", headers=applicant)
    log = client.get("/api/admin/audit-log?action=access_denied", headers=admin).json()
    assert len(log) == 1
    assert "/api/admin/users" in log[0]["details"]


def test_admin_creates_reviewer(client, admin):
    response = client.post(
        "/api/admin/users",
        headers=admin,
        json={
            "email": "jana@uni.de",
            "full_name": "Jana Becker",
            "password": "Jana12345",
            "role": "reviewer",
        },
    )
    assert response.status_code == 201
    assert response.json()["role"] == "reviewer"


def test_admin_changes_role_and_deactivates(client, applicant, admin):
    users = client.get("/api/admin/users", headers=admin).json()
    priya = next(u for u in users if u["email"] == "priya@example.com")

    response = client.patch(f"/api/admin/users/{priya['id']}", headers=admin, json={"role": "reviewer"})
    assert response.json()["role"] == "reviewer"

    client.patch(f"/api/admin/users/{priya['id']}", headers=admin, json={"is_active": False})
    login = client.post("/api/auth/login", json={"email": "priya@example.com", "password": "Secret123"})
    assert login.status_code == 403


def test_admin_can_not_change_own_role(client, admin):
    me = client.get("/api/auth/me", headers=admin).json()
    response = client.patch(f"/api/admin/users/{me['id']}", headers=admin, json={"role": "applicant"})
    assert response.status_code == 400


def test_manage_document_types(client, admin, applicant):
    response = client.post(
        "/api/admin/document-types",
        headers=admin,
        json={"name": "Portfolio", "description": "Design work", "is_required": False},
    )
    assert response.status_code == 201
    type_id = response.json()["id"]

    client.patch(f"/api/admin/document-types/{type_id}", headers=admin, json={"is_active": False})
    names = [t["name"] for t in client.get("/api/document-types", headers=applicant).json()]
    assert "Portfolio" not in names


def test_stats_and_audit_log(client, applicant, admin):
    client.post("/api/applications", headers=applicant, json={"programme": "MSc"})
    stats = client.get("/api/admin/stats", headers=admin).json()
    assert stats["applications_by_status"]["draft"] == 1
    actions = [e["action"] for e in client.get("/api/admin/audit-log", headers=admin).json()]
    assert "application_created" in actions
