"""
Modelo Menu (recursivo)
"""
from sqlalchemy import Column, Integer, String, TIMESTAMP, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db.base import Base
from app.db.models.perfil import perfil_menu


class Menu(Base):
    __tablename__ = "menu"
    
    menu_id = Column(Integer, primary_key=True, index=True)
    descripcion = Column(String(255), nullable=False)
    url = Column(String(255))
    parent_id = Column(Integer, ForeignKey("menu.menu_id"), nullable=True)
    nivel = Column(Integer, nullable=False, default=0)
    orden = Column(Integer, nullable=False, default=0)
    estado_id = Column(Integer, ForeignKey("estado.estado_id"))
    created_at = Column(TIMESTAMP, server_default=func.current_timestamp())
    
    # Relaciones
    estado = relationship("Estado")
    perfiles = relationship("Perfil", secondary=perfil_menu, back_populates="menus")
    
    # Relación recursiva para el menú jerárquico
    parent = relationship("Menu", remote_side=[menu_id], backref="children")
