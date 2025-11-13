from pydantic import BaseModel, EmailStr
from typing import Optional
from app.schemas.rol_schema import RolOut

class UsuarioCreate(BaseModel):
    password: str
    nombre: str
    apellido: str
    email: EmailStr
    id_rol: int

class UsuarioOut(BaseModel):
    id: int
    nombre: Optional[str] = None
    apellido: Optional[str] = None
    email: Optional[EmailStr] = None
    id_rol: Optional[int] = None
    rol: Optional[RolOut] = None

    class Config:
        orm_mode = True

class CambioRolUsuario(BaseModel):
    nuevo_id_rol: int
