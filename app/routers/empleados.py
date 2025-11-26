"""
Router de empleados
"""
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.dependencies import get_db, get_current_active_user
from app.schemas.empleados import (
    EmpleadoCreate, 
    EmpleadoUpdate, 
    EmpleadoResponse,
    EmpleadoConUsuarioResponse
)
from app.services.empleado_service import EmpleadoService
from app.db.models.usuarios import Usuario

router = APIRouter()


@router.get("/", response_model=List[EmpleadoResponse])
async def get_empleados(
    skip: int = 0,
    limit: int = 100,
    current_user: Usuario = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Obtener lista de empleados
    """
    empleados = EmpleadoService.get_empleados(db=db, skip=skip, limit=limit)
    return empleados


@router.get("/{empleado_id}", response_model=EmpleadoConUsuarioResponse)
async def get_empleado(
    empleado_id: int,
    current_user: Usuario = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Obtener empleado por ID con información de usuario asociado
    """
    empleado = EmpleadoService.get_empleado_con_usuario(db=db, empleado_id=empleado_id)
    return empleado


@router.get("/cedula/{cedula}", response_model=EmpleadoResponse)
async def get_empleado_by_cedula(
    cedula: str,
    current_user: Usuario = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Obtener empleado por cédula
    """
    empleado = EmpleadoService.get_empleado_by_cedula(db=db, cedula=cedula)
    if not empleado:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No se encontró empleado con cédula {cedula}"
        )
    return empleado


@router.post("/", response_model=EmpleadoResponse, status_code=status.HTTP_201_CREATED)
async def create_empleado(
    empleado_data: EmpleadoCreate,
    current_user: Usuario = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Crear nuevo empleado
    
    - Si `crear_usuario=true`, también crea un usuario asociado
    - Requiere: nombre, cedula, estado_id
    - Para crear usuario requiere además: usuario, contrasenia, perfil_id
    
    Ejemplo para crear empleado CON usuario:
    ```json
    {
      "nombre": "Juan Pérez",
      "cedula": "12345678",
      "telefono": "021-123456",
      "celular": "0981-123456",
      "domicilio": "Asunción",
      "nacionalidad": "Paraguaya",
      "estado_id": 1,
      "crear_usuario": true,
      "usuario": "jperez",
      "contrasenia": "password123",
      "perfil_id": 2
    }
    ```
    
    Ejemplo para crear empleado SIN usuario:
    ```json
    {
      "nombre": "Juan Pérez",
      "cedula": "12345678",
      "telefono": "021-123456",
      "estado_id": 1,
      "crear_usuario": false
    }
    ```
    """
    empleado = EmpleadoService.create_empleado(db=db, empleado_data=empleado_data)
    return empleado


@router.put("/{empleado_id}", response_model=EmpleadoResponse)
async def update_empleado(
    empleado_id: int,
    empleado_data: EmpleadoUpdate,
    current_user: Usuario = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Actualizar empleado
    
    - Si se cambia el estado del empleado, también se actualiza el estado de su usuario
    """
    empleado = EmpleadoService.update_empleado(
        db=db, 
        empleado_id=empleado_id, 
        empleado_data=empleado_data
    )
    return empleado


@router.delete("/{empleado_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_empleado(
    empleado_id: int,
    current_user: Usuario = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Eliminar (desactivar) empleado
    
    - Desactiva el empleado (estado_id = 2)
    - Si tiene usuario asociado, también lo desactiva
    """
    EmpleadoService.delete_empleado(db=db, empleado_id=empleado_id)
    return None
