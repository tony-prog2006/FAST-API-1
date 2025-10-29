from pydantic import BaseModel
from typing import Optional, List

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

# ✅ Esquema para cada módulo asignado (usado en /roles_con_modulos y /modulos_por_rol)
class ModuloAsignadoOut(BaseModel):
    id: int
    nombre: str
    descripcion: Optional[str] = None

    class Config:
        from_attributes = True

# ✅ Esquema de salida para /roles_con_modulos
class RolConModulosOut(BaseModel):
    id: int
    nombre: str
    descripcion: Optional[str] = None
    modulos: List[ModuloAsignadoOut]

    class Config:
        from_attributes = True
