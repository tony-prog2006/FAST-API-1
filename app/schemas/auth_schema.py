#Esquemas Pydantic para validar entrada y salida del login
from pydantic import BaseModel

# Esquema para recibir credenciales del usuario (entrada)
class LoginRequest(BaseModel):  
    username: str  # Nombre de usuario
    password: str  # Contraseña en texto plano (se validará en el backend)

# Esquema para devolver el token JWT al cliente (salida)
class TokenResponse(BaseModel):
    access_token: str  # Token de acceso generado
    token_type: str = "bearer"  # Tipo de token usado en el header Authorization
