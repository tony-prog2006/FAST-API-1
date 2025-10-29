import pytest

#  Login exitoso
def test_login_usuario_normal(client):
    response = client.post("/login", json={"username": "usuario_normal", "password": "normalpass"})
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

def test_login_admin(client):
    response = client.post("/login", json={"username": "admin", "password": "adminpass"})
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data

#  Login fallido
def test_login_invalido(client):
    response = client.post("/login", json={"username": "usuario_normal", "password": "clave_incorrecta"})
    assert response.status_code == 401
    assert "credenciales" in response.json()["detail"].lower()

#  Acceso autorizado para admin
def test_acceso_admin(client):
    token = client.post("/login", json={"username": "admin", "password": "adminpass"}).json()["access_token"]
    response = client.get("/get_users", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200

#  Acceso denegado para usuario normal
def test_acceso_denegado_usuario_normal(client):
    token = client.post("/login", json={"username": "usuario_normal", "password": "normalpass"}).json()["access_token"]
    response = client.get("/get_users", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 403
    assert "restringido" in response.json()["detail"].lower()

#  Token inválido
def test_token_manipulado(client):
    fake_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.fake.payload.signature"
    response = client.get("/get_users", headers={"Authorization": f"Bearer {fake_token}"})
    assert response.status_code == 401
    assert "token" in response.json()["detail"].lower()
