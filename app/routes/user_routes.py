from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.config.database import SessionLocal
from app.controllers.usuario_controller import UsuarioController
from app.schemas.usuario_schema import UsuarioCreate, UsuarioOut
from app.utils.auth_utils import get_current_user, require_admin 

# Creamos el router para agrupar las rutas de usuario
router = APIRouter()
usuario_controller = UsuarioController()

# Dependencia para obtener la sesión activa de base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Ruta para crear un nuevo usuario (pública)
@router.post("/create_user", response_model=UsuarioOut)
async def create_user(user: UsuarioCreate, db: Session = Depends(get_db)):
    return usuario_controller.create_usuario(db, user)

# Ruta para obtener un usuario por ID (pública)
@router.get("/get_user/{user_id}", response_model=UsuarioOut)
async def get_user(user_id: int, db: Session = Depends(get_db)):
    return usuario_controller.get_usuario_by_id(db, user_id)

# Ruta para obtener la lista de todos los usuarios (protegida solo para administradores)
@router.get("/get_users", response_model=list[UsuarioOut])
def get_users(
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_admin)  # Solo admins pueden acceder
):
    return usuario_controller.get_usuarios(db)
