from typing import Optional, Dict, List
from pydantic import BaseModel, EmailStr
from datetime import time
from app.models.models import RolEnum, TipoProfesorEnum, DiaSemanaEnum

# Base schemas
class CarreraBase(BaseModel):
    nombre: str

class CarreraCreate(CarreraBase):
    pass

class CarreraResponse(CarreraBase):
    id: int
    
    class Config:
        from_attributes = True

# Usuario schemas
class UsuarioBase(BaseModel):
    email: EmailStr
    nombre_completo: str
    rol: RolEnum
    id_carrera: Optional[int] = None

class UsuarioCreate(UsuarioBase):
    password: str

class UsuarioResponse(UsuarioBase):
    id: int
    carrera: Optional[CarreraResponse] = None
    
    class Config:
        from_attributes = True

class UsuarioLogin(BaseModel):
    email: EmailStr
    password: str

# Profesor schemas
class ProfesorBase(BaseModel):
    numero_empleado: str
    nombre_completo: str
    tipo_profesor: TipoProfesorEnum
    disponibilidad: Optional[Dict[str, List[str]]] = None

class ProfesorCreate(ProfesorBase):
    id_carrera: int

class ProfesorUpdate(BaseModel):
    nombre_completo: Optional[str] = None
    disponibilidad: Optional[Dict[str, List[str]]] = None

class ProfesorResponse(ProfesorBase):
    id: int
    id_carrera: int
    carrera: CarreraResponse
    
    class Config:
        from_attributes = True

# Materia schemas
class MateriaBase(BaseModel):
    nombre_materia: str
    cuatrimestre: int
    horas_semanales: int

class MateriaCreate(MateriaBase):
    id_carrera: int

class MateriaResponse(MateriaBase):
    id: int
    id_carrera: int
    carrera: CarreraResponse
    
    class Config:
        from_attributes = True

# Grupo schemas
class GrupoBase(BaseModel):
    cuatrimestre: int
    nombre_grupo: Optional[str] = None

class GrupoCreate(GrupoBase):
    id_carrera: int

class GrupoResponse(GrupoBase):
    id: int
    id_carrera: int
    carrera: CarreraResponse
    
    class Config:
        from_attributes = True

# HorarioGenerado schemas
class HorarioGeneradoBase(BaseModel):
    dia_semana: DiaSemanaEnum
    hora_inicio: time
    hora_fin: time
    version_horario: int = 1

class HorarioGeneradoCreate(HorarioGeneradoBase):
    id_grupo: int
    id_materia: int
    id_profesor: int

class HorarioGeneradoResponse(HorarioGeneradoBase):
    id: int
    grupo: GrupoResponse
    materia: MateriaResponse
    profesor: ProfesorResponse
    
    class Config:
        from_attributes = True

# Auth schemas
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None

# Schedule generation schemas
class ScheduleGenerationRequest(BaseModel):
    id_carrera: int
    cuatrimestre: Optional[int] = None  # Si no se especifica, genera para todos los cuatrimestres

class ScheduleGenerationResponse(BaseModel):
    success: bool
    message: str
    generated_schedules: List[int]  # IDs de grupos para los que se generaron horarios

# Registration schemas
class UsuarioRegister(BaseModel):
    email: EmailStr
    password: str
    nombre_completo: str
    numero_empleado: Optional[str] = None

class PasswordChange(BaseModel):
    current_password: str
    new_password: str

class UserProfile(BaseModel):
    id: int
    email: EmailStr
    nombre_completo: str
    rol: RolEnum
    carrera: Optional[CarreraResponse] = None
    
    class Config:
        from_attributes = True
