# Guía de Configuración SIGAH con XAMPP

## Prerrequisitos
- XAMPP instalado y funcionando
- Python 3.8+ con el entorno virtual activado

## Pasos de Configuración

### 1. Iniciar XAMPP
1. Abre el panel de control de XAMPP
2. Inicia **Apache** y **MySQL**
3. Verifica que ambos servicios estén corriendo (luz verde)

### 2. Crear la Base de Datos
1. Ve a `http://localhost/phpmyadmin`
2. Haz clic en "New" o "Nueva" en el panel izquierdo
3. Nombre de la base de datos: `sigah_db`
4. Collation: `utf8mb4_unicode_ci`
5. Haz clic en "Create" o "Crear"

**Alternativa**: Ejecuta el archivo SQL:
- Ve a phpMyAdmin → Import → Selecciona `create_database_mysql.sql`

### 3. Configurar el Backend

#### a) Activar el entorno virtual (si no está activo)
```powershell
cd "C:\Users\pakog\Documents\Horarios"
.\.venv\Scripts\Activate.ps1
```

#### b) Ir al directorio del backend
```powershell
cd backend
```

#### c) Ejecutar el script de configuración automática
```powershell
python setup_xampp.py
```

**Si el script automático falla, ejecuta manualmente:**

#### d) Ejecutar migraciones (manual)
```powershell
alembic upgrade head
```

#### e) Inicializar datos básicos (manual)
```powershell
python init_db.py
```

### 4. Iniciar el Backend
```powershell
uvicorn main:app --reload
```

### 5. Verificar el Sistema
- **Frontend**: http://localhost:3000 (ya está corriendo)
- **Backend**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **phpMyAdmin**: http://localhost/phpmyadmin

### 6. Credenciales de Prueba
- **Email**: admin@universidad.edu
- **Contraseña**: admin123

## Solución de Problemas

### Error: "Can't connect to MySQL server"
- Verifica que MySQL esté corriendo en XAMPP
- Revisa que el puerto sea 3306
- Reinicia MySQL en XAMPP

### Error: "Database doesn't exist"
- Asegúrate de haber creado la base de datos `sigah_db`
- Verifica el nombre de la base de datos en phpMyAdmin

### Error: "Table doesn't exist"
- Ejecuta las migraciones: `alembic upgrade head`
- Si falla, ejecuta: `alembic revision --autogenerate -m "Initial migration"`

### Error de autenticación
- Verifica que `init_db.py` se haya ejecutado correctamente
- Revisa los logs del backend para errores

## Estructura de la Base de Datos
Después de las migraciones, deberías ver estas tablas en phpMyAdmin:
- `alembic_version`
- `usuarios`
- `carreras`
- `profesores`
- `materias`
- `grupos`
- `horarios_generados`

## Configuración Actual
- **Host**: localhost
- **Puerto**: 3306
- **Usuario**: root
- **Contraseña**: (vacía)
- **Base de datos**: sigah_db
