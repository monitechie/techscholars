# tests/test_auth.py

from fastapi.testclient import TestClient
from app.main import app  # Replace with your FastAPI app instance

client = TestClient(app)


def test_token_validation():
    response = client.post(
        "/token",
        data={"username": "admin", "password": "admin"}
    )
    assert response.status_code == 200
    token = response.json().get("access_token")
    headers = {"Authorization": f"Bearer {token}"}
    response = client.get("/protected-endpoint", headers=headers)
    assert response.status_code == 200
    assert response.json() == {
        "msg": "You have access to this data", "user": "admin"}
