from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr
from app.core import get_db
from app.models import Usuario, RolEnum, Carrera
from app.schemas import (
    UsuarioCreate, 
    UsuarioResponse, 
    CarreraResponse
)
from app.services import UsuarioService, CarreraService
from app.api.dependencies import require_superuser, get_current_user

router = APIRouter(prefix="/register", tags=["registration"])

# Esquema específico para registro público
class UsuarioRegister(BaseModel):
    email: EmailStr
    password: str
    nombre_completo: str
    numero_empleado: Optional[str] = None  # Para profesores que se autoregistran
    
@router.post("/jefe-carrera", response_model=UsuarioResponse)
async def register_jefe_carrera(
    user_data: UsuarioRegister,
    id_carrera: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(require_superuser)
):
    """Registrar nuevo Jefe de Carrera (Solo Superusuario)"""
    user_service = UsuarioService(db)
    carrera_service = CarreraService(db)
    
    # Verificar que el email no exista
    existing_user = user_service.get_user_by_email(user_data.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El email ya está registrado"
        )
    
    # Verificar que la carrera exista
    carrera = carrera_service.get_carrera_by_id(id_carrera)
    if not carrera:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="La carrera especificada no existe"
        )
    
    # Verificar que no haya otro jefe para esta carrera
    existing_jefe = db.query(Usuario).filter(
        Usuario.id_carrera == id_carrera,
        Usuario.rol == RolEnum.JEFE_CARRERA
    ).first()
    
    if existing_jefe:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ya existe un Jefe de Carrera para esta carrera"
        )
    
    # Crear usuario
    create_data = UsuarioCreate(
        email=user_data.email,
        password=user_data.password,
        nombre_completo=user_data.nombre_completo,
        rol=RolEnum.JEFE_CARRERA,
        id_carrera=id_carrera
    )
    
    return user_service.create_user(create_data)

@router.get("/carreras-disponibles", response_model=List[CarreraResponse])
async def get_carreras_disponibles(
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(require_superuser)
):
    """Obtener carreras que no tienen Jefe de Carrera asignado"""
    carreras_con_jefe = db.query(Usuario.id_carrera).filter(
        Usuario.rol == RolEnum.JEFE_CARRERA,
        Usuario.id_carrera.isnot(None)
    ).subquery()
    
    carreras_disponibles = db.query(Carrera).filter(
        ~Carrera.id.in_(carreras_con_jefe)
    ).all()
    
    return carreras_disponibles

@router.post("/change-password")
async def change_password(
    current_password: str,
    new_password: str,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """Cambiar contraseña del usuario actual"""
    from app.core.security import verify_password, get_password_hash
    
    # Verificar contraseña actual
    if not verify_password(current_password, current_user.password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Contraseña actual incorrecta"
        )
    
    # Actualizar contraseña
    current_user.password = get_password_hash(new_password)
    db.commit()
    db.refresh(current_user)
    
    return {"message": "Contraseña actualizada exitosamente"}

@router.get("/profile", response_model=UsuarioResponse)
async def get_current_user_profile(
    current_user: Usuario = Depends(get_current_user)
):
    """Obtener perfil del usuario actual"""
    return current_user
