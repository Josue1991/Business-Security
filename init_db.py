"""
Script para inicializar la base de datos con datos de ejemplo
"""
from app.db.base import Base
from app.db.session import engine
from app.db.models.estado import Estado
from app.db.models.perfil import Perfil
from app.db.models.empleados import Empleado
from app.db.models.usuarios import Usuario
from app.db.models.menu import Menu
from app.core.security import get_password_hash
from sqlalchemy.orm import Session


def init_db():
    """Crear todas las tablas"""
    print("Creando tablas...")
    Base.metadata.create_all(bind=engine)
    print("✓ Tablas creadas")


def seed_data():
    """Insertar datos de ejemplo"""
    print("Insertando datos de ejemplo...")
    
    with Session(engine) as db:
        # Estados
        estados = [
            Estado(estado_id=1, descripcion="Activo"),
            Estado(estado_id=2, descripcion="Inactivo"),
            Estado(estado_id=3, descripcion="Bloqueado")
        ]
        db.add_all(estados)
        db.commit()
        print("✓ Estados insertados")
        
        # Perfiles
        perfiles = [
            Perfil(perfil_id=1, descripcion="Administrador", estado_id=1),
            Perfil(perfil_id=2, descripcion="Usuario", estado_id=1),
            Perfil(perfil_id=3, descripcion="Supervisor", estado_id=1)
        ]
        db.add_all(perfiles)
        db.commit()
        print("✓ Perfiles insertados")
        
        # Empleados
        empleados = [
            Empleado(
                empleado_id=1,
                nombre="Admin Principal",
                cedula="1234567",
                telefono="021-123456",
                celular="0981-123456",
                domicilio="Asunción",
                nacionalidad="Paraguaya",
                estado_id=1
            ),
            Empleado(
                empleado_id=2,
                nombre="Usuario Demo",
                cedula="7654321",
                telefono="021-654321",
                celular="0981-654321",
                domicilio="Asunción",
                nacionalidad="Paraguaya",
                estado_id=1
            )
        ]
        db.add_all(empleados)
        db.commit()
        print("✓ Empleados insertados")
        
        # Usuarios (contraseña por defecto: "password123")
        usuarios = [
            Usuario(
                usuario_id=1,
                usuario="admin",
                contrasenia=get_password_hash("password123"),
                perfil_id=1,
                estado_id=1,
                empleado_id=1,
                intentos=0
            ),
            Usuario(
                usuario_id=2,
                usuario="usuario",
                contrasenia=get_password_hash("password123"),
                perfil_id=2,
                estado_id=1,
                empleado_id=2,
                intentos=0
            )
        ]
        db.add_all(usuarios)
        db.commit()
        print("✓ Usuarios insertados (contraseña: password123)")
        
        # Menús
        menus = [
            # Nivel 0 (raíz)
            Menu(menu_id=1, descripcion="Dashboard", url="/dashboard", parent_id=None, nivel=0, orden=1, estado_id=1),
            Menu(menu_id=2, descripcion="Usuarios", url="/usuarios", parent_id=None, nivel=0, orden=2, estado_id=1),
            Menu(menu_id=3, descripcion="Configuración", url=None, parent_id=None, nivel=0, orden=3, estado_id=1),
            
            # Nivel 1 (hijos de Usuarios)
            Menu(menu_id=4, descripcion="Lista de Usuarios", url="/usuarios/lista", parent_id=2, nivel=1, orden=1, estado_id=1),
            Menu(menu_id=5, descripcion="Perfiles", url="/usuarios/perfiles", parent_id=2, nivel=1, orden=2, estado_id=1),
            
            # Nivel 1 (hijos de Configuración)
            Menu(menu_id=6, descripcion="Sistema", url="/config/sistema", parent_id=3, nivel=1, orden=1, estado_id=1),
            Menu(menu_id=7, descripcion="Menú", url="/config/menu", parent_id=3, nivel=1, orden=2, estado_id=1),
        ]
        db.add_all(menus)
        db.commit()
        print("✓ Menús insertados")
        
        # Asignar todos los menús al perfil Admin
        perfil_admin = db.query(Perfil).filter(Perfil.perfil_id == 1).first()
        perfil_admin.menus = menus
        
        # Asignar solo Dashboard al perfil Usuario
        perfil_usuario = db.query(Perfil).filter(Perfil.perfil_id == 2).first()
        perfil_usuario.menus = [menus[0]]  # Solo Dashboard
        
        db.commit()
        print("✓ Menús asignados a perfiles")
    
    print("\n✅ Base de datos inicializada correctamente")
    print("\nCredenciales de prueba:")
    print("  Usuario: admin | Contraseña: password123")
    print("  Usuario: usuario | Contraseña: password123")


if __name__ == "__main__":
    print("=== Inicialización de Base de Datos ===\n")
    init_db()
    seed_data()
