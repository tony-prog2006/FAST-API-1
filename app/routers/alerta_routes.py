from fastapi import APIRouter, Depends
from app.utils.auth_utils import require_modulo

router = APIRouter()

@router.get("/alertas")
def ver_alertas(current_user: dict = Depends(require_modulo(2))):
    return {"msg": "Acceso autorizado al módulo de alertas", "usuario": current_user["sub"]}
