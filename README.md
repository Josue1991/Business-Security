# Business Security API

Backend de autenticación y autorización para Business ERP, desarrollado con FastAPI y SQLAlchemy.

## 🚀 Características

- ✅ Autenticación JWT con control de intentos fallidos
- ✅ Gestión de usuarios, perfiles y empleados
- ✅ Sistema de menú jerárquico (recursivo)
- ✅ Autorización basada en perfiles
- ✅ Bloqueo automático por intentos fallidos
- ✅ API REST documentada con OpenAPI/Swagger
- ✅ Arquitectura limpia y escalable

## 📁 Estructura del Proyecto

```
Business-Security/
├── app/
│   ├── core/              # Configuración, seguridad, dependencias
│   ├── db/                # Modelos SQLAlchemy y sesión
│   │   └── models/        # Modelos de BD
│   ├── routers/           # Endpoints API (FastAPI)
│   ├── schemas/           # Schemas Pydantic (validación)
│   ├── services/          # Lógica de negocio
│   └── main.py            # Punto de entrada
├── init_db.py             # Script de inicialización de BD
├── requirements.txt       # Dependencias Python
├── .env.example           # Variables de entorno ejemplo
└── README.md
```

## 🛠️ Tecnologías

- **FastAPI** - Framework web moderno y rápido
- **SQLAlchemy** - ORM para Python
- **Pydantic** - Validación de datos
- **JWT** - Autenticación con tokens
- **Bcrypt** - Hash de contraseñas
- **PostgreSQL/SQLite** - Base de datos

## 📦 Instalación

### 1. Crear entorno virtual

```powershell
cd c:\Proyectos\BusinessApp\Business-Security
python -m venv .venv
.venv\Scripts\activate
```

### 2. Instalar dependencias

```powershell
pip install -r requirements.txt
```

### 3. Configurar variables de entorno

Copiar `.env.example` a `.env` y ajustar valores:

```powershell
copy .env.example .env
```

Editar `.env` con tus configuraciones:
- `DATABASE_URL`: URL de conexión a la base de datos
- `SECRET_KEY`: Clave secreta para JWT (cambiar en producción)
- `ALLOWED_ORIGINS`: Orígenes permitidos para CORS

### 4. Inicializar base de datos con Alembic

#### **Opción A: Base de datos nueva (PostgreSQL o SQLite)**

```powershell
# Aplicar migraciones (crear tablas)
alembic upgrade head

# Poblar con datos iniciales
python seed_db.py
```

#### **Opción B: Base de datos PostgreSQL existente con tablas**

Si tu base de datos PostgreSQL ya tiene las tablas creadas:

```powershell
# 1. Verificar conexión
python check_db_sqlalchemy.py

# 2. Sincronizar Alembic con el estado actual
alembic stamp head

# 3. (Opcional) Poblar datos si es necesario
python seed_db.py
```

**Datos de prueba creados:**
- **Usuario:** `admin` | **Contraseña:** `admin123`
- **Usuario:** `usuario` | **Contraseña:** `usuario123`

> 📖 **Ver guía completa de migraciones**: [MIGRACIONES.md](./MIGRACIONES.md)

## 🚀 Ejecutar el servidor

```powershell
# Activar entorno virtual
& .venv\Scripts\Activate.ps1

# Iniciar servidor
uvicorn app.main:app --reload --port 8000
```

El servidor estará disponible en: http://localhost:8000

## 📚 Documentación API

Una vez ejecutado el servidor, accede a:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🔐 Endpoints Principales

### Autenticación

- `POST /api/auth/login` - Login con usuario/contraseña
- `POST /api/auth/login-form` - Login formato OAuth2
- `GET /api/auth/me` - Información del usuario actual
- `POST /api/auth/change-password` - Cambiar contraseña
- `POST /api/auth/reset-attempts/{usuario_id}` - Resetear intentos

### Usuarios

- `GET /api/usuarios/` - Listar usuarios
- `GET /api/usuarios/{id}` - Obtener usuario
- `POST /api/usuarios/` - Crear usuario
- `PUT /api/usuarios/{id}` - Actualizar usuario
- `DELETE /api/usuarios/{id}` - Eliminar usuario

### Perfiles

- `GET /api/perfiles/` - Listar perfiles
- `POST /api/perfiles/` - Crear perfil
- `POST /api/perfiles/{id}/menus` - Asignar menús a perfil

### Menú

- `GET /api/menu/tree` - Obtener árbol de menú del usuario actual
- `GET /api/menu/` - Listar todos los menús
- `POST /api/menu/` - Crear menú

## 🔑 Flujo de Autenticación

1. **Login**: `POST /api/auth/login`
   ```json
   {
     "usuario": "admin",
     "contrasenia": "password123"
   }
   ```
   
   Respuesta:
   ```json
   {
     "access_token": "eyJhbGc...",
     "token_type": "bearer"
   }
   ```

2. **Usar token**: Agregar header en requests subsiguientes
   ```
   Authorization: Bearer eyJhbGc...
   ```

3. **Obtener menú del usuario**: `GET /api/menu/tree`
   - Devuelve el árbol de menú jerárquico según el perfil del usuario

## 🔒 Seguridad

- Contraseñas hasheadas con **bcrypt**
- Tokens JWT con expiración configurable
- Control de intentos de login fallidos (bloqueo automático)
- Estados de usuario (activo, inactivo, bloqueado)
- CORS configurado para orígenes específicos

## 🗃️ Modelo de Datos

### Tablas principales:

- `estado` - Estados (Activo, Inactivo, Bloqueado)
- `empleados` - Información de empleados
- `usuarios` - Credenciales y control de acceso
- `perfil` - Roles/perfiles de usuario
- `menu` - Menú jerárquico (recursivo)
- `perfil_menu` - Relación N:N entre perfiles y menús

## 🧪 Testing

Para probar la API, puedes usar:

- **Swagger UI**: http://localhost:8000/docs (interfaz interactiva)
- **Postman/Insomnia**: Importar la colección desde OpenAPI
- **curl** o **httpie**

Ejemplo con curl:

```powershell
# Login
curl -X POST "http://localhost:8000/api/auth/login" `
  -H "Content-Type: application/json" `
  -d '{\"usuario\":\"admin\",\"contrasenia\":\"password123\"}'

# Obtener menú (con token)
curl -X GET "http://localhost:8000/api/menu/tree" `
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

## 🔧 Configuración de Producción

1. Cambiar `SECRET_KEY` en `.env`
2. Usar PostgreSQL en lugar de SQLite
3. Configurar `DEBUG=False`
4. Ajustar `ALLOWED_ORIGINS` con dominios reales
5. Usar HTTPS (detrás de proxy/gateway)
6. Configurar logs y monitoreo

## 🔄 Migraciones de Base de Datos

Este proyecto usa **Alembic** para gestionar migraciones de base de datos.

### Flujo completo con base de datos existente:

```powershell
# 1. Configurar .env con credenciales PostgreSQL
# DATABASE_URL=postgresql+psycopg://postgres:tu_password@localhost:5432/Auth

# 2. Verificar conexión
python check_db_sqlalchemy.py

# 3. Sincronizar estado actual
alembic stamp head

# 4. Ver estado de migraciones
alembic current
```

### Comandos básicos para desarrollo:

```powershell
# Crear nueva migración después de modificar modelos
alembic revision --autogenerate -m "descripción del cambio"

# Aplicar migraciones pendientes
alembic upgrade head

# Revertir última migración
alembic downgrade -1

# Ver historial
alembic history
```

📖 **Guía completa**: Ver [MIGRACIONES.md](./MIGRACIONES.md) para documentación detallada.

## 📝 Próximas Mejoras

- [ ] Refresh tokens
- [ ] Roles y permisos granulares
- [ ] Auditoría de acciones
- [ ] Rate limiting
- [ ] Tests unitarios y de integración
- [x] Alembic para migraciones de BD
- [ ] Logs estructurados

## 📄 Licencia

Proyecto interno de Business ERP

## 👥 Contacto

Para dudas o sugerencias, contactar al equipo de desarrollo.
