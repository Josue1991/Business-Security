"""
Router de menú
"""
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.dependencies import get_db, get_current_active_user
from app.schemas.menu import MenuCreate, MenuUpdate, MenuResponse, MenuTreeResponse
from app.services.menu_service import MenuService
from app.db.models.menu import Menu
from app.db.models.usuarios import Usuario

router = APIRouter()


@router.get("/tree", response_model=List[MenuTreeResponse])
async def get_user_menu_tree(
    current_user: Usuario = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Obtener árbol de menú del usuario actual según su perfil
    """
    menu_tree = MenuService.get_user_menu_tree(db=db, usuario=current_user)
    return menu_tree


@router.get("/", response_model=List[MenuResponse])
async def get_all_menus(
    include_inactive: bool = False,
    current_user: Usuario = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Obtener todos los menús (para administración)
    """
    menus = MenuService.get_all_menus(db=db, include_inactive=include_inactive)
    return menus


@router.get("/{menu_id}", response_model=MenuResponse)
async def get_menu(
    menu_id: int,
    current_user: Usuario = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Obtener menú por ID
    """
    menu = db.query(Menu).filter(Menu.menu_id == menu_id).first()
    if not menu:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Menú no encontrado"
        )
    return menu


@router.post("/", response_model=MenuResponse, status_code=status.HTTP_201_CREATED)
async def create_menu(
    menu_data: MenuCreate,
    current_user: Usuario = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Crear nuevo menú
    """
    db_menu = Menu(
        descripcion=menu_data.descripcion,
        url=menu_data.url,
        parent_id=menu_data.parent_id,
        nivel=menu_data.nivel,
        orden=menu_data.orden,
        estado_id=menu_data.estado_id
    )
    db.add(db_menu)
    db.commit()
    db.refresh(db_menu)
    return db_menu


@router.put("/{menu_id}", response_model=MenuResponse)
async def update_menu(
    menu_id: int,
    menu_data: MenuUpdate,
    current_user: Usuario = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Actualizar menú
    """
    db_menu = db.query(Menu).filter(Menu.menu_id == menu_id).first()
    if not db_menu:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Menú no encontrado"
        )
    
    update_data = menu_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_menu, field, value)
    
    db.commit()
    db.refresh(db_menu)
    return db_menu


@router.delete("/{menu_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_menu(
    menu_id: int,
    current_user: Usuario = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Eliminar menú
    """
    db_menu = db.query(Menu).filter(Menu.menu_id == menu_id).first()
    if not db_menu:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Menú no encontrado"
        )
    
    db.delete(db_menu)
    db.commit()
    return None
