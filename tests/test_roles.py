import uuid

# 🔐 Simulación de login para obtener token de usuario normal
def obtener_token_usuario_normal(client):
    response = client.post("/login", json={"username": "usuario_normal", "password": "normalpass"})
    assert response.status_code == 200
    return response.json()["access_token"]

# 🔐 Test de acceso restringido
def test_acceso_restringido_para_rol_no_admin(client):
    token = obtener_token_usuario_normal(client)
    response = client.get("/get_users", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 403
    assert response.json()["detail"] == "Acceso restringido: solo administradores"

# ✅ Test: crear rol con módulos
def test_crear_rol_con_modulos(client):
    nombre_unico = f"rol_test_{uuid.uuid4().hex[:6]}"
    payload = {
        "nombre": nombre_unico,
        "descripcion": "Rol creado desde test",
        "modulos": [1, 2]
    }

    response = client.post("/roles_con_modulos", json=payload)
    print("📌 CREAR ROL:", response.json())
    assert response.status_code == 201
    data = response.json()
    assert data["nombre"] == payload["nombre"]
    assert data["descripcion"] == payload["descripcion"]
    assert isinstance(data["modulos"], list)

# ✅ Test: listar roles con módulos
def test_listar_roles_con_modulos(client):
    response = client.get("/roles_con_modulos")
    print("📌 LISTAR ROLES:", response.json())
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    if data:
        assert "id" in data[0]
        assert "modulos" in data[0]

# ✅ Test: actualizar rol con nuevos módulos
def test_actualizar_rol_con_modulos(client):
    nombre_unico = f"rol_actualizable_{uuid.uuid4().hex[:6]}"
    payload_creacion = {
        "nombre": nombre_unico,
        "descripcion": "Inicial",
        "modulos": [1]
    }
    response_creacion = client.post("/roles_con_modulos", json=payload_creacion)
    assert response_creacion.status_code == 201
    rol_id = response_creacion.json()["id"]

    payload_actualizacion = {
        "nombre": f"{nombre_unico}_actualizado",
        "descripcion": "Descripción actualizada",
        "modulos": [2]
    }
    response_actualizacion = client.put(f"/roles_con_modulos/{rol_id}", json=payload_actualizacion)
    print("📌 ACTUALIZAR ROL:", response_actualizacion.json())
    assert response_actualizacion.status_code == 200
    data = response_actualizacion.json()
    assert data["nombre"] == payload_actualizacion["nombre"]
    assert data["descripcion"] == payload_actualizacion["descripcion"]

# ✅ Test: error al crear rol duplicado
def test_error_rol_duplicado(client):
    nombre_fijo = "rol_duplicado_test"
    payload = {
        "nombre": nombre_fijo,
        "descripcion": "Rol duplicado",
        "modulos": [1]
    }

    response1 = client.post("/roles_con_modulos", json=payload)
    assert response1.status_code in [201, 400]

    response2 = client.post("/roles_con_modulos", json=payload)
    print("📌 ERROR DUPLICADO:", response2.json())
    assert response2.status_code == 400
    assert "ya existe" in response2.json()["detail"]

# ✅ Test: error al asignar módulo inexistente
def test_error_modulo_inexistente(client):
    nombre_unico = f"rol_modulo_invalido_{uuid.uuid4().hex[:6]}"
    payload = {
        "nombre": nombre_unico,
        "descripcion": "Rol con módulo inválido",
        "modulos": [9999]
    }

    response = client.post("/roles_con_modulos", json=payload)
    print("📌 ERROR MÓDULO:", response.json())
    assert response.status_code == 404
    assert "no existe" in response.json()["detail"]

# ✅ Test: eliminar asignación rol-módulo
def test_eliminar_asignacion_rol_modulo(client):
    nombre_unico = f"rol_para_eliminar_{uuid.uuid4().hex[:6]}"
    payload = {
        "nombre": nombre_unico,
        "descripcion": "Rol temporal",
        "modulos": [1]
    }

    response = client.post("/roles_con_modulos", json=payload)
    assert response.status_code == 201
    rol_id = response.json()["id"]

    response_roles = client.get("/roles_con_modulos")
    asignacion_id = None
    for rol in response_roles.json():
        if rol["id"] == rol_id and rol["modulos"]:
            asignacion_id = rol["modulos"][0]["id"]
            break

    assert asignacion_id is not None

    response_delete = client.delete(f"/rolmodulo/{asignacion_id}")
    print("📌 ELIMINAR ASIGNACIÓN:", response_delete.status_code)
    assert response_delete.status_code == 204

