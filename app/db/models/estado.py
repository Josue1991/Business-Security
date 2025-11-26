"""
Modelo Estado
"""
from sqlalchemy import Column, Integer, String, TIMESTAMP
from sqlalchemy.sql import func
from app.db.base import Base


class Estado(Base):
    __tablename__ = "estado"
    
    estado_id = Column(Integer, primary_key=True, index=True)
    descripcion = Column(String(255), nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.current_timestamp())
