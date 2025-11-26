"""
Script de seed para poblar la base de datos con datos iniciales
Ejecutar: python seed_db.py
"""
import sys
from datetime import datetime
from sqlalchemy.orm import Session
from app.db.session import SessionLocal, engine
from app.db.base import Base
from app.db.models.estado import Estado
from app.db.models.perfil import Perfil
from app.db.models.menu import Menu
from app.db.models.empleados import Empleado
from app.db.models.usuarios import Usuario
from app.core.security import get_password_hash


def seed_estados(db: Session):
    """Crear estados básicos"""
    estados = [
        {"estado_id": 1, "descripcion": "Activo"},
        {"estado_id": 2, "descripcion": "Inactivo"},
        {"estado_id": 3, "descripcion": "Bloqueado"},
    ]
    
    for estado_data in estados:
        estado = db.query(Estado).filter(Estado.estado_id == estado_data["estado_id"]).first()
        if not estado:
            estado = Estado(**estado_data)
            db.add(estado)
            print(f"✅ Estado creado: {estado_data['descripcion']}")
    
    db.commit()


def seed_perfiles(db: Session):
    """Crear perfiles básicos"""
    perfiles = [
        {"perfil_id": 1, "descripcion": "Administrador", "estado_id": 1},
        {"perfil_id": 2, "descripcion": "Usuario", "estado_id": 1},
        {"perfil_id": 3, "descripcion": "Supervisor", "estado_id": 1},
    ]
    
    for perfil_data in perfiles:
        perfil = db.query(Perfil).filter(Perfil.perfil_id == perfil_data["perfil_id"]).first()
        if not perfil:
            perfil = Perfil(**perfil_data)
            db.add(perfil)
            print(f"✅ Perfil creado: {perfil_data['descripcion']}")
    
    db.commit()


def seed_menu(db: Session):
    """Crear estructura de menú"""
    menus = [
        # Nivel 1 - Menús principales
        {"menu_id": 1, "descripcion": "Dashboard", "url": "/dashboard", "parent_id": None, "nivel": 1, "orden": 1, "estado_id": 1},
        {"menu_id": 2, "descripcion": "Seguridad", "url": None, "parent_id": None, "nivel": 1, "orden": 2, "estado_id": 1},
        {"menu_id": 3, "descripcion": "RRHH", "url": None, "parent_id": None, "nivel": 1, "orden": 3, "estado_id": 1},
        {"menu_id": 4, "descripcion": "Reportes", "url": "/reportes", "parent_id": None, "nivel": 1, "orden": 4, "estado_id": 1},
        
        # Nivel 2 - Submenús de Seguridad
        {"menu_id": 5, "descripcion": "Usuarios", "url": "/seguridad/usuarios", "parent_id": 2, "nivel": 2, "orden": 1, "estado_id": 1},
        {"menu_id": 6, "descripcion": "Perfiles", "url": "/seguridad/perfiles", "parent_id": 2, "nivel": 2, "orden": 2, "estado_id": 1},
        {"menu_id": 7, "descripcion": "Menú", "url": "/seguridad/menu", "parent_id": 2, "nivel": 2, "orden": 3, "estado_id": 1},
        
        # Nivel 2 - Submenús de RRHH
        {"menu_id": 8, "descripcion": "Empleados", "url": "/rrhh/empleados", "parent_id": 3, "nivel": 2, "orden": 1, "estado_id": 1},
        {"menu_id": 9, "descripcion": "Departamentos", "url": "/rrhh/departamentos", "parent_id": 3, "nivel": 2, "orden": 2, "estado_id": 1},
    ]
    
    for menu_data in menus:
        menu = db.query(Menu).filter(Menu.menu_id == menu_data["menu_id"]).first()
        if not menu:
            menu = Menu(**menu_data)
            db.add(menu)
            print(f"✅ Menú creado: {menu_data['descripcion']}")
    
    db.commit()


def seed_perfil_menu(db: Session):
    """Asignar menús a perfiles"""
    # Administrador tiene acceso a todo
    admin_perfil = db.query(Perfil).filter(Perfil.perfil_id == 1).first()
    if admin_perfil:
        todos_menus = db.query(Menu).all()
        admin_perfil.menus = todos_menus
        print(f"✅ Asignados {len(todos_menus)} menús al perfil Administrador")
    
    # Usuario tiene acceso limitado
    usuario_perfil = db.query(Perfil).filter(Perfil.perfil_id == 2).first()
    if usuario_perfil:
        menus_usuario = db.query(Menu).filter(Menu.menu_id.in_([1, 4, 8])).all()  # Dashboard, Reportes, Empleados
        usuario_perfil.menus = menus_usuario
        print(f"✅ Asignados {len(menus_usuario)} menús al perfil Usuario")
    
    db.commit()


def seed_empleados(db: Session):
    """Crear empleados de ejemplo"""
    empleados = [
        {
            "empleado_id": 1,
            "nombre": "Juan Pérez",
            "cedula": "1234567",
            "telefono": "021-123456",
            "celular": "0981-123456",
            "domicilio": "Asunción",
            "nacionalidad": "Paraguaya",
            "estado_id": 1
        },
        {
            "empleado_id": 2,
            "nombre": "María González",
            "cedula": "7654321",
            "telefono": "021-654321",
            "celular": "0981-654321",
            "domicilio": "Asunción",
            "nacionalidad": "Paraguaya",
            "estado_id": 1
        },
    ]
    
    for emp_data in empleados:
        empleado = db.query(Empleado).filter(Empleado.cedula == emp_data["cedula"]).first()
        if not empleado:
            empleado = Empleado(**emp_data)
            db.add(empleado)
            print(f"✅ Empleado creado: {emp_data['nombre']}")
    
    db.commit()


def seed_usuarios(db: Session):
    """Crear usuarios de ejemplo"""
    usuarios = [
        {
            "usuario_id": 1,
            "usuario": "admin",
            "contrasenia": get_password_hash("admin123"),
            "perfil_id": 1,
            "estado_id": 1,
            "empleado_id": 1,
            "intentos": 0
        },
        {
            "usuario_id": 2,
            "usuario": "usuario",
            "contrasenia": get_password_hash("usuario123"),
            "perfil_id": 2,
            "estado_id": 1,
            "empleado_id": 2,
            "intentos": 0
        },
    ]
    
    for user_data in usuarios:
        usuario = db.query(Usuario).filter(Usuario.usuario == user_data["usuario"]).first()
        if not usuario:
            usuario = Usuario(**user_data)
            db.add(usuario)
            print(f"✅ Usuario creado: {user_data['usuario']}")
    
    db.commit()


def main():
    """Función principal"""
    print("🌱 Iniciando seed de base de datos...")
    print("=" * 60)
    
    db = SessionLocal()
    
    try:
        # Verificar conexión
        print("🔍 Verificando conexión a base de datos...")
        from sqlalchemy import text
        db.execute(text("SELECT 1"))
        print("✅ Conexión exitosa\n")
        
        # Ejecutar seeds en orden
        print("📊 Creando Estados...")
        seed_estados(db)
        print()
        
        print("👥 Creando Perfiles...")
        seed_perfiles(db)
        print()
        
        print("📋 Creando Menú...")
        seed_menu(db)
        print()
        
        print("🔗 Asignando Menús a Perfiles...")
        seed_perfil_menu(db)
        print()
        
        print("👤 Creando Empleados...")
        seed_empleados(db)
        print()
        
        print("🔐 Creando Usuarios...")
        seed_usuarios(db)
        print()
        
        print("=" * 60)
        print("✅ Seed completado exitosamente!")
        print("\n📝 Usuarios creados:")
        print("   - admin / admin123 (Administrador)")
        print("   - usuario / usuario123 (Usuario)")
        
    except Exception as e:
        print(f"\n❌ Error durante el seed: {str(e)}")
        db.rollback()
        sys.exit(1)
    finally:
        db.close()


if __name__ == "__main__":
    main()
