#Lógica de negocio para validar credenciales y generar token
from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.models.usuario_model import Usuario
from app.schemas.auth_schema import LoginRequest
from app.utils.auth_utils import create_access_token

class AuthController:

    # Función para iniciar sesión y generar token
    def login(self, db: Session, credentials: LoginRequest):
        # Buscamos el usuario por nombre
        user = db.query(Usuario).filter(Usuario.username == credentials.username).first()

        # Validamos existencia y contraseña (sin encriptar por ahora)
        if not user or user.password != credentials.password:
            raise HTTPException(status_code=401, detail="Credenciales inválidas")

        # Datos que se incluirán en el token
        token_data = {
            "sub": user.username,  # Identificador principal
            "id": user.id,         # ID del usuario
            "rol": user.id_rol     # Rol asignado
        }

        # Generamos el token JWT
        access_token = create_access_token(token_data)

        # Devolvemos el token al cliente
        return {"access_token": access_token, "token_type": "bearer"}
