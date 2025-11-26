"""
Modelo Perfil
"""
from sqlalchemy import Column, Integer, String, TIMESTAMP, ForeignKey, Table
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db.base import Base

# Tabla de relación N:N entre Perfil y Menu
perfil_menu = Table(
    'perfil_menu',
    Base.metadata,
    Column('perfil_id', Integer, ForeignKey('perfil.perfil_id'), primary_key=True),
    Column('menu_id', Integer, ForeignKey('menu.menu_id'), primary_key=True)
)


class Perfil(Base):
    __tablename__ = "perfil"
    
    perfil_id = Column(Integer, primary_key=True, index=True)
    descripcion = Column(String(255), nullable=False)
    estado_id = Column(Integer, ForeignKey("estado.estado_id"))
    created_at = Column(TIMESTAMP, server_default=func.current_timestamp())
    
    # Relaciones
    estado = relationship("Estado")
    usuarios = relationship("Usuario", back_populates="perfil")
    menus = relationship("Menu", secondary=perfil_menu, back_populates="perfiles")
