from pydantic import BaseModel
from typing import Optional, List
from app.schemas.modulo_schema import ModuloOut

class RolCreate(BaseModel):
    nombre: str
    descripcion: Optional[str] = None

class RolOut(BaseModel):
    id: int
    nombre: str
    descripcion: Optional[str] = None

    class Config:
        from_attributes = True

class RolConModulosCreate(BaseModel):
    nombre: str
    descripcion: Optional[str] = None
    modulos: List[int]

class ModuloAsignadoOut(BaseModel):
    id: int  # ID de la asignación RolModulo
    modulo: ModuloOut

    class Config:
        from_attributes = True

class RolConModulosOut(BaseModel):
    id: int
    nombre: str
    descripcion: Optional[str] = None
    modulos: List[ModuloAsignadoOut]

    class Config:
        from_attributes = True
