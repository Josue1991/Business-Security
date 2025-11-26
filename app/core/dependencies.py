"""
Dependencias comunes de FastAPI: DB session, autenticación, etc.
"""
from typing import Generator, Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.core.security import decode_access_token
from app.db.models.usuarios import Usuario

# OAuth2 con Bearer token
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")


def get_db() -> Generator:
    """
    Dependencia para obtener una sesión de base de datos
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> Usuario:
    """
    Obtener el usuario actual desde el token JWT
    
    Raises:
        HTTPException: Si el token es inválido o el usuario no existe/no está activo
    
    Returns:
        Usuario autenticado
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No se pudo validar las credenciales",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    # Decodificar token
    payload = decode_access_token(token)
    if payload is None:
        raise credentials_exception
    
    usuario_id: Optional[int] = payload.get("sub")
    if usuario_id is None:
        raise credentials_exception
    
    # Buscar usuario en DB
    usuario = db.query(Usuario).filter(Usuario.usuario_id == usuario_id).first()
    if usuario is None:
        raise credentials_exception
    
    # Verificar que el usuario esté activo (estado_id = 1, por ejemplo)
    if usuario.estado_id != 1:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Usuario inactivo o bloqueado"
        )
    
    return usuario


async def get_current_active_user(
    current_user: Usuario = Depends(get_current_user)
) -> Usuario:
    """
    Verificar que el usuario actual esté activo
    """
    # Aquí puedes agregar más validaciones si es necesario
    return current_user
