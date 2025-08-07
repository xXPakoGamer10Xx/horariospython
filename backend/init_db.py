"""
Script para inicializar la base de datos con datos básicos
Ejecutar después de las migraciones de Alembic
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy.orm import Session
from app.core.database import SessionLocal, engine
from app.models import Base, Usuario, Carrera, RolEnum
from app.core.security import get_password_hash

def create_initial_data():
    """Crear datos iniciales del sistema"""
    
    # Crear todas las tablas
    Base.metadata.create_all(bind=engine)
    
    db: Session = SessionLocal()
    
    try:
        # Verificar si ya existe un superusuario
        existing_super = db.query(Usuario).filter(Usuario.rol == RolEnum.SUPERUSUARIO).first()
        if existing_super:
            print("Ya existe un superusuario en el sistema")
            return
        
        # Crear carreras de ejemplo
        carreras_ejemplo = [
            "Ingeniería en Sistemas Computacionales",
            "Ingeniería Industrial",
            "Ingeniería Mecatrónica",
            "Licenciatura en Administración",
            "Contador Público"
        ]
        
        carreras_creadas = []
        for nombre_carrera in carreras_ejemplo:
            existing_carrera = db.query(Carrera).filter(Carrera.nombre == nombre_carrera).first()
            if not existing_carrera:
                carrera = Carrera(nombre=nombre_carrera)
                db.add(carrera)
                carreras_creadas.append(nombre_carrera)
        
        db.commit()
        
        if carreras_creadas:
            print(f"Carreras creadas: {', '.join(carreras_creadas)}")
        
        # Crear superusuario por defecto
        superuser = Usuario(
            email="admin@universidad.edu",
            password=get_password_hash("admin123"),  # Cambiar en producción
            nombre_completo="Administrador del Sistema",
            rol=RolEnum.SUPERUSUARIO,
            id_carrera=None
        )
        
        db.add(superuser)
        db.commit()
        
        print("✅ Datos iniciales creados exitosamente:")
        print(f"   📧 Email: admin@universidad.edu")
        print(f"   🔑 Contraseña: admin123")
        print(f"   👤 Rol: Superusuario")
        print(f"   ⚠️  IMPORTANTE: Cambiar la contraseña en producción")
        
    except Exception as e:
        print(f"❌ Error al crear datos iniciales: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    print("🚀 Inicializando base de datos con datos básicos...")
    create_initial_data()
    print("✨ Proceso completado")
