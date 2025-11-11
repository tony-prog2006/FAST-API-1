from fastapi import APIRouter, Depends
from app.utils.auth_utils import require_modulo

router = APIRouter()

@router.get("/dashboard")
def ver_dashboard(current_user: dict = Depends(require_modulo(3))):
    return {"msg": "Acceso autorizado al módulo de estadísticas", "usuario": current_user["sub"]}
