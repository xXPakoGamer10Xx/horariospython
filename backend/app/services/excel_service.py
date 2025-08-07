import pandas as pd
from typing import List, Dict, Any
from sqlalchemy.orm import Session
from app.models import Profesor, Materia
from app.models.models import TipoProfesorEnum

class ExcelImportService:
    """Servicio para importación de datos desde Excel"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def import_profesores_from_excel(self, file_path: str, carrera_id: int) -> Dict[str, Any]:
        """
        Importa profesores desde archivo Excel
        Asume columnas: numero_empleado, nombre_completo, tipo_profesor
        """
        try:
            df = pd.read_excel(file_path)
            
            # Validar columnas requeridas
            required_columns = ['numero_empleado', 'nombre_completo', 'tipo_profesor']
            if not all(col in df.columns for col in required_columns):
                return {
                    "success": False, 
                    "message": f"Columnas requeridas: {required_columns}"
                }
            
            imported_count = 0
            errors = []
            
            for index, row in df.iterrows():
                try:
                    # Validar tipo de profesor
                    tipo_profesor = row['tipo_profesor'].upper()
                    if tipo_profesor not in [e.value for e in TipoProfesorEnum]:
                        errors.append(f"Fila {index + 1}: Tipo de profesor inválido: {tipo_profesor}")
                        continue
                    
                    # Verificar si el profesor ya existe
                    existing = self.db.query(Profesor).filter(
                        Profesor.numero_empleado == str(row['numero_empleado'])
                    ).first()
                    
                    if existing:
                        errors.append(f"Fila {index + 1}: Profesor ya existe: {row['numero_empleado']}")
                        continue
                    
                    # Crear nuevo profesor
                    profesor = Profesor(
                        numero_empleado=str(row['numero_empleado']),
                        nombre_completo=str(row['nombre_completo']),
                        id_carrera=carrera_id,
                        tipo_profesor=TipoProfesorEnum(tipo_profesor),
                        disponibilidad={}  # Se configurará después
                    )
                    
                    self.db.add(profesor)
                    imported_count += 1
                    
                except Exception as e:
                    errors.append(f"Fila {index + 1}: {str(e)}")
            
            self.db.commit()
            
            return {
                "success": True,
                "message": f"Importados {imported_count} profesores",
                "imported_count": imported_count,
                "errors": errors
            }
            
        except Exception as e:
            self.db.rollback()
            return {"success": False, "message": f"Error al procesar archivo: {str(e)}"}
    
    def import_materias_from_excel(self, file_path: str, carrera_id: int) -> Dict[str, Any]:
        """
        Importa materias desde archivo Excel
        Asume columnas: nombre_materia, cuatrimestre, horas_semanales
        """
        try:
            df = pd.read_excel(file_path)
            
            # Validar columnas requeridas
            required_columns = ['nombre_materia', 'cuatrimestre', 'horas_semanales']
            if not all(col in df.columns for col in required_columns):
                return {
                    "success": False, 
                    "message": f"Columnas requeridas: {required_columns}"
                }
            
            imported_count = 0
            errors = []
            
            for index, row in df.iterrows():
                try:
                    # Validar datos
                    cuatrimestre = int(row['cuatrimestre'])
                    horas_semanales = int(row['horas_semanales'])
                    
                    if cuatrimestre < 1 or cuatrimestre > 10:
                        errors.append(f"Fila {index + 1}: Cuatrimestre debe estar entre 1 y 10")
                        continue
                    
                    if horas_semanales < 1 or horas_semanales > 10:
                        errors.append(f"Fila {index + 1}: Horas semanales debe estar entre 1 y 10")
                        continue
                    
                    # Verificar si la materia ya existe
                    existing = self.db.query(Materia).filter(
                        Materia.nombre_materia == str(row['nombre_materia']),
                        Materia.id_carrera == carrera_id,
                        Materia.cuatrimestre == cuatrimestre
                    ).first()
                    
                    if existing:
                        errors.append(f"Fila {index + 1}: Materia ya existe: {row['nombre_materia']}")
                        continue
                    
                    # Crear nueva materia
                    materia = Materia(
                        nombre_materia=str(row['nombre_materia']),
                        id_carrera=carrera_id,
                        cuatrimestre=cuatrimestre,
                        horas_semanales=horas_semanales
                    )
                    
                    self.db.add(materia)
                    imported_count += 1
                    
                except Exception as e:
                    errors.append(f"Fila {index + 1}: {str(e)}")
            
            self.db.commit()
            
            return {
                "success": True,
                "message": f"Importadas {imported_count} materias",
                "imported_count": imported_count,
                "errors": errors
            }
            
        except Exception as e:
            self.db.rollback()
            return {"success": False, "message": f"Error al procesar archivo: {str(e)}"}
