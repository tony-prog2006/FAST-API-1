from fastapi.testclient import TestClient
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app.main import app

client = TestClient(app)

def eliminar_usuario_si_existe(username):
    from app.config.database import SessionLocal
    from app.models.usuario_model import Usuario
    db = SessionLocal()
    usuario = db.query(Usuario).filter(Usuario.username == username).first()
    if usuario:
        db.delete(usuario)
        db.commit()
    db.close()

def test_crear_usuario_exitoso():
    eliminar_usuario_si_existe("nuevo_usuario")
    response = client.post("/create_user", json={
        "username": "nuevo_usuario",
        "password": "nuevapass",
        "nombre": "Nuevo",
        "edad": 22,
        "id_rol": 2
    })
    assert response.status_code == 200
    assert response.json()["username"] == "nuevo_usuario"

def test_crear_usuario_sin_password():
    eliminar_usuario_si_existe("sinpass")
    response = client.post("/create_user", json={
        "username": "sinpass",
        "nombre": "Sin Pass",
        "edad": 25,
        "id_rol": 2
    })
    assert response.status_code == 422

def test_crear_usuario_con_edad_invalida():
    eliminar_usuario_si_existe("menor")
    response = client.post("/create_user", json={
        "username": "menor",
        "password": "pass123",
        "nombre": "Menor",
        "edad": -5,
        "id_rol": 2
    })
    assert response.status_code == 422

#def test_crear_usuario_duplicado():
 #   eliminar_usuario_si_existe("duplicado")
  #  client.post("/create_user", json={
   #     "username": "duplicado",
    #    "password": "pass123",
     #   "nombre": "Duplicado",
      #  "edad": 30,
       # "id_rol": 2
    #})
    #response = client.post("/create_user", json={
     #   "username": "duplicado",
      #  "password": "pass123",
       # "nombre": "Duplicado",
        #"edad": 30,
        #"id_rol": 2
    #})
    #assert response.status_code == 400
    #assert response.json()["detail"] == "El usuario ya existe"
