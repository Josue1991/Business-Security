"""
Punto de entrada principal de la aplicación FastAPI
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.routers import auth, usuarios, perfiles, menu, empleados

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="API de autenticación y autorización para Business ERP"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir routers
app.include_router(auth.router, prefix="/api/auth", tags=["Autenticación"])
app.include_router(empleados.router, prefix="/api/empleados", tags=["Empleados"])
app.include_router(usuarios.router, prefix="/api/usuarios", tags=["Usuarios"])
app.include_router(perfiles.router, prefix="/api/perfiles", tags=["Perfiles"])
app.include_router(menu.router, prefix="/api/menu", tags=["Menú"])


@app.get("/")
async def root():
    return {
        "message": "Business Security API",
        "version": settings.APP_VERSION,
        "status": "running"
    }


@app.get("/health")
async def health_check():
    return {"status": "ok"}
