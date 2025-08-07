#!/usr/bin/env python3
"""
Script para configurar SIGAH con XAMPP MySQL
Ejecutar este script después de:
1. Iniciar XAMPP (Apache y MySQL)
2. Crear la base de datos 'sigah_db' en phpMyAdmin
"""

import os
import sys
import subprocess
from pathlib import Path

def check_mysql_connection():
    """Verificar conexión a MySQL"""
    try:
        import pymysql
        connection = pymysql.connect(
            host='localhost',
            user='root',
            password='',
            port=3306
        )
        print("✅ Conexión a MySQL exitosa")
        connection.close()
        return True
    except Exception as e:
        print(f"❌ Error conectando a MySQL: {e}")
        print("Asegúrate de que XAMPP esté ejecutándose")
        return False

def check_database_exists():
    """Verificar si la base de datos existe"""
    try:
        import pymysql
        connection = pymysql.connect(
            host='localhost',
            user='root',
            password='',
            port=3306
        )
        cursor = connection.cursor()
        cursor.execute("SHOW DATABASES LIKE 'sigah_db'")
        result = cursor.fetchone()
        connection.close()
        
        if result:
            print("✅ Base de datos 'sigah_db' encontrada")
            return True
        else:
            print("❌ Base de datos 'sigah_db' no encontrada")
            return False
    except Exception as e:
        print(f"❌ Error verificando base de datos: {e}")
        return False

def create_database():
    """Crear la base de datos si no existe"""
    try:
        import pymysql
        connection = pymysql.connect(
            host='localhost',
            user='root',
            password='',
            port=3306
        )
        cursor = connection.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS sigah_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
        connection.commit()
        connection.close()
        print("✅ Base de datos 'sigah_db' creada")
        return True
    except Exception as e:
        print(f"❌ Error creando base de datos: {e}")
        return False

def run_migrations():
    """Ejecutar migraciones de Alembic"""
    try:
        print("🔄 Ejecutando migraciones...")
        result = subprocess.run(["alembic", "upgrade", "head"], capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Migraciones ejecutadas exitosamente")
            return True
        else:
            print(f"❌ Error en migraciones: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ Error ejecutando migraciones: {e}")
        return False

def initialize_data():
    """Inicializar datos básicos"""
    try:
        print("🔄 Inicializando datos básicos...")
        result = subprocess.run([sys.executable, "init_db.py"], capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Datos iniciales creados exitosamente")
            print("👤 Usuario administrador creado:")
            print("   Email: admin@universidad.edu")
            print("   Contraseña: admin123")
            return True
        else:
            print(f"❌ Error inicializando datos: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ Error inicializando datos: {e}")
        return False

def main():
    print("🚀 Configurando SIGAH para XAMPP MySQL")
    print("=" * 50)
    
    # Verificar conexión a MySQL
    if not check_mysql_connection():
        print("\n📋 Pasos para solucionar:")
        print("1. Asegúrate de que XAMPP esté ejecutándose")
        print("2. Inicia el servicio MySQL en el panel de XAMPP")
        print("3. Verifica que MySQL esté corriendo en el puerto 3306")
        return False
    
    # Verificar/crear base de datos
    if not check_database_exists():
        print("🔄 Creando base de datos...")
        if not create_database():
            return False
    
    # Ejecutar migraciones
    if not run_migrations():
        print("\n📋 Si las migraciones fallan:")
        print("1. Ejecuta: alembic revision --autogenerate -m 'Initial migration'")
        print("2. Luego: alembic upgrade head")
        return False
    
    # Inicializar datos
    if not initialize_data():
        return False
    
    print("\n🎉 ¡Configuración completada exitosamente!")
    print("\n📋 Próximos pasos:")
    print("1. Ejecuta el backend: uvicorn main:app --reload")
    print("2. El frontend ya está corriendo en http://localhost:3000")
    print("3. Inicia sesión con: admin@universidad.edu / admin123")
    print("\n🔗 URLs importantes:")
    print("   Frontend: http://localhost:3000")
    print("   Backend: http://localhost:8000")
    print("   API Docs: http://localhost:8000/docs")
    print("   phpMyAdmin: http://localhost/phpmyadmin")
    
    return True

if __name__ == "__main__":
    main()
