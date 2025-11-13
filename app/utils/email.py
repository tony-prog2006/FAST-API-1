from email.message import EmailMessage
import smtplib
import os
from dotenv import load_dotenv

load_dotenv()

EMAIL_HOST = os.getenv("EMAIL_HOST")
EMAIL_PORT = int(os.getenv("EMAIL_PORT"))
EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")

def enviar_correo_bienvenida(destinatario: str, nombre: str, apellido: str):
    mensaje = EmailMessage()
    mensaje["Subject"] = "¡Bienvenido a la plataforma!"
    mensaje["From"] = EMAIL_USER
    mensaje["To"] = destinatario
    mensaje.set_content(f"""
Hola {nombre} {apellido},

Gracias por registrarte en nuestra plataforma Aqualis. Estamos felices de tenerte con nosotros.

Saludos del equipo de Aqualis...
""")

    with smtplib.SMTP(EMAIL_HOST, EMAIL_PORT) as smtp:
        smtp.starttls()
        smtp.login(EMAIL_USER, EMAIL_PASSWORD)
        smtp.send_message(mensaje)

def enviar_correo_cambio_rol(destinatario: str, nombre: str, apellido: str, rol_anterior: str, rol_nuevo: str):
    mensaje = EmailMessage()
    mensaje["Subject"] = "Notificación de cambio de rol"
    mensaje["From"] = EMAIL_USER
    mensaje["To"] = destinatario
    mensaje.set_content(f"""
Hola {nombre} {apellido},

Te informamos que tu rol en la plataforma Aqualis ha sido actualizado:

Rol anterior: {rol_anterior}
Nuevo rol: {rol_nuevo}

Si tienes alguna duda, no dudes en contactarnos.

Saludos del equipo de Aqualis.
""")

    with smtplib.SMTP(EMAIL_HOST, EMAIL_PORT) as smtp:
        smtp.starttls()
        smtp.login(EMAIL_USER, EMAIL_PASSWORD)
        smtp.send_message(mensaje)
