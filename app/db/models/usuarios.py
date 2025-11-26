"""
Modelo Usuario
"""
from sqlalchemy import Column, Integer, String, TIMESTAMP, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db.base import Base


class Usuario(Base):
    __tablename__ = "usuarios"
    
    usuario_id = Column(Integer, primary_key=True, index=True)
    usuario = Column(String(255), unique=True, nullable=False, index=True)
    contrasenia = Column(String(255), nullable=False)  # Almacenar hash
    perfil_id = Column(Integer, ForeignKey("perfil.perfil_id"))
    estado_id = Column(Integer, ForeignKey("estado.estado_id"))
    empleado_id = Column(Integer, ForeignKey("empleados.empleado_id"))
    intentos = Column(Integer, default=0)
    created_at = Column(TIMESTAMP, server_default=func.current_timestamp())
    
    # Relaciones
    perfil = relationship("Perfil", back_populates="usuarios")
    estado = relationship("Estado")
    empleado = relationship("Empleado", back_populates="usuario")
