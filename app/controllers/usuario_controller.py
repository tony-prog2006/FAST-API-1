from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.usuario_model import Usuario
from app.schemas.usuario_schema import UsuarioCreate
from app.utils.auth_utils import hash_password
from utils.email import enviar_correo_bienvenida  # 👈 Importar función de correo

class UsuarioController:

    def create_usuario(self, db: Session, usuario_data: UsuarioCreate):
        try:
            if not usuario_data.password or usuario_data.password.strip() == "":
                raise HTTPException(status_code=400, detail="La contraseña no puede estar vacía")

            nuevo_usuario = Usuario(
                password=hash_password(usuario_data.password),
                nombre=usuario_data.nombre,
                apellido=usuario_data.apellido,
                email=usuario_data.email,
                id_rol=usuario_data.id_rol,
            )
            db.add(nuevo_usuario)
            db.commit()
            db.refresh(nuevo_usuario)

       
            try:
                enviar_correo_bienvenida(destinatario=nuevo_usuario.email, nombre=nuevo_usuario.nombre, apellido=nuevo_usuario.apellido)
            except Exception as e:
                print(f"Error al enviar correo: {e}")

            return nuevo_usuario
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=500, detail=f"Error al crear usuario: {str(e)}")

    def get_usuarios(self, db: Session):
        try:
            return db.query(Usuario).all()
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error al obtener usuarios: {str(e)}")

    def get_usuario_by_id(self, db: Session, usuario_id: int):
        try:
            usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()
            if not usuario:
                raise HTTPException(status_code=404, detail="Usuario no encontrado")
            return usuario
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error al buscar usuario: {str(e)}")
