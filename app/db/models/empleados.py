"""
Modelo Empleados
"""
from sqlalchemy import Column, Integer, String, TIMESTAMP, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db.base import Base


class Empleado(Base):
    __tablename__ = "empleados"
    
    empleado_id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(255), nullable=False)
    cedula = Column(String(50), unique=True, nullable=False)
    telefono = Column(String(50))
    celular = Column(String(50))
    domicilio = Column(String(255))
    nacionalidad = Column(String(100))
    estado_id = Column(Integer, ForeignKey("estado.estado_id"))
    created_at = Column(TIMESTAMP, server_default=func.current_timestamp())
    
    # Relaciones
    estado = relationship("Estado")
    usuario = relationship("Usuario", back_populates="empleado", uselist=False)
