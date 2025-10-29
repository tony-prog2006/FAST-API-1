from pydantic import BaseModel

class RolModuloCreate(BaseModel):
    id_rol: int
    id_modulo: int

class RolModuloOut(BaseModel):
    id: int
    id_rol: int
    id_modulo: int

    class Config:
        from_attributes = True
