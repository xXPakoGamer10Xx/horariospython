-- Script para crear la base de datos SIGAH en MySQL (XAMPP)
-- Ejecutar este script en phpMyAdmin

-- Crear la base de datos
CREATE DATABASE IF NOT EXISTS sigah_db 
CHARACTER SET utf8mb4 
COLLATE utf8mb4_unicode_ci;

-- Usar la base de datos
USE sigah_db;

-- Verificar que la base de datos se creó correctamente
SHOW TABLES;

-- El script está listo. Las tablas se crearán automáticamente cuando ejecutes el backend
-- con Alembic migrations.
