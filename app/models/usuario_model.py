from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.config.database import Base

class Usuario(Base):
    __tablename__ = "usuario"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    nombre = Column(String(100), nullable=False)
    edad = Column(Integer, nullable=False)
    id_rol = Column(Integer, ForeignKey("rol.id"), nullable=False)

    rol = relationship("Rol", back_populates="usuarios")  #  relación con Rol
