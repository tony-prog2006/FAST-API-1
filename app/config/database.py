import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv

# Cargar variables del archivo .env
load_dotenv()

# Leer variables de entorno de Clever Cloud
DB_HOST = os.getenv("MYSQL_ADDON_HOST")
DB_PORT = os.getenv("MYSQL_ADDON_PORT", "3306")
DB_USER = os.getenv("MYSQL_ADDON_USER")
DB_PASSWORD = os.getenv("MYSQL_ADDON_PASSWORD")
DB_NAME = os.getenv("MYSQL_ADDON_DB")

# Construir la URL de conexión
DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Crear el motor de conexión
engine = create_engine(DATABASE_URL)

# Crear la sesión para interactuar con la base de datos
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

# Base para los modelos ORM
Base = declarative_base()
