from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.config.database import SessionLocal
from app.models.modulo_model import Modulo

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/mis_modulos")
def obtener_modulos(db: Session = Depends(get_db)):
    modulos = db.query(Modulo).all()
    return [{"id": m.id, "nombre": m.nombre, "descripcion": m.descripcion} for m in modulos]
