"""
Servicio para CRUD de usuarios
"""
from typing import List, Optional
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.db.models.usuarios import Usuario
from app.schemas.usuarios import UsuarioCreate, UsuarioUpdate
from app.core.security import get_password_hash


class UsuarioService:
    """Servicio para manejar lógica de usuarios"""
    
    @staticmethod
    def get_usuarios(db: Session, skip: int = 0, limit: int = 100) -> List[Usuario]:
        """Obtener lista de usuarios"""
        return db.query(Usuario).offset(skip).limit(limit).all()
    
    @staticmethod
    def get_usuario_by_id(db: Session, usuario_id: int) -> Optional[Usuario]:
        """Obtener usuario por ID"""
        return db.query(Usuario).filter(Usuario.usuario_id == usuario_id).first()
    
    @staticmethod
    def get_usuario_by_username(db: Session, usuario: str) -> Optional[Usuario]:
        """Obtener usuario por nombre de usuario"""
        return db.query(Usuario).filter(Usuario.usuario == usuario).first()
    
    @staticmethod
    def create_usuario(db: Session, usuario_data: UsuarioCreate) -> Usuario:
        """
        Crear nuevo usuario
        
        Args:
            db: Sesión de base de datos
            usuario_data: Datos del usuario
        
        Returns:
            Usuario creado
        
        Raises:
            HTTPException: Si el usuario ya existe
        """
        # Verificar si el usuario ya existe
        existing = UsuarioService.get_usuario_by_username(db, usuario_data.usuario)
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El usuario ya existe"
            )
        
        # Hashear contraseña
        hashed_password = get_password_hash(usuario_data.contrasenia)
        
        # Crear usuario
        db_usuario = Usuario(
            usuario=usuario_data.usuario,
            contrasenia=hashed_password,
            perfil_id=usuario_data.perfil_id,
            estado_id=usuario_data.estado_id,
            empleado_id=usuario_data.empleado_id,
            intentos=0
        )
        
        db.add(db_usuario)
        db.commit()
        db.refresh(db_usuario)
        
        return db_usuario
    
    @staticmethod
    def update_usuario(db: Session, usuario_id: int, usuario_data: UsuarioUpdate) -> Usuario:
        """
        Actualizar usuario
        
        Args:
            db: Sesión de base de datos
            usuario_id: ID del usuario
            usuario_data: Datos a actualizar
        
        Returns:
            Usuario actualizado
        
        Raises:
            HTTPException: Si el usuario no existe
        """
        db_usuario = UsuarioService.get_usuario_by_id(db, usuario_id)
        if not db_usuario:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Usuario no encontrado"
            )
        
        # Actualizar campos
        update_data = usuario_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_usuario, field, value)
        
        db.commit()
        db.refresh(db_usuario)
        
        return db_usuario
    
    @staticmethod
    def delete_usuario(db: Session, usuario_id: int):
        """
        Eliminar (desactivar) usuario
        
        Args:
            db: Sesión de base de datos
            usuario_id: ID del usuario
        
        Raises:
            HTTPException: Si el usuario no existe
        """
        db_usuario = UsuarioService.get_usuario_by_id(db, usuario_id)
        if not db_usuario:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Usuario no encontrado"
            )
        
        # En lugar de eliminar, desactivar
        db_usuario.estado_id = 2  # Asumiendo 2 = Inactivo
        db.commit()
