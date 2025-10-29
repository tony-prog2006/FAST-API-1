from pydantic import BaseModel, Field
from typing import Optional
from app.schemas.rol_schema import RolOut

class UsuarioCreate(BaseModel):
    username: str
    password: str
    nombre: str
    edad: int = Field(..., ge=0)
    id_rol: int

class UsuarioOut(BaseModel):
    id: int
    username: str
    nombre: Optional[str] = None
    edad: Optional[int] = None
    id_rol: Optional[int] = None
    rol: Optional[RolOut] = None

    class Config:
        from_attributes = True
