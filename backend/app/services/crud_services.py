from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import and_
from app.models import Usuario, Carrera, Profesor, Materia, Grupo, HorarioGenerado, RolEnum
from app.schemas import UsuarioCreate, UsuarioResponse
from app.core.security import get_password_hash, verify_password

class UsuarioService:
    """Servicio para gestión de usuarios"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def create_user(self, user_data: UsuarioCreate) -> Usuario:
        """Crear un nuevo usuario"""
        hashed_password = get_password_hash(user_data.password)
        db_user = Usuario(
            email=user_data.email,
            password=hashed_password,
            nombre_completo=user_data.nombre_completo,
            rol=user_data.rol,
            id_carrera=user_data.id_carrera
        )
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return db_user
    
    def get_user_by_email(self, email: str) -> Optional[Usuario]:
        """Obtener usuario por email"""
        return self.db.query(Usuario).filter(Usuario.email == email).first()
    
    def get_user_by_id(self, user_id: int) -> Optional[Usuario]:
        """Obtener usuario por ID"""
        return self.db.query(Usuario).filter(Usuario.id == user_id).first()
    
    def authenticate_user(self, email: str, password: str) -> Optional[Usuario]:
        """Autenticar usuario"""
        user = self.get_user_by_email(email)
        if not user or not verify_password(password, user.password):
            return None
        return user
    
    def update_password(self, user_id: int, new_password: str) -> Optional[Usuario]:
        """Actualizar contraseña de usuario"""
        user = self.get_user_by_id(user_id)
        if user:
            user.password = get_password_hash(new_password)
            self.db.commit()
            self.db.refresh(user)
        return user
    
    def get_jefes_carrera(self) -> List[Usuario]:
        """Obtener todos los jefes de carrera"""
        return self.db.query(Usuario).filter(Usuario.rol == RolEnum.JEFE_CARRERA).all()
    
    def check_carrera_has_jefe(self, carrera_id: int) -> bool:
        """Verificar si una carrera ya tiene jefe asignado"""
        existing = self.db.query(Usuario).filter(
            Usuario.id_carrera == carrera_id,
            Usuario.rol == RolEnum.JEFE_CARRERA
        ).first()
        return existing is not None

class CarreraService:
    """Servicio para gestión de carreras"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def get_all_carreras(self) -> List[Carrera]:
        """Obtener todas las carreras"""
        return self.db.query(Carrera).all()
    
    def get_carrera_by_id(self, carrera_id: int) -> Optional[Carrera]:
        """Obtener carrera por ID"""
        return self.db.query(Carrera).filter(Carrera.id == carrera_id).first()
    
    def create_carrera(self, nombre: str) -> Carrera:
        """Crear nueva carrera"""
        db_carrera = Carrera(nombre=nombre)
        self.db.add(db_carrera)
        self.db.commit()
        self.db.refresh(db_carrera)
        return db_carrera

class ProfesorService:
    """Servicio para gestión de profesores"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def get_profesores_by_carrera(self, carrera_id: int) -> List[Profesor]:
        """Obtener profesores de una carrera"""
        return self.db.query(Profesor).filter(Profesor.id_carrera == carrera_id).all()
    
    def update_profesor_availability(self, profesor_id: int, disponibilidad: dict) -> Optional[Profesor]:
        """Actualizar disponibilidad de profesor"""
        profesor = self.db.query(Profesor).filter(Profesor.id == profesor_id).first()
        if profesor:
            profesor.disponibilidad = disponibilidad
            self.db.commit()
            self.db.refresh(profesor)
        return profesor

class HorarioService:
    """Servicio para gestión de horarios"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def get_horario_grupo(self, grupo_id: int, version: int = 1) -> List[HorarioGenerado]:
        """Obtener horario de un grupo específico"""
        return self.db.query(HorarioGenerado).filter(
            and_(
                HorarioGenerado.id_grupo == grupo_id,
                HorarioGenerado.version_horario == version
            )
        ).all()
    
    def get_horario_profesor(self, profesor_id: int) -> List[HorarioGenerado]:
        """Obtener horario de un profesor"""
        return self.db.query(HorarioGenerado).filter(
            HorarioGenerado.id_profesor == profesor_id
        ).all()
    
    def delete_horarios_grupo(self, grupo_id: int):
        """Eliminar todos los horarios de un grupo"""
        self.db.query(HorarioGenerado).filter(
            HorarioGenerado.id_grupo == grupo_id
        ).delete()
        self.db.commit()
