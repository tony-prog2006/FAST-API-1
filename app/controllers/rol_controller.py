# Importamos la sesión de SQLAlchemy
from sqlalchemy.orm import Session

# Importamos el modelo ORM y el esquema de entrada
from app.models.rol_model import Rol
from app.schemas.rol_schema import RolCreate

# Esta clase contiene funciones que interactúan con la base de datos
class RolController:

    # Crear un nuevo rol en la base de datos
    def create_rol(self, db: Session, rol_data: RolCreate):
        # Convertimos el esquema Pydantic en un modelo ORM
        nuevo_rol = Rol(**rol_data.dict())
        db.add(nuevo_rol)         # Agregamos el nuevo rol a la sesión
        db.commit()               # Guardamos los cambios en la base de datos
        db.refresh(nuevo_rol)     # Actualizamos el objeto con el ID generado
        return nuevo_rol

    # Obtener todos los roles registrados
    def get_roles(self, db: Session):
        return db.query(Rol).all()  # Consulta todos los registros de la tabla Rol
