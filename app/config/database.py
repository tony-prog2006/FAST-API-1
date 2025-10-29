from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# URL de conexión a MySQL usando PyMySQL
DATABASE_URL = "mysql+pymysql://root:@localhost/propuesta_proyecto"

# Crear el motor de conexión
engine = create_engine(DATABASE_URL)

# Crear la sesión para interactuar con la base de datos
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

# Base para los modelos ORM
Base = declarative_base()
