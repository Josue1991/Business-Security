"""
Schemas para Usuario
"""
from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class UsuarioBase(BaseModel):
    """Base para Usuario"""
    usuario: str
    perfil_id: int
    estado_id: int
    empleado_id: int


class UsuarioCreate(UsuarioBase):
    """Crear usuario"""
    contrasenia: str


class UsuarioUpdate(BaseModel):
    """Actualizar usuario"""
    usuario: Optional[str] = None
    perfil_id: Optional[int] = None
    estado_id: Optional[int] = None
    empleado_id: Optional[int] = None


class UsuarioResponse(UsuarioBase):
    """Response de usuario (sin contraseña)"""
    usuario_id: int
    intentos: int
    created_at: datetime
    
    class Config:
        from_attributes = True


class UsuarioMeResponse(BaseModel):
    """Response de usuario actual con datos de empleado"""
    usuario_id: int
    usuario: str
    perfil_id: int
    estado_id: int
    empleado_id: int
    intentos: int
    empleado_nombre: Optional[str] = None
    perfil_descripcion: Optional[str] = None
    
    class Config:
        from_attributes = True
