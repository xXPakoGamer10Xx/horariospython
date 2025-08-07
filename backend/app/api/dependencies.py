from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from app.core import get_db, verify_token
from app.models import Usuario, RolEnum
from app.services import UsuarioService

router = APIRouter()
security = HTTPBearer()

async def get_current_user(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)],
    db: Session = Depends(get_db)
) -> Usuario:
    """Dependency para obtener el usuario actual desde JWT token"""
    
    token_data = verify_token(credentials.credentials)
    if not token_data:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido o expirado",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    email = token_data.get("sub")
    if not email:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    user_service = UsuarioService(db)
    user = user_service.get_user_by_email(email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario no encontrado",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return user

async def require_superuser(
    current_user: Usuario = Depends(get_current_user)
) -> Usuario:
    """Dependency que requiere rol de SUPERUSUARIO"""
    if current_user.rol != RolEnum.SUPERUSUARIO:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Permisos insuficientes. Se requiere rol de Superusuario"
        )
    return current_user

async def require_jefe_carrera_or_super(
    current_user: Usuario = Depends(get_current_user)
) -> Usuario:
    """Dependency que requiere rol de JEFE_CARRERA o SUPERUSUARIO"""
    if current_user.rol not in [RolEnum.JEFE_CARRERA, RolEnum.SUPERUSUARIO]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Permisos insuficientes"
        )
    return current_user

def check_carrera_access(user: Usuario, carrera_id: int):
    """Verifica si el usuario tiene acceso a una carrera específica"""
    if user.rol == RolEnum.SUPERUSUARIO:
        return True  # Superusuario tiene acceso a todo
    
    if user.rol == RolEnum.JEFE_CARRERA and user.id_carrera == carrera_id:
        return True  # Jefe de carrera solo a su carrera
    
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="No tiene acceso a esta carrera"
    )
