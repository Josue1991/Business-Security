"""
Schemas para Empleado
"""
from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class EmpleadoBase(BaseModel):
    """Base para Empleado"""
    nombre: str
    cedula: str
    telefono: Optional[str] = None
    celular: Optional[str] = None
    domicilio: Optional[str] = None
    nacionalidad: Optional[str] = None
    estado_id: int


class EmpleadoCreate(EmpleadoBase):
    """Crear empleado"""
    # Datos opcionales para crear usuario asociado
    crear_usuario: bool = False
    usuario: Optional[str] = None
    contrasenia: Optional[str] = None
    perfil_id: Optional[int] = None


class EmpleadoUpdate(BaseModel):
    """Actualizar empleado"""
    nombre: Optional[str] = None
    cedula: Optional[str] = None
    telefono: Optional[str] = None
    celular: Optional[str] = None
    domicilio: Optional[str] = None
    nacionalidad: Optional[str] = None
    estado_id: Optional[int] = None


class EmpleadoResponse(EmpleadoBase):
    """Response de empleado"""
    empleado_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True


class EmpleadoConUsuarioResponse(EmpleadoResponse):
    """Response de empleado con información de usuario asociado"""
    tiene_usuario: bool = False
    usuario_id: Optional[int] = None
    nombre_usuario: Optional[str] = None
    usuario_estado: Optional[str] = None
    
    class Config:
        from_attributes = True
