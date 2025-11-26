"""
Router de perfiles
"""
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.dependencies import get_db, get_current_active_user
from app.schemas.perfiles import PerfilCreate, PerfilUpdate, PerfilResponse, PerfilMenuAssign
from app.db.models.perfil import Perfil
from app.db.models.menu import Menu
from app.db.models.usuarios import Usuario

router = APIRouter()


@router.get("/", response_model=List[PerfilResponse])
async def get_perfiles(
    skip: int = 0,
    limit: int = 100,
    current_user: Usuario = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Obtener lista de perfiles
    """
    perfiles = db.query(Perfil).offset(skip).limit(limit).all()
    return perfiles


@router.get("/{perfil_id}", response_model=PerfilResponse)
async def get_perfil(
    perfil_id: int,
    current_user: Usuario = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Obtener perfil por ID
    """
    perfil = db.query(Perfil).filter(Perfil.perfil_id == perfil_id).first()
    if not perfil:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Perfil no encontrado"
        )
    return perfil


@router.post("/", response_model=PerfilResponse, status_code=status.HTTP_201_CREATED)
async def create_perfil(
    perfil_data: PerfilCreate,
    current_user: Usuario = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Crear nuevo perfil
    """
    db_perfil = Perfil(
        descripcion=perfil_data.descripcion,
        estado_id=perfil_data.estado_id
    )
    db.add(db_perfil)
    db.commit()
    db.refresh(db_perfil)
    return db_perfil


@router.put("/{perfil_id}", response_model=PerfilResponse)
async def update_perfil(
    perfil_id: int,
    perfil_data: PerfilUpdate,
    current_user: Usuario = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Actualizar perfil
    """
    db_perfil = db.query(Perfil).filter(Perfil.perfil_id == perfil_id).first()
    if not db_perfil:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Perfil no encontrado"
        )
    
    update_data = perfil_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_perfil, field, value)
    
    db.commit()
    db.refresh(db_perfil)
    return db_perfil


@router.delete("/{perfil_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_perfil(
    perfil_id: int,
    current_user: Usuario = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Eliminar perfil
    """
    db_perfil = db.query(Perfil).filter(Perfil.perfil_id == perfil_id).first()
    if not db_perfil:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Perfil no encontrado"
        )
    
    db.delete(db_perfil)
    db.commit()
    return None


@router.post("/{perfil_id}/menus")
async def assign_menus_to_perfil(
    perfil_id: int,
    menu_data: PerfilMenuAssign,
    current_user: Usuario = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Asignar menús a un perfil
    """
    perfil = db.query(Perfil).filter(Perfil.perfil_id == perfil_id).first()
    if not perfil:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Perfil no encontrado"
        )
    
    # Obtener menús
    menus = db.query(Menu).filter(Menu.menu_id.in_(menu_data.menu_ids)).all()
    if len(menus) != len(menu_data.menu_ids):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Algunos menús no existen"
        )
    
    # Asignar menús al perfil
    perfil.menus = menus
    db.commit()
    
    return {"message": f"{len(menus)} menús asignados al perfil"}
