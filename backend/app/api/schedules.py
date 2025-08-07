from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session
from app.core import get_db
from app.models import Usuario
from app.schemas import (
    ProfesorResponse, ProfesorUpdate, MateriaResponse, 
    ScheduleGenerationRequest, ScheduleGenerationResponse,
    HorarioGeneradoResponse
)
from app.services import ProfesorService, ScheduleOptimizer, HorarioService, ExcelImportService
from app.api.dependencies import require_jefe_carrera_or_super, check_carrera_access
import tempfile
import os

router = APIRouter(prefix="/schedule", tags=["schedule_management"])

@router.get("/profesores/{carrera_id}", response_model=List[ProfesorResponse])
async def get_profesores_by_carrera(
    carrera_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(require_jefe_carrera_or_super)
):
    """Obtener profesores de una carrera"""
    check_carrera_access(current_user, carrera_id)
    
    profesor_service = ProfesorService(db)
    return profesor_service.get_profesores_by_carrera(carrera_id)

@router.put("/profesor/{profesor_id}/availability", response_model=ProfesorResponse)
async def update_profesor_availability(
    profesor_id: int,
    update_data: ProfesorUpdate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(require_jefe_carrera_or_super)
):
    """Actualizar disponibilidad de profesor"""
    from app.models import Profesor
    profesor_service = ProfesorService(db)
    profesor = db.query(Profesor).filter(Profesor.id == profesor_id).first()
    
    if not profesor:
        raise HTTPException(status_code=404, detail="Profesor no encontrado")
    
    check_carrera_access(current_user, profesor.id_carrera)
    
    return profesor_service.update_profesor_availability(profesor_id, update_data.disponibilidad)

@router.post("/generate", response_model=ScheduleGenerationResponse)
async def generate_schedule(
    request: ScheduleGenerationRequest,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(require_jefe_carrera_or_super)
):
    """Generar horarios para una carrera"""
    check_carrera_access(current_user, request.id_carrera)
    
    optimizer = ScheduleOptimizer(db)
    result = optimizer.generate_schedule_for_career(request.id_carrera, request.cuatrimestre)
    
    return ScheduleGenerationResponse(
        success=result["success"],
        message=result["message"],
        generated_schedules=result.get("generated_schedules", [])
    )

@router.get("/grupo/{grupo_id}/horario", response_model=List[HorarioGeneradoResponse])
async def get_grupo_schedule(
    grupo_id: int,
    version: int = 1,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(require_jefe_carrera_or_super)
):
    """Obtener horario de un grupo específico"""
    horario_service = HorarioService(db)
    
    # Verificar acceso (grupo debe pertenecer a la carrera del usuario)
    from app.models import Grupo
    grupo = db.query(Grupo).filter(Grupo.id == grupo_id).first()
    if not grupo:
        raise HTTPException(status_code=404, detail="Grupo no encontrado")
    
    check_carrera_access(current_user, grupo.id_carrera)
    
    return horario_service.get_horario_grupo(grupo_id, version)

@router.post("/import/profesores/{carrera_id}")
async def import_profesores(
    carrera_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(require_jefe_carrera_or_super)
):
    """Importar profesores desde Excel"""
    check_carrera_access(current_user, carrera_id)
    
    if not file.filename.endswith(('.xlsx', '.xls')):
        raise HTTPException(status_code=400, detail="Archivo debe ser formato Excel")
    
    # Guardar archivo temporalmente
    with tempfile.NamedTemporaryFile(delete=False, suffix='.xlsx') as tmp_file:
        content = await file.read()
        tmp_file.write(content)
        tmp_file_path = tmp_file.name
    
    try:
        excel_service = ExcelImportService(db)
        result = excel_service.import_profesores_from_excel(tmp_file_path, carrera_id)
        return result
    finally:
        os.unlink(tmp_file_path)

@router.post("/import/materias/{carrera_id}")
async def import_materias(
    carrera_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(require_jefe_carrera_or_super)
):
    """Importar materias desde Excel"""
    check_carrera_access(current_user, carrera_id)
    
    if not file.filename.endswith(('.xlsx', '.xls')):
        raise HTTPException(status_code=400, detail="Archivo debe ser formato Excel")
    
    # Guardar archivo temporalmente
    with tempfile.NamedTemporaryFile(delete=False, suffix='.xlsx') as tmp_file:
        content = await file.read()
        tmp_file.write(content)
        tmp_file_path = tmp_file.name
    
    try:
        excel_service = ExcelImportService(db)
        result = excel_service.import_materias_from_excel(tmp_file_path, carrera_id)
        return result
    finally:
        os.unlink(tmp_file_path)
