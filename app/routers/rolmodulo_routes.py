from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.config.database import SessionLocal
from app.models.rolmodulo_model import RolModulo

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/asignar_modulo")
def asignar_modulo(id_rol: int, id_modulo: int, db: Session = Depends(get_db)):
    existe = db.query(RolModulo).filter_by(id_rol=id_rol, id_modulo=id_modulo).first()
    if existe:
        raise HTTPException(status_code=400, detail="Este rol ya tiene acceso a ese módulo")
    nuevo = RolModulo(id_rol=id_rol, id_modulo=id_modulo)
    db.add(nuevo)
    db.commit()
    return {"msg": "Acceso asignado correctamente"}
