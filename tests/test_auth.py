from fastapi.testclient import TestClient
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app.main import app

client = TestClient(app)

def test_login_correcto():
    response = client.post("/login", json={"username": "testuser", "password": "testpass"})
    assert response.status_code == 200
    assert "access_token" in response.json()

def test_login_usuario_invalido():
    response = client.post("/login", json={"username": "no_existe", "password": "123456"})
    assert response.status_code == 401
    assert response.json()["detail"] == "Usuario no encontrado"

def test_login_contraseña_incorrecta():
    response = client.post("/login", json={"username": "testuser", "password": "clave_mal"})
    assert response.status_code == 401
    assert response.json()["detail"] == "Contraseña incorrecta"
