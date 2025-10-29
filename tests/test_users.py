from fastapi.testclient import TestClient
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app.main import app

client = TestClient(app)

def obtener_token():
    response = client.post("/login", json={"username": "testuser", "password": "testpass"})
    return response.json()["access_token"]

def test_get_users_con_token_valido():
    token = obtener_token()
    response = client.get("/get_users", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_users_sin_token():
    response = client.get("/get_users")
    assert response.status_code == 401

def test_get_users_con_token_invalido():
    response = client.get("/get_users", headers={"Authorization": "Bearer token_falso"})
    assert response.status_code == 401
