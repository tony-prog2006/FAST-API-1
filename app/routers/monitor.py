from fastapi import APIRouter, Query, HTTPException
from pydantic import BaseModel
from typing import Dict, Any, List
from services.especies import obtener_condiciones, obtener_zonas

router = APIRouter()

# Modelo de respuesta para validación de condiciones
class ValidacionResponse(BaseModel):
    especie_id: int
    valores_sensor: Dict[str, float]
    condiciones_ideales: Dict[str, Any]
    resultado_validacion: Dict[str, bool]

@router.get(
    "/validar-condiciones",
    response_model=ValidacionResponse,
    summary="Valida condiciones ambientales para una especie",
    description="Recibe valores de sensores y compara si están dentro del rango ideal para la especie indicada."
)
def validar(
    especie_id: int = Query(..., description="ID de la especie a validar"),
    temperatura: float = Query(..., ge=0, le=50, description="Temperatura medida (°C)"),
    ph: float = Query(..., ge=0, le=14, description="Nivel de pH medido"),
    oxigeno: float = Query(..., ge=0, le=20, description="Oxígeno disuelto medido (mg/L)")
):
    condiciones = obtener_condiciones(especie_id)
    if not condiciones:
        raise HTTPException(status_code=404, detail="No se encontraron condiciones para esta especie")

    c = condiciones[0]  # asumimos una sola fila por especie

    resultado = {
        "temperatura": float(c["temperatura_min"]) <= temperatura <= float(c["temperatura_max"]),
        "ph": float(c["ph_min"]) <= ph <= float(c["ph_max"]),
        "oxigeno": float(c["oxigeno_min"]) <= oxigeno <= float(c["oxigeno_max"])
    }

    return {
        "especie_id": especie_id,
        "valores_sensor": {
            "temperatura": temperatura,
            "ph": ph,
            "oxigeno": oxigeno
        },
        "condiciones_ideales": c,
        "resultado_validacion": resultado
    }

# Modelo de respuesta para zonas recomendadas
class ZonaResponse(BaseModel):
    id: int
    id_especie: int
    region: str
    departamento: str
    descripcion: str


@router.get(
    "/zonas-recomendadas",
    response_model=List[ZonaResponse],
    summary="Consulta zonas recomendadas para una especie",
    description="Devuelve las zonas asociadas a una especie específica, útil para visualización y análisis geográfico."
)
def zonas_recomendadas(
    especie_id: int = Query(..., description="ID de la especie a consultar")
):
    zonas = obtener_zonas(especie_id)
    if not zonas:
        raise HTTPException(status_code=404, detail="No se encontraron zonas para esta especie")
    return zonas
