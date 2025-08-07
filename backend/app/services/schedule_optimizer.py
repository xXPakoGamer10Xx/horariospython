from typing import List, Optional, Dict, Any
from datetime import time, datetime, timedelta
from ortools.sat.python import cp_model
from sqlalchemy.orm import Session
from app.models import Grupo, Materia, Profesor, HorarioGenerado
from app.models.models import DiaSemanaEnum, TipoProfesorEnum

class ScheduleOptimizer:
    """Motor de optimización de horarios usando Google OR-Tools CP-SAT"""
    
    def __init__(self, db: Session):
        self.db = db
        self.model = cp_model.CpModel()
        self.solver = cp_model.CpSolver()
        
        # Configuración de tiempo
        self.dias_semana = list(DiaSemanaEnum)
        self.horas_inicio = [7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]  # 7:00 AM a 8:00 PM
        self.max_horas_diarias = 8
        
    def generate_schedule_for_career(self, id_carrera: int, cuatrimestre: Optional[int] = None) -> Dict[str, Any]:
        """
        Genera horarios para una carrera específica
        Returns: Dict con success, message y horarios generados
        """
        try:
            # Obtener grupos de la carrera
            query = self.db.query(Grupo).filter(Grupo.id_carrera == id_carrera)
            if cuatrimestre:
                query = query.filter(Grupo.cuatrimestre == cuatrimestre)
            grupos = query.all()
            
            if not grupos:
                return {"success": False, "message": "No se encontraron grupos para procesar"}
            
            results = []
            for grupo in grupos:
                # Generar 2 versiones de horario para cada grupo
                for version in [1, 2]:
                    schedule_result = self._generate_schedule_for_group(grupo, version)
                    if schedule_result["success"]:
                        results.append(grupo.id)
            
            return {
                "success": True,
                "message": f"Horarios generados exitosamente para {len(results)} grupos",
                "generated_schedules": results
            }
            
        except Exception as e:
            return {"success": False, "message": f"Error en la generación: {str(e)}"}
    
    def _generate_schedule_for_group(self, grupo: Grupo, version: int) -> Dict[str, Any]:
        """Genera un horario específico para un grupo"""
        try:
            # Limpiar horarios existentes para esta versión
            self.db.query(HorarioGenerado).filter(
                HorarioGenerado.id_grupo == grupo.id,
                HorarioGenerado.version_horario == version
            ).delete()
            
            # Obtener materias del cuatrimestre
            materias = self.db.query(Materia).filter(
                Materia.id_carrera == grupo.id_carrera,
                Materia.cuatrimestre == grupo.cuatrimestre
            ).all()
            
            # Obtener profesores disponibles
            profesores = self.db.query(Profesor).filter(
                Profesor.id_carrera == grupo.id_carrera
            ).all()
            
            if not materias or not profesores:
                return {"success": False, "message": "Datos insuficientes"}
            
            # Crear variables de decisión
            assignments = self._create_decision_variables(materias, profesores)
            
            # Agregar restricciones
            self._add_constraints(assignments, materias, profesores, grupo)
            
            # Resolver el modelo
            status = self.solver.Solve(self.model)
            
            if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
                self._save_solution(assignments, materias, profesores, grupo, version)
                return {"success": True, "message": "Horario generado exitosamente"}
            else:
                return {"success": False, "message": "No se pudo encontrar una solución factible"}
                
        except Exception as e:
            return {"success": False, "message": f"Error: {str(e)}"}
    
    def _create_decision_variables(self, materias: List[Materia], profesores: List[Profesor]) -> Dict:
        """Crea las variables de decisión del modelo"""
        assignments = {}
        
        for materia in materias:
            for profesor in profesores:
                for dia_idx, dia in enumerate(self.dias_semana):
                    for hora in self.horas_inicio:
                        # Variable: materia m, profesor p, día d, hora h está asignada
                        var_name = f"assign_{materia.id}_{profesor.id}_{dia_idx}_{hora}"
                        assignments[var_name] = self.model.NewBoolVar(var_name)
        
        return assignments
    
    def _add_constraints(self, assignments: Dict, materias: List[Materia], 
                        profesores: List[Profesor], grupo: Grupo):
        """Agrega todas las restricciones al modelo"""
        
        # Restricción 1: Cada materia debe cumplir sus horas semanales
        for materia in materias:
            materia_assignments = []
            for profesor in profesores:
                for dia_idx in range(len(self.dias_semana)):
                    for hora in self.horas_inicio:
                        var_name = f"assign_{materia.id}_{profesor.id}_{dia_idx}_{hora}"
                        if var_name in assignments:
                            materia_assignments.append(assignments[var_name])
            
            self.model.Add(sum(materia_assignments) == materia.horas_semanales)
        
        # Restricción 2: Un profesor no puede estar en dos lugares al mismo tiempo
        for profesor in profesores:
            for dia_idx in range(len(self.dias_semana)):
                for hora in self.horas_inicio:
                    profesor_hour_assignments = []
                    for materia in materias:
                        var_name = f"assign_{materia.id}_{profesor.id}_{dia_idx}_{hora}"
                        if var_name in assignments:
                            profesor_hour_assignments.append(assignments[var_name])
                    
                    self.model.Add(sum(profesor_hour_assignments) <= 1)
        
        # Restricción 3: El grupo no puede tener dos materias al mismo tiempo
        for dia_idx in range(len(self.dias_semana)):
            for hora in self.horas_inicio:
                group_hour_assignments = []
                for materia in materias:
                    for profesor in profesores:
                        var_name = f"assign_{materia.id}_{profesor.id}_{dia_idx}_{hora}"
                        if var_name in assignments:
                            group_hour_assignments.append(assignments[var_name])
                
                self.model.Add(sum(group_hour_assignments) <= 1)
        
        # Restricción 4: Disponibilidad de profesores
        self._add_availability_constraints(assignments, materias, profesores)
        
        # Restricción 5: Optimización para PTC (40 horas semanales)
        self._add_ptc_optimization(assignments, materias, profesores)
    
    def _add_availability_constraints(self, assignments: Dict, materias: List[Materia], 
                                    profesores: List[Profesor]):
        """Agrega restricciones de disponibilidad de profesores"""
        for profesor in profesores:
            if not profesor.disponibilidad:
                continue
                
            for dia_idx, dia in enumerate(self.dias_semana):
                dia_name = dia.value
                if dia_name not in profesor.disponibilidad:
                    # Profesor no disponible este día
                    for hora in self.horas_inicio:
                        for materia in materias:
                            var_name = f"assign_{materia.id}_{profesor.id}_{dia_idx}_{hora}"
                            if var_name in assignments:
                                self.model.Add(assignments[var_name] == 0)
                else:
                    # Verificar rangos horarios disponibles
                    available_hours = self._parse_availability(profesor.disponibilidad[dia_name])
                    for hora in self.horas_inicio:
                        if hora not in available_hours:
                            for materia in materias:
                                var_name = f"assign_{materia.id}_{profesor.id}_{dia_idx}_{hora}"
                                if var_name in assignments:
                                    self.model.Add(assignments[var_name] == 0)
    
    def _parse_availability(self, time_ranges: List[str]) -> List[int]:
        """Convierte rangos de tiempo a lista de horas disponibles"""
        available_hours = []
        for time_range in time_ranges:
            start_str, end_str = time_range.split("-")
            start_hour = int(start_str.split(":")[0])
            end_hour = int(end_str.split(":")[0])
            available_hours.extend(range(start_hour, end_hour))
        return available_hours
    
    def _add_ptc_optimization(self, assignments: Dict, materias: List[Materia], 
                            profesores: List[Profesor]):
        """Optimización para profesores de tiempo completo (40 horas)"""
        for profesor in profesores:
            if profesor.tipo_profesor == TipoProfesorEnum.PTC:
                total_hours = []
                for materia in materias:
                    for dia_idx in range(len(self.dias_semana)):
                        for hora in self.horas_inicio:
                            var_name = f"assign_{materia.id}_{profesor.id}_{dia_idx}_{hora}"
                            if var_name in assignments:
                                total_hours.append(assignments[var_name])
                
                # Objetivo: acercarse a 40 horas (ajustable según necesidades)
                if total_hours:
                    self.model.Add(sum(total_hours) >= 20)  # Mínimo 20 horas
                    self.model.Add(sum(total_hours) <= 40)  # Máximo 40 horas
    
    def _save_solution(self, assignments: Dict, materias: List[Materia], 
                      profesores: List[Profesor], grupo: Grupo, version: int):
        """Guarda la solución en la base de datos"""
        for materia in materias:
            for profesor in profesores:
                for dia_idx, dia in enumerate(self.dias_semana):
                    for hora in self.horas_inicio:
                        var_name = f"assign_{materia.id}_{profesor.id}_{dia_idx}_{hora}"
                        if var_name in assignments and self.solver.Value(assignments[var_name]) == 1:
                            # Crear registro de horario
                            horario = HorarioGenerado(
                                id_grupo=grupo.id,
                                id_materia=materia.id,
                                id_profesor=profesor.id,
                                dia_semana=dia,
                                hora_inicio=time(hora, 0),
                                hora_fin=time(hora + 1, 0),  # Asumiendo clases de 1 hora
                                version_horario=version
                            )
                            self.db.add(horario)
        
        self.db.commit()
