import sys
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi

# Aseguramos que el directorio raíz esté en el path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Importamos todos los modelos para que SQLAlchemy los registre
from app.models.usuario_model import Usuario
from app.models.rol_model import Rol
from app.models.modulo_model import Modulo
from app.models.rolmodulo_model import RolModulo

# Importamos los routers existentes
from app.routes.user_routes import router as user_router
from app.routes.rol_routes import router as rol_router
from app.routes.auth_routes import router as auth_router

# Importamos los routers por módulo
from app.routes.sensor_routes import router as sensor_router
from app.routes.alerta_routes import router as alerta_router
from app.routes.dashboard_routes import router as dashboard_router
from app.routes.modulo_routes import router as modulo_router
from app.routes.rolmodulo_routes import router as rolmodulo_router  # ✅ Nuevo router para asignación de módulos

# Creamos la instancia principal de la aplicación FastAPI
app = FastAPI(debug=True)

# Configuración del middleware CORS
origins = ["http://localhost"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# Registramos las rutas
app.include_router(user_router)
app.include_router(rol_router)
app.include_router(auth_router)
app.include_router(sensor_router)
app.include_router(alerta_router)
app.include_router(dashboard_router)
app.include_router(modulo_router)
app.include_router(rolmodulo_router)  # ✅ Registro del nuevo router

# Configuración personalizada de Swagger con autenticación JWT
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="API con JWT",
        version="1.0.0",
        description="Documentación de la API protegida con autenticación JWT",
        routes=app.routes,
    )
    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT"
        }
    }
    for path in openapi_schema["paths"].values():
        for method in path.values():
            method["security"] = [{"BearerAuth": []}]
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

# Ejecutamos el servidor si se llama directamente
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
