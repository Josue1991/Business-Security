"""
Schemas para Perfil
"""
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class PerfilBase(BaseModel):
    """Base para Perfil"""
    descripcion: str
    estado_id: int


class PerfilCreate(PerfilBase):
    """Crear perfil"""
    pass


class PerfilUpdate(BaseModel):
    """Actualizar perfil"""
    descripcion: Optional[str] = None
    estado_id: Optional[int] = None


class PerfilResponse(PerfilBase):
    """Response de perfil"""
    perfil_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True


class PerfilMenuAssign(BaseModel):
    """Asignar menús a un perfil"""
    menu_ids: List[int]
