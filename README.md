# SIGAH - Sistema de Gestión y Generación Automática de Horarios Universitarios

## Descripción del Proyecto

SIGAH es una aplicación web completa para la administración y generación automática de horarios académicos en universidades. El sistema gestiona profesores, materias, carreras y grupos para asignar clases de manera óptima utilizando algoritmos de optimización avanzados.

## Características Principales

### ✅ **Sistema de Usuarios y Roles**
- **Superusuario**: Control total sobre la plataforma
- **Jefe de Carrera**: Gestión restringida a su carrera específica
- **Módulo de Registro**: Registro de nuevos Jefes de Carrera por Superusuario
- **Gestión de Perfiles**: Cambio de contraseñas y actualización de datos
- **Alumnos**: Acceso público a horarios (sin autenticación)

### ✅ **Gestión de Datos**
- Importación masiva desde archivos Excel (.xlsx/.csv)
- CRUD completo para Carreras, Materias, Profesores y Grupos
- Control de acceso basado en roles

### ✅ **Motor de Optimización**
- **Google OR-Tools CP-SAT Solver** para generación automática
- **Restricciones Duras**: Sin conflictos de tiempo, cumplimiento de horas
- **Restricciones Suaves**: Minimización de huecos, optimización PTC (40 horas)
- **2 versiones de horario** por cada grupo automáticamente

### ✅ **Visualización y Exportación**
- Grids de horarios para alumnos, profesores y administradores
- Exportación a **PNG**, **PDF** y **Excel**
- Formatos específicos según requerimientos académicos

## Arquitectura Técnica

### **Backend - FastAPI (Python)**
```
backend/
├── app/
│   ├── api/                 # Rutas de la API REST
│   ├── core/                # Configuración, seguridad, BD
│   ├── models/              # Modelos SQLAlchemy
│   ├── schemas/             # Esquemas Pydantic
│   ├── services/            # Lógica de negocio
│   └── main.py             # Aplicación principal
├── alembic/                # Migraciones de BD
├── requirements.txt        # Dependencias Python
└── .env.example           # Variables de entorno
```

### **Frontend - React (TypeScript)**
```
frontend/
├── src/
│   ├── components/         # Componentes reutilizables
│   ├── pages/             # Páginas principales
│   ├── services/          # Servicios de API
│   ├── types/             # Tipos TypeScript
│   └── App.tsx            # Componente raíz
├── public/                # Archivos estáticos
├── package.json           # Dependencias Node.js
└── tsconfig.json          # Configuración TypeScript
```

### **Base de Datos - PostgreSQL**
- **Carrera**: Información de carreras universitarias
- **Usuario**: Sistema de autenticación y roles
- **Profesor**: Datos y disponibilidad horaria
- **Materia**: Materias con horas semanales por cuatrimestre
- **Grupo**: Grupos de estudiantes por carrera/cuatrimestre
- **HorarioGenerado**: Resultados de la optimización

## Dependencias Principales

### Backend
- **FastAPI 0.104.1**: Framework web moderno y rápido
- **SQLAlchemy 2.0.23**: ORM para base de datos
- **PostgreSQL** (psycopg2-binary): Base de datos principal
- **Google OR-Tools 9.8**: Motor de optimización
- **JWT** (python-jose): Autenticación y autorización
- **Pandas 2.1.3**: Procesamiento de datos Excel
- **Alembic**: Migraciones de base de datos

### Frontend
- **React 18.2**: Framework de interfaz de usuario
- **TypeScript**: Tipado estático
- **Material-UI (MUI)**: Componentes de interfaz
- **React Router**: Navegación SPA
- **Axios**: Cliente HTTP para API
- **jsPDF & html2canvas**: Exportación de documentos

## Instalación y Configuración

### Prerrequisitos
- **Python 3.8+**
- **Node.js 16+**
- **PostgreSQL 12+**
- **Git**

### 1. Configuración del Backend

```bash
# Navegar al directorio backend
cd backend

# Crear entorno virtual
python -m venv venv

# Activar entorno virtual (Windows)
venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt

# Configurar variables de entorno
copy .env.example .env
# Editar .env con tus credenciales de PostgreSQL
```

### 2. Configuración de Base de Datos

```bash
# Crear base de datos PostgreSQL
createdb sigah_db

# Ejecutar migraciones
cd backend
alembic upgrade head

# Inicializar con datos básicos y superusuario
python init_db.py
```

**Usuario por Defecto Creado:**
- **Email**: `admin@universidad.edu`
- **Contraseña**: `admin123`
- **Rol**: Superusuario
- ⚠️ **CAMBIAR CONTRASEÑA EN PRODUCCIÓN**

### 3. Configuración del Frontend

```bash
# Navegar al directorio frontend
cd frontend

# Instalar dependencias
npm install

# (Opcional) Configurar variables de entorno
echo "REACT_APP_API_URL=http://localhost:8000" > .env
```

## Ejecución del Proyecto

### Desarrollo Local

**Terminal 1 - Backend:**
```bash
cd backend
venv\Scripts\activate  # Windows
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm start
```

**Accesos:**
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **Documentación API**: http://localhost:8000/docs

### Usuario por Defecto
Después de ejecutar `python init_db.py`:
- **Email**: `admin@universidad.edu`
- **Contraseña**: `admin123`
- **Rol**: Superusuario

⚠️ **IMPORTANTE**: Cambiar la contraseña del superusuario después del primer login.

## Variables de Entorno

### Backend (.env)
```bash
DATABASE_URL=postgresql://username:password@localhost:5432/sigah_db
SECRET_KEY=tu-clave-secreta-muy-segura-cambiar-en-produccion
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
DEBUG=True
```

### Frontend (.env) - Opcional
```bash
REACT_APP_API_URL=http://localhost:8000
```

## Funcionalidades Implementadas

### 🔐 **Autenticación y Autorización**
- JWT tokens para sesiones seguras
- Control de acceso basado en roles
- Middleware de autenticación automática

### 📊 **Gestión de Datos**
- Importación Excel para Profesores y Materias
- Validación automática de datos
- Interfaz CRUD para todas las entidades

### 🧠 **Motor de Optimización (Google OR-Tools)**
- Algoritmo CP-SAT para asignación óptima
- Restricciones duras: sin conflictos temporales
- Restricciones suaves: minimización de huecos
- Generación de múltiples opciones de horario

### 📱 **Interfaz de Usuario**
- Dashboard especializado por rol
- Grids de horarios interactivos
- Importación drag-and-drop de archivos
- Exportación multi-formato

### 📈 **Reportes y Exportación**
- Horarios por grupo (estudiantes)
- Horarios por profesor
- Resumen de asignación docente
- Formatos: PNG, PDF, Excel

## Estructura de la API

### Endpoints Principales

**Autenticación:**
- `POST /auth/login` - Inicio de sesión
- `POST /auth/login-json` - Login con JSON

**Administración (Solo Superusuario):**
- `GET /admin/carreras` - Listar carreras
- `POST /admin/carreras` - Crear carrera
- `POST /admin/users` - Crear usuario

**Registro y Perfil:**
- `POST /register/jefe-carrera` - Registrar Jefe de Carrera
- `GET /register/carreras-disponibles` - Carreras sin jefe asignado
- `POST /register/change-password` - Cambiar contraseña
- `GET /register/profile` - Obtener perfil de usuario

**Gestión de Horarios:**
- `GET /schedule/profesores/{carrera_id}` - Profesores por carrera
- `PUT /schedule/profesor/{id}/availability` - Actualizar disponibilidad
- `POST /schedule/generate` - Generar horarios
- `GET /schedule/grupo/{id}/horario` - Obtener horario de grupo
- `POST /schedule/import/profesores/{carrera_id}` - Importar profesores
- `POST /schedule/import/materias/{carrera_id}` - Importar materias

## Algoritmo de Optimización

El sistema utiliza **Google OR-Tools CP-SAT** con las siguientes restricciones:

### Restricciones Duras (Obligatorias)
1. **Sin doble asignación de profesores**: Un profesor no puede estar en dos lugares simultáneamente
2. **Sin solapamiento de grupos**: Un grupo no puede tener dos materias al mismo tiempo
3. **Respeto de disponibilidad**: Las clases solo se asignan en horarios disponibles del profesor
4. **Cumplimiento de horas**: Cada materia debe cumplir sus horas semanales requeridas

### Restricciones Suaves (Objetivos de Optimización)
1. **Minimización de huecos**: Reduce espacios vacíos en horarios de grupos
2. **Agrupación de profesores**: Evita que los profesores tengan clases muy dispersas
3. **Optimización PTC**: Los profesores de tiempo completo tienden hacia 40 horas semanales

## Próximas Mejoras

- [ ] Dashboard para Superusuario
- [ ] Exportación avanzada con plantillas personalizables
- [ ] Notificaciones en tiempo real
- [ ] API para consulta pública de horarios
- [ ] Móvil responsivo mejorado
- [ ] Cache y optimización de rendimiento
- [ ] Tests automatizados
- [ ] Deployment con Docker

## Contribución

1. Fork del repositorio
2. Crear rama feature (`git checkout -b feature/nueva-funcionalidad`)
3. Commit cambios (`git commit -am 'Agregar nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Crear Pull Request

## Licencia

Este proyecto está bajo licencia MIT. Ver el archivo `LICENSE` para más detalles.

## Soporte

Para soporte técnico o preguntas sobre el sistema:
- Crear un issue en GitHub
- Contactar al equipo de desarrollo
- Revisar la documentación de la API en `/docs`

---

**SIGAH v1.0.0** - Sistema desarrollado para optimizar la gestión de horarios universitarios mediante tecnologías modernas y algoritmos de optimización avanzados.
