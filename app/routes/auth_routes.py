from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from pymysql.err import IntegrityError as MySQLIntegrityError
from app.config.database import SessionLocal
from app.schemas.auth_schema import LoginRequest, TokenResponse
from app.schemas.usuario_schema import UsuarioCreate, UsuarioOut
from app.models.usuario_model import Usuario
from app.models.rol_model import Rol
from app.utils.auth_utils import create_access_token, verify_password, hash_password

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/login", response_model=TokenResponse)
def login(credentials: LoginRequest, db: Session = Depends(get_db)):
    usuario = db.query(Usuario).filter(Usuario.username == credentials.username).first()

    if not usuario:
        raise HTTPException(status_code=401, detail="Credenciales inválidas")

    if not usuario.password:
        raise HTTPException(status_code=500, detail="Contraseña no registrada para este usuario")

    if not verify_password(credentials.password, usuario.password):
        raise HTTPException(status_code=401, detail="Credenciales inválidas")

    token_data = {
        "sub": usuario.username,
        "id": usuario.id,
        "rol": usuario.id_rol
    }

    access_token = create_access_token(token_data)
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/create_user", response_model=UsuarioOut)
def create_user(user: UsuarioCreate, db: Session = Depends(get_db)):
    existente = db.query(Usuario).filter(Usuario.username == user.username).first()
    if existente:
        raise HTTPException(status_code=400, detail="El usuario ya existe")

    nuevo_usuario = Usuario(
        username=user.username,
        password=hash_password(user.password),
        nombre=user.nombre,
        edad=user.edad,
        id_rol=user.id_rol
    )

    db.add(nuevo_usuario)
    try:
        db.commit()
        db.refresh(nuevo_usuario)
        return nuevo_usuario
    except:
        db.rollback()
        raise HTTPException(status_code=500, detail="Error interno al crear usuario")
