"""
Servicio para CRUD de empleados
"""
from typing import List, Optional
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.db.models.empleados import Empleado
from app.db.models.usuarios import Usuario
from app.db.models.estado import Estado
from app.schemas.empleados import EmpleadoCreate, EmpleadoUpdate
from app.core.security import get_password_hash


class EmpleadoService:
    """Servicio para manejar lógica de empleados"""
    
    @staticmethod
    def get_empleados(db: Session, skip: int = 0, limit: int = 100) -> List[Empleado]:
        """Obtener lista de empleados"""
        return db.query(Empleado).offset(skip).limit(limit).all()
    
    @staticmethod
    def get_empleado_by_id(db: Session, empleado_id: int) -> Optional[Empleado]:
        """Obtener empleado por ID"""
        return db.query(Empleado).filter(Empleado.empleado_id == empleado_id).first()
    
    @staticmethod
    def get_empleado_by_cedula(db: Session, cedula: str) -> Optional[Empleado]:
        """Obtener empleado por cédula"""
        return db.query(Empleado).filter(Empleado.cedula == cedula).first()
    
    @staticmethod
    def create_empleado(db: Session, empleado_data: EmpleadoCreate) -> Empleado:
        """
        Crear nuevo empleado y opcionalmente su usuario
        
        Args:
            db: Sesión de base de datos
            empleado_data: Datos del empleado (puede incluir datos de usuario)
        
        Returns:
            Empleado creado
        
        Raises:
            HTTPException: Si la cédula ya existe o hay error en validaciones
        """
        # Verificar si la cédula ya existe
        existing = EmpleadoService.get_empleado_by_cedula(db, empleado_data.cedula)
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Ya existe un empleado con la cédula {empleado_data.cedula}"
            )
        
        # Crear empleado
        db_empleado = Empleado(
            nombre=empleado_data.nombre,
            cedula=empleado_data.cedula,
            telefono=empleado_data.telefono,
            celular=empleado_data.celular,
            domicilio=empleado_data.domicilio,
            nacionalidad=empleado_data.nacionalidad,
            estado_id=empleado_data.estado_id
        )
        
        db.add(db_empleado)
        db.flush()  # Para obtener el empleado_id antes de commit
        
        # Si se solicita crear usuario
        if empleado_data.crear_usuario:
            if not empleado_data.usuario or not empleado_data.contrasenia or not empleado_data.perfil_id:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Para crear usuario se requiere: usuario, contrasenia y perfil_id"
                )
            
            # Verificar si el nombre de usuario ya existe
            existing_user = db.query(Usuario).filter(Usuario.usuario == empleado_data.usuario).first()
            if existing_user:
                db.rollback()
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"El nombre de usuario '{empleado_data.usuario}' ya existe"
                )
            
            # Crear usuario asociado
            hashed_password = get_password_hash(empleado_data.contrasenia)
            db_usuario = Usuario(
                usuario=empleado_data.usuario,
                contrasenia=hashed_password,
                perfil_id=empleado_data.perfil_id,
                estado_id=empleado_data.estado_id,  # Mismo estado que el empleado
                empleado_id=db_empleado.empleado_id,
                intentos=0
            )
            db.add(db_usuario)
        
        db.commit()
        db.refresh(db_empleado)
        
        return db_empleado
    
    @staticmethod
    def update_empleado(db: Session, empleado_id: int, empleado_data: EmpleadoUpdate) -> Empleado:
        """
        Actualizar empleado
        
        Args:
            db: Sesión de base de datos
            empleado_id: ID del empleado
            empleado_data: Datos a actualizar
        
        Returns:
            Empleado actualizado
        
        Raises:
            HTTPException: Si el empleado no existe o la cédula está duplicada
        """
        db_empleado = EmpleadoService.get_empleado_by_id(db, empleado_id)
        if not db_empleado:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Empleado no encontrado"
            )
        
        # Si se actualiza la cédula, verificar que no exista
        if empleado_data.cedula and empleado_data.cedula != db_empleado.cedula:
            existing = EmpleadoService.get_empleado_by_cedula(db, empleado_data.cedula)
            if existing:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Ya existe un empleado con la cédula {empleado_data.cedula}"
                )
        
        # Actualizar campos
        update_data = empleado_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_empleado, field, value)
        
        # Si se cambia el estado del empleado, actualizar el estado de su usuario
        if empleado_data.estado_id:
            usuario = db.query(Usuario).filter(Usuario.empleado_id == empleado_id).first()
            if usuario:
                usuario.estado_id = empleado_data.estado_id
        
        db.commit()
        db.refresh(db_empleado)
        
        return db_empleado
    
    @staticmethod
    def delete_empleado(db: Session, empleado_id: int):
        """
        Eliminar (desactivar) empleado y su usuario asociado
        
        Args:
            db: Sesión de base de datos
            empleado_id: ID del empleado
        
        Raises:
            HTTPException: Si el empleado no existe
        """
        db_empleado = EmpleadoService.get_empleado_by_id(db, empleado_id)
        if not db_empleado:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Empleado no encontrado"
            )
        
        # Desactivar empleado (estado_id = 2, asumiendo 2 = Inactivo)
        db_empleado.estado_id = 2
        
        # Desactivar usuario asociado si existe
        usuario = db.query(Usuario).filter(Usuario.empleado_id == empleado_id).first()
        if usuario:
            usuario.estado_id = 2
        
        db.commit()
    
    @staticmethod
    def get_empleado_con_usuario(db: Session, empleado_id: int) -> dict:
        """
        Obtener empleado con información de su usuario asociado
        
        Args:
            db: Sesión de base de datos
            empleado_id: ID del empleado
        
        Returns:
            Diccionario con datos del empleado y usuario
        """
        empleado = EmpleadoService.get_empleado_by_id(db, empleado_id)
        if not empleado:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Empleado no encontrado"
            )
        
        # Buscar usuario asociado
        usuario = db.query(Usuario).filter(Usuario.empleado_id == empleado_id).first()
        
        # Construir respuesta
        response = {
            "empleado_id": empleado.empleado_id,
            "nombre": empleado.nombre,
            "cedula": empleado.cedula,
            "telefono": empleado.telefono,
            "celular": empleado.celular,
            "domicilio": empleado.domicilio,
            "nacionalidad": empleado.nacionalidad,
            "estado_id": empleado.estado_id,
            "created_at": empleado.created_at,
            "tiene_usuario": usuario is not None,
            "usuario_id": usuario.usuario_id if usuario else None,
            "nombre_usuario": usuario.usuario if usuario else None,
            "usuario_estado": self._get_estado_descripcion(db, usuario.estado_id) if usuario else None
        }
        
        return response
    
    @staticmethod
    def _get_estado_descripcion(db: Session, estado_id: int) -> str:
        """Obtener descripción del estado"""
        estado = db.query(Estado).filter(Estado.estado_id == estado_id).first()
        return estado.descripcion if estado else "Desconocido"
