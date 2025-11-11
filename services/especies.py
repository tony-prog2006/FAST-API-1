import requests

BASE_URL = "http://localhost:3000/api"
TIMEOUT = 5  # segundos

def obtener_especies():
    try:
        resp = requests.get(f"{BASE_URL}/especies", timeout=TIMEOUT)
        resp.raise_for_status()
        return resp.json()
    except requests.RequestException as e:
        print(f"[ERROR] No se pudo obtener especies: {e}")
        return []

def obtener_condiciones(especie_id: int):
    try:
        resp = requests.get(f"{BASE_URL}/condiciones", params={"especie_id": especie_id}, timeout=TIMEOUT)
        resp.raise_for_status()
        return resp.json()
    except requests.RequestException as e:
        print(f"[ERROR] No se pudo obtener condiciones para especie {especie_id}: {e}")
        return []

def obtener_zonas(especie_id: int):
    try:
        resp = requests.get(f"{BASE_URL}/zonas", params={"especie_id": especie_id}, timeout=TIMEOUT)
        resp.raise_for_status()
        return resp.json()
    except requests.RequestException as e:
        print(f"[ERROR] No se pudo obtener zonas para especie {especie_id}: {e}")
        return []
