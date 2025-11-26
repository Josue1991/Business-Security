"""Verificar conexión PostgreSQL con SQLAlchemy"""
from sqlalchemy import create_engine, text, inspect
import os
import sys

# Configurar encoding
if sys.platform == 'win32':
    os.environ['PYTHONUTF8'] = '1'

# URL de conexión (psycopg3)
database_url = "postgresql+psycopg://postgres:jocr1991@localhost:5432/Auth"

print("🔄 Intentando conectar a PostgreSQL con SQLAlchemy...")
print(f"📡 URL: {database_url.replace('postgres', '***')}")

try:
    # Crear engine con configuración robusta
    engine = create_engine(
        database_url,
        connect_args={
            "client_encoding": "utf8",
            "options": "-c client_encoding=utf8"
        },
        pool_pre_ping=True,
        echo=False
    )
    
    # Probar conexión
    with engine.connect() as conn:
        result = conn.execute(text("SELECT version()"))
        version = result.fetchone()[0]
        print(f"✅ Conexión exitosa!")
        print(f"📊 PostgreSQL: {version.split(',')[0]}")
        
    # Inspeccionar tablas
    inspector = inspect(engine)
    tables = inspector.get_table_names()
    
    if tables:
        print(f"\n📋 Tablas encontradas ({len(tables)}):")
        for table in tables:
            columns = inspector.get_columns(table)
            print(f"  - {table:<20} ({len(columns)} columnas)")
    else:
        print("\n⚠️  Base de datos vacía - no hay tablas")
        print("💡 Ejecutar: alembic upgrade head")
        
    engine.dispose()
    print("\n✅ Todo OK - Configuración lista para usar")
    
except Exception as e:
    print(f"\n❌ Error: {type(e).__name__}")
    print(f"   {str(e)}")
    print("\n💡 Posibles soluciones:")
    print("  1. Verificar que PostgreSQL esté corriendo")
    print("  2. Verificar credenciales (user: user, password: postgres)")
    print("  3. Verificar que existe la base de datos 'Auth'")
    print("  4. Crear la BD: CREATE DATABASE \"Auth\";")
    sys.exit(1)
