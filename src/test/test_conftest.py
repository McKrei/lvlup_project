import sys

sys.path.append(r"C:\Users\legion\projects\NEW\investment_portfolio\src")

import pytest
from fastapi.testclient import TestClient
from main import app

@pytest.fixture
def client():
    client = TestClient(app)
    yield client


def test_create_user(client):
    user_data = {
        "username": "testuser",
        "email": "test@example.com",
        "password": "testpassword"
    }
    response = client.post("/user/", json=user_data)
    assert response.status_code == 201
    data = response.json()
    assert data["username"] == user_data["username"]
    assert data["email"] == user_data["email"]
    assert "password" not in data
