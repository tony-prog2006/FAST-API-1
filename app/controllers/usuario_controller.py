from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.usuario_model import Usuario
from app.models.rol_model import Rol
from app.schemas.usuario_schema import UsuarioCreate, CambioRolUsuario
from app.utils.auth_utils import hash_password
from utils.email import enviar_correo_bienvenida, enviar_correo_cambio_rol

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
                enviar_correo_bienvenida(
                    destinatario=nuevo_usuario.email,
                    nombre=nuevo_usuario.nombre,
                    apellido=nuevo_usuario.apellido
                )
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

    def cambiar_rol_usuario(self, db: Session, id_usuario: int, datos: CambioRolUsuario):
        try:
            usuario = db.query(Usuario).filter(Usuario.id == id_usuario).first()
            if not usuario:
                raise HTTPException(status_code=404, detail="Usuario no encontrado")

            rol_anterior = db.query(Rol).filter(Rol.id == usuario.id_rol).first()
            rol_nuevo = db.query(Rol).filter(Rol.id == datos.nuevo_id_rol).first()

            if not rol_nuevo:
                raise HTTPException(status_code=404, detail="Rol nuevo no válido")

            usuario.id_rol = datos.nuevo_id_rol
            db.commit()
            db.refresh(usuario)

            try:
                enviar_correo_cambio_rol(
                    destinatario=usuario.email,
                    nombre=usuario.nombre,
                    apellido=usuario.apellido,
                    rol_anterior=rol_anterior.nombre if rol_anterior else "Desconocido",
                    rol_nuevo=rol_nuevo.nombre
                )
            except Exception as e:
                print(f"Error al enviar correo de cambio de rol: {e}")

            return usuario
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=500, detail=f"Error al cambiar rol: {str(e)}")
