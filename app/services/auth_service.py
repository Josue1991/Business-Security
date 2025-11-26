"""
Servicio de autenticación
"""
from typing import Optional
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.db.models.usuarios import Usuario
from app.core.security import verify_password, get_password_hash
from app.core.config import settings


class AuthService:
    """Servicio para manejar lógica de autenticación"""
    
    @staticmethod
    def authenticate_user(db: Session, usuario: str, contrasenia: str) -> Optional[Usuario]:
        """
        Autenticar usuario
        
        Args:
            db: Sesión de base de datos
            usuario: Nombre de usuario
            contrasenia: Contraseña en texto plano
        
        Returns:
            Usuario si las credenciales son válidas
        
        Raises:
            HTTPException: Si las credenciales son inválidas o el usuario está bloqueado
        """
        # Buscar usuario
        user = db.query(Usuario).filter(Usuario.usuario == usuario).first()
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Usuario o contraseña incorrectos"
            )
        
        # Verificar si está bloqueado
        if user.intentos >= settings.MAX_LOGIN_ATTEMPTS:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Usuario bloqueado. Máximo {settings.MAX_LOGIN_ATTEMPTS} intentos fallidos"
            )
        
        # Verificar si el usuario está activo (estado_id = 1)
        if user.estado_id != 1:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Usuario inactivo"
            )
        
        # Verificar contraseña
        if not verify_password(contrasenia, user.contrasenia):
            # Incrementar intentos fallidos
            user.intentos += 1
            db.commit()
            
            intentos_restantes = settings.MAX_LOGIN_ATTEMPTS - user.intentos
            if intentos_restantes > 0:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail=f"Usuario o contraseña incorrectos. Intentos restantes: {intentos_restantes}"
                )
            else:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail=f"Usuario bloqueado. Máximo {settings.MAX_LOGIN_ATTEMPTS} intentos fallidos"
                )
        
        # Login exitoso: resetear intentos
        if user.intentos > 0:
            user.intentos = 0
            db.commit()
        
        return user
    
    @staticmethod
    def change_password(db: Session, usuario_id: int, contrasenia_actual: str, contrasenia_nueva: str):
        """
        Cambiar contraseña de usuario
        
        Args:
            db: Sesión de base de datos
            usuario_id: ID del usuario
            contrasenia_actual: Contraseña actual
            contrasenia_nueva: Nueva contraseña
        
        Raises:
            HTTPException: Si la contraseña actual es incorrecta
        """
        user = db.query(Usuario).filter(Usuario.usuario_id == usuario_id).first()
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Usuario no encontrado"
            )
        
        # Verificar contraseña actual
        if not verify_password(contrasenia_actual, user.contrasenia):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Contraseña actual incorrecta"
            )
        
        # Actualizar contraseña
        user.contrasenia = get_password_hash(contrasenia_nueva)
        db.commit()
    
    @staticmethod
    def reset_login_attempts(db: Session, usuario_id: int):
        """
        Resetear intentos de login de un usuario (para admins)
        """
        user = db.query(Usuario).filter(Usuario.usuario_id == usuario_id).first()
        if user:
            user.intentos = 0
            db.commit()
