from pydantic import BaseModel
from typing import Optional

class ModuloCreate(BaseModel):
    nombre: str  # Ej: "dashboard"
    descripcion: Optional[str] = None  # Ej: "Estadísticas generales"

class ModuloOut(BaseModel):
    id: int
    nombre: str
    descripcion: Optional[str] = None

    class Config:
        from_attributes = True
