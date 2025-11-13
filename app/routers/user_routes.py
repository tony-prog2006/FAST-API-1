from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.config.database import SessionLocal
from app.controllers.usuario_controller import UsuarioController
from app.schemas.usuario_schema import UsuarioCreate, UsuarioOut

router = APIRouter()
usuario_controller = UsuarioController()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/create_user", response_model=UsuarioOut)
async def create_user(user: UsuarioCreate, db: Session = Depends(get_db)):
    return usuario_controller.create_usuario(db, user)

@router.get("/get_user/{user_id}", response_model=UsuarioOut)
async def get_user(user_id: int, db: Session = Depends(get_db)):
    return usuario_controller.get_usuario_by_id(db, user_id)

@router.get("/get_users", response_model=list[UsuarioOut])
def get_users(db: Session = Depends(get_db)):
    return usuario_controller.get_usuarios(db)
