from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.config.database import Base

class RolModulo(Base):
    __tablename__ = "rolmodulo"

    id = Column(Integer, primary_key=True, index=True)
    id_rol = Column(Integer, ForeignKey("rol.id"), nullable=False)
    id_modulo = Column(Integer, ForeignKey("modulo.id"), nullable=False)

