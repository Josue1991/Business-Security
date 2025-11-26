"""
Servicio para construcción de menú jerárquico
"""
from typing import List, Dict
from sqlalchemy.orm import Session
from app.db.models.menu import Menu
from app.db.models.usuarios import Usuario
from app.schemas.menu import MenuTreeResponse


class MenuService:
    """Servicio para manejar lógica de menú"""
    
    @staticmethod
    def get_user_menu_tree(db: Session, usuario: Usuario) -> List[MenuTreeResponse]:
        """
        Obtener árbol de menú para un usuario según su perfil
        
        Args:
            db: Sesión de base de datos
            usuario: Usuario autenticado
        
        Returns:
            Lista de menús jerárquicos (solo raíz, con hijos anidados)
        """
        # Obtener perfil del usuario
        perfil = usuario.perfil
        if not perfil:
            return []
        
        # Obtener todos los menús asociados al perfil (activos)
        menus = [m for m in perfil.menus if m.estado_id == 1]
        
        # Convertir a diccionario para búsqueda rápida
        menu_dict: Dict[int, MenuTreeResponse] = {}
        for menu in menus:
            menu_dict[menu.menu_id] = MenuTreeResponse(
                menu_id=menu.menu_id,
                descripcion=menu.descripcion,
                url=menu.url,
                parent_id=menu.parent_id,
                nivel=menu.nivel,
                orden=menu.orden,
                estado_id=menu.estado_id,
                created_at=menu.created_at,
                children=[]
            )
        
        # Construir árbol
        root_menus = []
        for menu in menu_dict.values():
            if menu.parent_id is None:
                # Es un menú raíz
                root_menus.append(menu)
            else:
                # Tiene padre, agregarlo como hijo
                parent = menu_dict.get(menu.parent_id)
                if parent:
                    parent.children.append(menu)
        
        # Ordenar por el campo 'orden'
        def sort_recursive(items: List[MenuTreeResponse]):
            items.sort(key=lambda x: x.orden)
            for item in items:
                if item.children:
                    sort_recursive(item.children)
        
        sort_recursive(root_menus)
        
        return root_menus
    
    @staticmethod
    def get_all_menus(db: Session, include_inactive: bool = False) -> List[Menu]:
        """
        Obtener todos los menús
        
        Args:
            db: Sesión de base de datos
            include_inactive: Si incluir menús inactivos
        
        Returns:
            Lista de menús
        """
        query = db.query(Menu)
        if not include_inactive:
            query = query.filter(Menu.estado_id == 1)
        
        return query.order_by(Menu.nivel, Menu.orden).all()
