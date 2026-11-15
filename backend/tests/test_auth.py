from tests.conftest import login, register_and_login


def test_register_and_login(client):
    headers = register_and_login(client)
    me = client.get("/api/auth/me", headers=headers).json()
    assert me["email"] == "priya@example.com"
    assert me["role"] == "applicant"


def test_register_rejects_weak_password(client):
    response = client.post(
        "/api/auth/register",
        json={"email": "weak@example.com", "full_name": "Weak", "password": "abc"},
    )
    assert response.status_code == 400


def test_register_rejects_duplicate_email(client):
    register_and_login(client)
    response = client.post(
        "/api/auth/register",
        json={"email": "PRIYA@example.com", "full_name": "Priya", "password": "Secret123"},
    )
    assert response.status_code == 409


def test_wrong_password(client):
    register_and_login(client)
    response = client.post("/api/auth/login", json={"email": "priya@example.com", "password": "Wrong1234"})
    assert response.status_code == 401


def test_account_locked_after_failed_logins(client):
    register_and_login(client)
    for _ in range(5):
        client.post("/api/auth/login", json={"email": "priya@example.com", "password": "Wrong1234"})
    response = client.post("/api/auth/login", json={"email": "priya@example.com", "password": "Secret123"})
    assert response.status_code == 423


def test_password_is_not_stored_in_plain_text(client):
    from app.database import SessionLocal
    from app.models import User

    register_and_login(client)
    with SessionLocal() as db:
        user = db.query(User).filter_by(email="priya@example.com").one()
        assert user.password_hash != "Secret123"
        assert user.password_hash.startswith("$2")


def test_me_requires_token(client):
    assert client.get("/api/auth/me").status_code == 401
    assert client.get("/api/auth/me", headers={"Authorization": "Bearer nonsense"}).status_code == 401


def test_seeded_admin_can_login(client):
    headers = login(client, "admin@example.com", "Admin12345")
    assert client.get("/api/auth/me", headers=headers).json()["role"] == "admin"
