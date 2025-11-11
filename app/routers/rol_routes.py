from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.config.database import SessionLocal
from app.controllers.rol_controller import RolController
from app.schemas.rol_schema import RolCreate, RolOut, RolConModulosCreate, RolConModulosOut, ModuloAsignadoOut
from app.models.modulo_model import Modulo
from app.models.rolmodulo_model import RolModulo
from app.models.rol_model import Rol
from typing import List

router = APIRouter()
rol_controller = RolController()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/roles", response_model=RolOut, status_code=201)
def create_rol(rol: RolCreate, db: Session = Depends(get_db)):
    try:
        return rol_controller.create_rol(db, rol)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al crear rol: {str(e)}")

@router.get("/roles", response_model=List[RolOut])
def get_roles(db: Session = Depends(get_db)):
    try:
        return rol_controller.get_roles(db)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener roles: {str(e)}")

@router.post("/roles_con_modulos", response_model=RolConModulosOut, status_code=201)
def create_rol_con_modulos(data: RolConModulosCreate, db: Session = Depends(get_db)):
    try:
        if db.query(Rol).filter(Rol.nombre == data.nombre).first():
            raise HTTPException(status_code=400, detail="El rol ya existe")

        nuevo_rol = Rol(nombre=data.nombre, descripcion=data.descripcion)
        db.add(nuevo_rol)
        db.commit()
        db.refresh(nuevo_rol)

        asignaciones = []
        for id_modulo in data.modulos:
            modulo = db.query(Modulo).filter(Modulo.id == id_modulo).first()
            if not modulo:
                raise HTTPException(status_code=404, detail=f"Módulo con ID {id_modulo} no existe")
            asignacion = RolModulo(id_rol=nuevo_rol.id, id_modulo=id_modulo)
            db.add(asignacion)
            db.commit()
            db.refresh(asignacion)
            asignaciones.append({
                "id": modulo.id,
                "nombre": modulo.nombre,
                "descripcion": modulo.descripcion
            })

        return {
            "id": nuevo_rol.id,
            "nombre": nuevo_rol.nombre,
            "descripcion": nuevo_rol.descripcion,
            "modulos": asignaciones
        }

    except HTTPException as e:
        raise e
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error inesperado: {str(e)}")

@router.get("/roles_con_modulos", response_model=List[RolConModulosOut])
def get_roles_con_modulos(db: Session = Depends(get_db)):
    try:
        roles = db.query(Rol).all()
        resultado = []

        for rol in roles:
            asignaciones = db.query(RolModulo).filter(RolModulo.id_rol == rol.id).all()
            modulos = []
            for asignacion in asignaciones:
                modulo = db.query(Modulo).filter(Modulo.id == asignacion.id_modulo).first()
                if modulo:
                    modulos.append({
                        "id": modulo.id,
                        "nombre": modulo.nombre,
                        "descripcion": modulo.descripcion
                    })
            resultado.append({
                "id": rol.id,
                "nombre": rol.nombre,
                "descripcion": rol.descripcion,
                "modulos": modulos
            })

        return resultado

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener roles con módulos: {str(e)}")

@router.get("/modulos_por_rol/{id_rol}", response_model=List[ModuloAsignadoOut])
def get_modulos_por_rol(id_rol: int, db: Session = Depends(get_db)):
    try:
        asignaciones = db.query(RolModulo).filter(RolModulo.id_rol == id_rol).all()
        modulos = []
        for asignacion in asignaciones:
            modulo = db.query(Modulo).filter(Modulo.id == asignacion.id_modulo).first()
            if modulo:
                modulos.append({
                    "id": modulo.id,
                    "nombre": modulo.nombre,
                    "descripcion": modulo.descripcion
                })
        return modulos
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener módulos del rol: {str(e)}")

@router.delete("/modulos_por_rol", status_code=204)
def delete_modulo_por_rol(id_rol: int, id_modulo: int, db: Session = Depends(get_db)):
    try:
        asignacion = db.query(RolModulo).filter(
            RolModulo.id_rol == id_rol,
            RolModulo.id_modulo == id_modulo
        ).first()

        if not asignacion:
            raise HTTPException(status_code=404, detail="Asignación no encontrada")

        db.delete(asignacion)
        db.commit()
        return

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error al revocar acceso: {str(e)}")

@router.put("/roles_con_modulos/{id}", response_model=RolOut)
def update_rol_con_modulos(id: int, data: RolConModulosCreate, db: Session = Depends(get_db)):
    try:
        rol = db.query(Rol).filter(Rol.id == id).first()
        if not rol:
            raise HTTPException(status_code=404, detail="Rol no encontrado")

        rol.nombre = data.nombre
        rol.descripcion = data.descripcion
        db.commit()

        db.query(RolModulo).filter(RolModulo.id_rol == id).delete()

        for id_modulo in data.modulos:
            modulo = db.query(Modulo).filter(Modulo.id == id_modulo).first()
            if not modulo:
                raise HTTPException(status_code=404, detail=f"Módulo con ID {id_modulo} no existe")
            nueva_asignacion = RolModulo(id_rol=id, id_modulo=id_modulo)
            db.add(nueva_asignacion)

        db.commit()
        db.refresh(rol)
        return rol

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error al actualizar rol con módulos: {str(e)}")

@router.delete("/rolmodulo/{id}", status_code=204)
def delete_rolmodulo(id: int, db: Session = Depends(get_db)):
    try:
        asignacion = db.query(RolModulo).filter(RolModulo.id == id).first()
        if not asignacion:
            raise HTTPException(status_code=404, detail="Asignación rol-módulo no encontrada")

        db.delete(asignacion)
        db.commit()
        return

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error al eliminar asignación: {str(e)}")
