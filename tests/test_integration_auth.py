from src.auth.reset import create_reset_token
from src.auth.security import verify_password
from src.repository.users import get_user_by_email
from tests.conftest import test_user, TestingSessionLocal


def test_reset_password_request_success(client):
    response = client.post(
        "/auth/reset-password-request", json={"email": test_user["email"]}
    )
    assert response.status_code == 200
    assert response.json()["message"] == "Password reset email sent"


def test_reset_password_request_user_not_found(client):
    response = client.post(
        "/auth/reset-password-request", json={"email": "notfound@example.com"}
    )
    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"


def test_reset_password_success(client):
    token = create_reset_token(
        test_user["email"]
    ) 

    new_password = "new_secure_password"
    response = client.post(
        "/auth/reset-password",
        json={"token": token, "new_password": new_password},
    )
    assert response.status_code == 200
    assert response.json()["message"] == "Password updated successfully"

    db = TestingSessionLocal()
    user = get_user_by_email(test_user["email"], db)
    assert verify_password(new_password, user.hashed_password)
    db.close()


def test_reset_password_invalid_token(client):
    response = client.post(
        "/auth/reset-password",
        json={"token": "invalid.token.here", "new_password": "anything"},
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "Invalid or expired token"


def test_reset_password_user_not_found(client):
    token = create_reset_token("ghost@example.com")

    response = client.post(
        "/auth/reset-password",
        json={"token": token, "new_password": "whatever"},
    )
    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"