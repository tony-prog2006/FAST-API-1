from sqlalchemy import Column, Integer, String
from app.config.database import Base

class Modulo(Base):
    __tablename__ = "modulo"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(50), unique=True, nullable=False)
    descripcion = Column(String(255), nullable=True)
