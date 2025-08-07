from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core import get_db
from app.models import Usuario
from app.schemas import CarreraCreate, CarreraResponse, UsuarioCreate, UsuarioResponse
from app.services import CarreraService, UsuarioService
from app.api.dependencies import require_superuser

router = APIRouter(prefix="/admin", tags=["administration"])

@router.get("/carreras", response_model=List[CarreraResponse])
async def get_all_carreras(
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(require_superuser)
):
    """Obtener todas las carreras (Solo Superusuario)"""
    carrera_service = CarreraService(db)
    return carrera_service.get_all_carreras()

@router.post("/carreras", response_model=CarreraResponse)
async def create_carrera(
    carrera_data: CarreraCreate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(require_superuser)
):
    """Crear nueva carrera (Solo Superusuario)"""
    carrera_service = CarreraService(db)
    return carrera_service.create_carrera(carrera_data.nombre)

@router.post("/users", response_model=UsuarioResponse)
async def create_user(
    user_data: UsuarioCreate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(require_superuser)
):
    """Crear nuevo usuario (Solo Superusuario)"""
    user_service = UsuarioService(db)
    
    # Verificar que el email no exista
    existing_user = user_service.get_user_by_email(user_data.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El email ya está registrado"
        )
    
    # Verificar que la carrera exista si se especifica
    if user_data.id_carrera:
        carrera_service = CarreraService(db)
        carrera = carrera_service.get_carrera_by_id(user_data.id_carrera)
        if not carrera:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="La carrera especificada no existe"
            )
    
    return user_service.create_user(user_data)
