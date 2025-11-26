"""
Schemas para Menu
"""
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class MenuBase(BaseModel):
    """Base para Menu"""
    descripcion: str
    url: Optional[str] = None
    parent_id: Optional[int] = None
    nivel: int = 0
    orden: int = 0
    estado_id: int


class MenuCreate(MenuBase):
    """Crear menú"""
    pass


class MenuUpdate(BaseModel):
    """Actualizar menú"""
    descripcion: Optional[str] = None
    url: Optional[str] = None
    parent_id: Optional[int] = None
    nivel: Optional[int] = None
    orden: Optional[int] = None
    estado_id: Optional[int] = None


class MenuResponse(MenuBase):
    """Response de menú"""
    menu_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True


class MenuTreeResponse(MenuResponse):
    """Response de menú con hijos (recursivo)"""
    children: List['MenuTreeResponse'] = []
    
    class Config:
        from_attributes = True


# Actualizar forward references para recursión
MenuTreeResponse.model_rebuild()
