from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api import auth_router, admin_router, schedules_router, registration_router

# Crear aplicación FastAPI
app = FastAPI(
    title="SIGAH - Sistema de Gestión de Horarios Universitarios",
    description="API para la gestión y generación automática de horarios académicos",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir routers
app.include_router(auth_router)
app.include_router(admin_router)
app.include_router(schedules_router)
app.include_router(registration_router)

@app.get("/")
async def root():
    """Endpoint de estado de la API"""
    return {
        "message": "SIGAH API funcionando correctamente",
        "version": "1.0.0",
        "status": "active"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
