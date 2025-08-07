from sqlalchemy import Column, Integer, String, ForeignKey, Enum, Time, JSON, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import enum

Base = declarative_base()

class RolEnum(enum.Enum):
    SUPERUSUARIO = "SUPERUSUARIO"
    JEFE_CARRERA = "JEFE_CARRERA"

class TipoProfesorEnum(enum.Enum):
    PTC = "PTC"  # Profesor de Tiempo Completo
    PA = "PA"    # Profesor de Asignatura

class DiaSemanaEnum(enum.Enum):
    LUNES = "Lunes"
    MARTES = "Martes"
    MIERCOLES = "Miércoles"
    JUEVES = "Jueves"
    VIERNES = "Viernes"
    SABADO = "Sábado"

class Carrera(Base):
    __tablename__ = "carreras"
    
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(255), nullable=False, unique=True)
    
    # Relaciones
    usuarios = relationship("Usuario", back_populates="carrera")
    profesores = relationship("Profesor", back_populates="carrera")
    materias = relationship("Materia", back_populates="carrera")
    grupos = relationship("Grupo", back_populates="carrera")

class Usuario(Base):
    __tablename__ = "usuarios"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    password = Column(String(255), nullable=False)
    nombre_completo = Column(String(255), nullable=False)
    rol = Column(Enum(RolEnum), nullable=False)
    id_carrera = Column(Integer, ForeignKey("carreras.id"), nullable=True)
    
    # Relaciones
    carrera = relationship("Carrera", back_populates="usuarios")

class Profesor(Base):
    __tablename__ = "profesores"
    
    id = Column(Integer, primary_key=True, index=True)
    numero_empleado = Column(String(50), unique=True, nullable=False)
    nombre_completo = Column(String(255), nullable=False)
    id_carrera = Column(Integer, ForeignKey("carreras.id"), nullable=False)
    tipo_profesor = Column(Enum(TipoProfesorEnum), nullable=False)
    disponibilidad = Column(JSON, nullable=True)  # {"Lunes": ["07:00-10:00", "12:00-15:00"]}
    
    # Relaciones
    carrera = relationship("Carrera", back_populates="profesores")
    horarios = relationship("HorarioGenerado", back_populates="profesor")

class Materia(Base):
    __tablename__ = "materias"
    
    id = Column(Integer, primary_key=True, index=True)
    nombre_materia = Column(String(255), nullable=False)
    id_carrera = Column(Integer, ForeignKey("carreras.id"), nullable=False)
    cuatrimestre = Column(Integer, nullable=False)  # 1 al 10
    horas_semanales = Column(Integer, nullable=False)
    
    # Relaciones
    carrera = relationship("Carrera", back_populates="materias")
    horarios = relationship("HorarioGenerado", back_populates="materia")

class Grupo(Base):
    __tablename__ = "grupos"
    
    id = Column(Integer, primary_key=True, index=True)
    id_carrera = Column(Integer, ForeignKey("carreras.id"), nullable=False)
    cuatrimestre = Column(Integer, nullable=False)  # 1 al 10
    nombre_grupo = Column(String(100), nullable=True)  # Ej: "Grupo A", "Grupo B"
    
    # Relaciones
    carrera = relationship("Carrera", back_populates="grupos")
    horarios = relationship("HorarioGenerado", back_populates="grupo")

class HorarioGenerado(Base):
    __tablename__ = "horarios_generados"
    
    id = Column(Integer, primary_key=True, index=True)
    id_grupo = Column(Integer, ForeignKey("grupos.id"), nullable=False)
    id_materia = Column(Integer, ForeignKey("materias.id"), nullable=False)
    id_profesor = Column(Integer, ForeignKey("profesores.id"), nullable=False)
    dia_semana = Column(Enum(DiaSemanaEnum), nullable=False)
    hora_inicio = Column(Time, nullable=False)
    hora_fin = Column(Time, nullable=False)
    version_horario = Column(Integer, nullable=False, default=1)  # 1 o 2 (para las 2 opciones)
    
    # Relaciones
    grupo = relationship("Grupo", back_populates="horarios")
    materia = relationship("Materia", back_populates="horarios")
    profesor = relationship("Profesor", back_populates="horarios")
