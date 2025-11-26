"""
Configuración de la sesión de base de datos con SQLAlchemy
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

# Configurar connect_args según el tipo de base de datos
connect_args = {}
if "sqlite" in settings.DATABASE_URL:
    connect_args = {"check_same_thread": False}
elif "postgresql" in settings.DATABASE_URL:
    connect_args = {
        "client_encoding": "utf8",
        "connect_timeout": 10
    }

# Crear engine de SQLAlchemy
engine = create_engine(
    settings.DATABASE_URL,
    connect_args=connect_args,
    pool_pre_ping=True,  # Verificar conexión antes de usar
    echo=False  # Cambiar a True para debug SQL
)

# Crear SessionLocal class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
