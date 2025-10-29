from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.config.database import SessionLocal
from app.models.modulo_model import Modulo
from app.models.rolmodulo_model import RolModulo
from app.utils.auth_utils import get_current_user

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/mis_modulos")
def obtener_modulos(current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    rol_id = current_user["rol"]
    relaciones = db.query(RolModulo).filter_by(id_rol=rol_id).all()
    modulos = [db.query(Modulo).filter_by(id=r.id_modulo).first() for r in relaciones]
    return [{"id": m.id, "nombre": m.nombre, "descripcion": m.descripcion} for m in modulos if m]
