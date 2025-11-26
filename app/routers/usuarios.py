"""
Router de usuarios
"""
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.dependencies import get_db, get_current_active_user
from app.schemas.usuarios import UsuarioCreate, UsuarioUpdate, UsuarioResponse
from app.services.usuario_service import UsuarioService
from app.db.models.usuarios import Usuario

router = APIRouter()


@router.get("/", response_model=List[UsuarioResponse])
async def get_usuarios(
    skip: int = 0,
    limit: int = 100,
    current_user: Usuario = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Obtener lista de usuarios
    """
    usuarios = UsuarioService.get_usuarios(db=db, skip=skip, limit=limit)
    return usuarios


@router.get("/{usuario_id}", response_model=UsuarioResponse)
async def get_usuario(
    usuario_id: int,
    current_user: Usuario = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Obtener usuario por ID
    """
    usuario = UsuarioService.get_usuario_by_id(db=db, usuario_id=usuario_id)
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado"
        )
    return usuario


@router.post("/", response_model=UsuarioResponse, status_code=status.HTTP_201_CREATED)
async def create_usuario(
    usuario_data: UsuarioCreate,
    current_user: Usuario = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Crear nuevo usuario
    """
    usuario = UsuarioService.create_usuario(db=db, usuario_data=usuario_data)
    return usuario


@router.put("/{usuario_id}", response_model=UsuarioResponse)
async def update_usuario(
    usuario_id: int,
    usuario_data: UsuarioUpdate,
    current_user: Usuario = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Actualizar usuario
    """
    usuario = UsuarioService.update_usuario(db=db, usuario_id=usuario_id, usuario_data=usuario_data)
    return usuario


@router.delete("/{usuario_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_usuario(
    usuario_id: int,
    current_user: Usuario = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Eliminar (desactivar) usuario
    """
    UsuarioService.delete_usuario(db=db, usuario_id=usuario_id)
    return None
