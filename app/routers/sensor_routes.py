from fastapi import APIRouter, Depends
from app.utils.auth_utils import require_modulo

router = APIRouter()

@router.get("/sensores")
def ver_sensores(current_user: dict = Depends(require_modulo(1))):
    return {"msg": "Acceso autorizado al módulo de monitoreo", "usuario": current_user["sub"]}
