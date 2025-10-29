from datetime import datetime, timedelta, UTC
from jose import JWTError, jwt
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.config.database import SessionLocal
from app.models.usuario_model import Usuario
from app.models.rolmodulo_model import RolModulo
import bcrypt

# Clave secreta para firmar el token (debe mantenerse segura)
SECRET_KEY = "tu_clave_secreta_segura"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

#  Crear token JWT
def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.now(UTC) + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

#  Obtener usuario actual desde el token
def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Token inválido")
        return payload
    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido o expirado")

#  Validar si el usuario es administrador
def require_admin(current_user: dict = Depends(get_current_user)):
    if current_user.get("rol") != 1:
        raise HTTPException(status_code=403, detail="Acceso restringido: solo administradores")
    return current_user

# Validar si el usuario tiene acceso a un módulo específico
def require_modulo(modulo_id: int):
    def wrapper(current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
        acceso = db.query(RolModulo).filter_by(id_rol=current_user["rol"], id_modulo=modulo_id).first()
        if not acceso:
            raise HTTPException(status_code=403, detail="Acceso denegado: no tienes permiso para este módulo")
        return current_user
    return wrapper

#  Encriptar contraseña
def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')

#  Verificar contraseña
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

#  Obtener sesión de base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
