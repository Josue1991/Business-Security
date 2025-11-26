"""Script temporal para verificar conexión PostgreSQL"""
import psycopg2
import os
import sys

# Forzar encoding UTF-8
if sys.platform == 'win32':
    os.environ['PYTHONUTF8'] = '1'

# Eliminar variables que causan problemas con rutas
for var in ['HOME', 'USERPROFILE', 'APPDATA', 'PGPASSFILE', 'PGSERVICEFILE', 'PGSYSCONFDIR']:
    os.environ.pop(var, None)

# Configurar encoding de PostgreSQL
os.environ['PGCLIENTENCODING'] = 'UTF8'

try:
    # Conectar usando parámetros individuales
    conn = psycopg2.connect(
        host='localhost',
        port=5432,
        dbname='Auth',
        user='user',
        password='postgres',
        client_encoding='utf8',
        options='-c client_encoding=UTF8'
    )
    
    print('✅ Conexión exitosa a PostgreSQL')
    print(f'📊 Base de datos: Auth')
    
    cursor = conn.cursor()
    
    # Listar tablas
    cursor.execute("""
        SELECT table_name 
        FROM information_schema.tables 
        WHERE table_schema='public' 
        ORDER BY table_name
    """)
    
    tables = cursor.fetchall()
    
    if tables:
        print(f'\n📋 Tablas encontradas ({len(tables)}):')
        for table in tables:
            # Obtener cantidad de registros
            cursor.execute(f'SELECT COUNT(*) FROM {table[0]}')
            count = cursor.fetchone()[0]
            print(f'  - {table[0]:<20} ({count} registros)')
    else:
        print('\n⚠️  No se encontraron tablas en la base de datos')
        print('💡 Necesitas ejecutar: alembic upgrade head')
    
    cursor.close()
    conn.close()
    
except psycopg2.Error as e:
    print(f'❌ Error de conexión: {e}')
    print('\n💡 Verifica:')
    print('  - PostgreSQL está corriendo')
    print('  - Usuario: user')
    print('  - Password: postgres')
    print('  - Base de datos: Auth existe')
except Exception as e:
    print(f'❌ Error inesperado: {e}')
