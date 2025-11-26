# Arquitectura del Backend Business-Security

## 📋 Resumen

Backend de autenticación y autorización desarrollado con **FastAPI** siguiendo una arquitectura limpia de 3 capas (Routers → Services → Models).

## 🏗️ Arquitectura Implementada

### **Capas de la Aplicación**

```
┌─────────────────────────────────────────────┐
│          ROUTERS (API Endpoints)            │
│  ┌────────┬────────┬─────────┬────────┐     │
│  │  Auth  │Usuario │ Perfil  │  Menú  │     │
│  └────────┴────────┴─────────┴────────┘     │
└──────────────────┬──────────────────────────┘
                   │
┌──────────────────▼──────────────────────────┐
│          SERVICES (Lógica de Negocio)       │
│  ┌─────────────┬──────────────────────┐     │
│  │ Auth Service│ Usuario Service      │     │
│  │ Menu Service│ (+ Otros servicios)  │     │
│  └─────────────┴──────────────────────┘     │
└──────────────────┬──────────────────────────┘
                   │
┌──────────────────▼──────────────────────────┐
│          MODELS (Datos - SQLAlchemy)        │
│  ┌───────┬────────┬────────┬──────────┐     │
│  │Estado │Usuario │ Perfil │   Menú   │     │
│  │Empleado│        │        │PerfilMenu│     │
│  └───────┴────────┴────────┴──────────┘     │
└──────────────────┬──────────────────────────┘
                   │
            ┌──────▼──────┐
            │   DATABASE  │
            │ (SQLite/PG) │
            └─────────────┘
```

### **Componentes Principales**

#### **1. Core (app/core/)**
- `config.py`: Configuración de la aplicación (variables de entorno)
- `security.py`: Hash de contraseñas (bcrypt) y JWT (tokens de acceso)
- `dependencies.py`: Dependencias de FastAPI (DB session, auth)

#### **2. Database (app/db/)**
- `base.py`: Base declarativa de SQLAlchemy
- `session.py`: Configuración del engine y SessionLocal
- `models/`: Modelos ORM mapeando las tablas de la base de datos
  - `estado.py`: Estados (Activo, Inactivo, Bloqueado)
  - `empleados.py`: Datos de empleados
  - `usuarios.py`: Credenciales y control de acceso
  - `perfil.py`: Roles/perfiles + relación N:N con menú
  - `menu.py`: Menú jerárquico (recursivo con parent_id)

#### **3. Schemas (app/schemas/)**
Validación de datos con Pydantic:
- `auth.py`: Login, Token, ChangePassword
- `usuarios.py`: UsuarioCreate, UsuarioUpdate, UsuarioResponse
- `perfiles.py`: PerfilCreate, PerfilUpdate, PerfilMenuAssign
- `menu.py`: MenuCreate, MenuUpdate, MenuTreeResponse (recursivo)

#### **4. Services (app/services/)**
Lógica de negocio:
- `auth_service.py`: 
  - Autenticación de usuarios
  - Control de intentos fallidos (bloqueo automático)
  - Cambio de contraseña
  - Reset de intentos
- `menu_service.py`: 
  - Construcción del árbol de menú jerárquico
  - Filtrado por perfil del usuario
- `usuario_service.py`: 
  - CRUD de usuarios
  - Validaciones

#### **5. Routers (app/routers/)**
Endpoints HTTP:
- `auth.py`: `/api/auth/*`
  - `POST /login`: Login con usuario/contraseña → JWT token
  - `GET /me`: Información del usuario actual
  - `POST /change-password`: Cambiar contraseña
  - `POST /reset-attempts/{id}`: Resetear intentos (admin)
  
- `usuarios.py`: `/api/usuarios/*`
  - CRUD completo de usuarios
  
- `perfiles.py`: `/api/perfiles/*`
  - CRUD de perfiles
  - `POST /{id}/menus`: Asignar menús a perfil
  
- `menu.py`: `/api/menu/*`
  - `GET /tree`: Obtener árbol de menú del usuario actual
  - CRUD de menús

## 🔐 Flujo de Autenticación

```
┌───────────┐
│  Cliente  │
└─────┬─────┘
      │ 1. POST /api/auth/login
      │    {usuario, contrasenia}
      ▼
┌─────────────────┐
│  Auth Router    │
└────────┬────────┘
         │ 2. Llamar AuthService
         ▼
┌─────────────────────┐
│  Auth Service       │
│  - Buscar usuario   │
│  - Verificar estado │
│  - Verificar hash   │
│  - Control intentos │
└────────┬────────────┘
         │ 3. Usuario válido
         ▼
┌─────────────────────┐
│  Security (JWT)     │
│  - Crear token      │
│  - Payload: id,     │
│    perfil, etc.     │
└────────┬────────────┘
         │ 4. Devolver token
         ▼
┌───────────┐
│  Cliente  │ → Guarda token
└───────────┘

┌───────────┐
│  Cliente  │
└─────┬─────┘
      │ 5. GET /api/menu/tree
      │    Authorization: Bearer <token>
      ▼
┌─────────────────┐
│  Dependencies   │
│  - Verificar    │
│    token JWT    │
│  - Obtener user │
└────────┬────────┘
         │ 6. Usuario autenticado
         ▼
┌─────────────────────┐
│  Menu Service       │
│  - Obtener perfil   │
│  - Filtrar menús    │
│  - Armar árbol l     │
└────────┬────────────┘
         │ 7. Menú jerárquico
         ▼
┌───────────┐
│  Cliente  │ → Renderiza menú
└───────────┘
```

## 🛡️ Características de Seguridad

1. **Contraseñas hasheadas**: bcrypt con salt automático
2. **JWT con expiración**: 30 minutos por defecto (configurable)
3. **Control de intentos fallidos**: 
   - Máximo 3 intentos (configurable)
   - Bloqueo automático al exceder intentos
   - Reset manual de intentos por admin
4. **Estados de usuario**: Activo, Inactivo, Bloqueado
5. **CORS**: Configurado para orígenes específicos
6. **Validación de perfiles**: Solo usuarios con perfil activo pueden acceder

## 📊 Modelo de Datos

```
┌──────────┐       ┌──────────┐
│  Estado  │◄──────│  Perfil  │
└────┬─────┘       └────┬─────┘
     │                  │
     │                  │ N:N
     │             ┌────▼─────┐
     │             │Perfil    │
     │             │Menu      │
     │             └────┬─────┘
     │                  │
     │             ┌────▼─────┐
     │             │   Menu   │◄─┐
     │             │(parent_id)──┘
     │             └──────────┘
     │
┌────▼─────┐       ┌──────────┐
│Empleados │◄──────│ Usuarios │
└──────────┘       └──────────┘
                        ▲
                        │
                   ┌────┴─────┐
                   │  Perfil  │
                   └──────────┘
```

## 🚀 Endpoints Principales

### Autenticación
- `POST /api/auth/login` → Token JWT
- `GET /api/auth/me` → Usuario actual
- `POST /api/auth/change-password` → Cambiar contraseña

### Usuarios
- `GET /api/usuarios/` → Listar
- `POST /api/usuarios/` → Crear
- `PUT /api/usuarios/{id}` → Actualizar
- `DELETE /api/usuarios/{id}` → Eliminar (soft delete)

### Perfiles
- `GET /api/perfiles/` → Listar
- `POST /api/perfiles/{id}/menus` → Asignar menús

### Menú
- `GET /api/menu/tree` → Árbol del usuario actual
- `GET /api/menu/` → Todos los menús (admin)

## 🔧 Configuración

### Variables de Entorno (.env)
```env
DATABASE_URL=sqlite:///./business_security.db
SECRET_KEY=your-secret-key-here-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
ALLOWED_ORIGINS=http://localhost:4200,http://localhost:8100
MAX_LOGIN_ATTEMPTS=3
```

## 📈 Próximas Mejoras Sugeridas

1. **Refresh Tokens**: Para renovar access tokens sin login
2. **Roles granulares**: Permisos específicos por endpoint
3. **Auditoría**: Log de acciones de usuarios
4. **Rate Limiting**: Protección contra ataques de fuerza bruta
5. **Alembic**: Migraciones de base de datos
6. **Tests**: Unitarios e integración
7. **Logging estructurado**: Para debugging y monitoreo
8. **Caché**: Redis para tokens y sesiones
9. **2FA**: Autenticación de dos factores opcional
10. **API Keys**: Para integraciones externas

## 📝 Notas de Implementación

- **Separación de responsabilidades**: Routers solo manejan HTTP, Services contienen lógica
- **Inyección de dependencias**: FastAPI Depends para DB y Auth
- **Validación automática**: Pydantic schemas en requests/responses
- **Documentación automática**: Swagger UI en `/docs`
- **Tipado estricto**: Type hints en todo el código
- **Arquitectura escalable**: Fácil agregar nuevos endpoints/servicios

## 🎯 Patrones Utilizados

- **Repository Pattern**: (implícito en Services)
- **Dependency Injection**: FastAPI Depends
- **DTO Pattern**: Pydantic Schemas
- **Layered Architecture**: Routers → Services → Models
- **Factory Pattern**: SessionLocal para DB sessions

---

**Autor**: GitHub Copilot  
**Fecha**: Noviembre 2025  
**Stack**: FastAPI + SQLAlchemy + Pydantic + JWT
