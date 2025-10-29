import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
import sys, os

# Asegura que el directorio raíz esté en el path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.main import app
from app.config.database import SessionLocal
from app.models.rol_model import Rol
from app.models.rolmodulo_model import RolModulo

#  Fixture para cliente de prueba
@pytest.fixture(scope="module")
def client():
    with TestClient(app) as c:
        yield c

# Fixture para sesión de base de datos con limpieza automática
@pytest.fixture(scope="function")
def db_session():
    db: Session = SessionLocal()
    try:
        # Limpieza antes de cada test
        db.query(RolModulo).delete()
        db.query(Rol).delete()
        db.commit()
        yield db
    finally:
        db.close()
