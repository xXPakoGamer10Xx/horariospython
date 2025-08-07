// Tipos para el sistema SIGAH

export interface Usuario {
  id: number;
  email: string;
  nombre_completo: string;
  rol: 'SUPERUSUARIO' | 'JEFE_CARRERA';
  id_carrera?: number;
  carrera?: Carrera;
}

export interface Carrera {
  id: number;
  nombre: string;
}

export interface Profesor {
  id: number;
  numero_empleado: string;
  nombre_completo: string;
  id_carrera: number;
  tipo_profesor: 'PTC' | 'PA';
  disponibilidad?: { [dia: string]: string[] };
  carrera: Carrera;
}

export interface Materia {
  id: number;
  nombre_materia: string;
  id_carrera: number;
  cuatrimestre: number;
  horas_semanales: number;
  carrera: Carrera;
}

export interface Grupo {
  id: number;
  id_carrera: number;
  cuatrimestre: number;
  nombre_grupo?: string;
  carrera: Carrera;
}

export interface HorarioGenerado {
  id: number;
  grupo: Grupo;
  materia: Materia;
  profesor: Profesor;
  dia_semana: 'Lunes' | 'Martes' | 'Miércoles' | 'Jueves' | 'Viernes' | 'Sábado';
  hora_inicio: string;
  hora_fin: string;
  version_horario: number;
}

export interface AuthResponse {
  access_token: string;
  token_type: string;
}

export interface ScheduleGenerationRequest {
  id_carrera: number;
  cuatrimestre?: number;
}

export interface ScheduleGenerationResponse {
  success: boolean;
  message: string;
  generated_schedules: number[];
}

// Tipos para formularios
export interface LoginForm {
  email: string;
  password: string;
}

export interface CreateUsuarioForm {
  email: string;
  password: string;
  nombre_completo: string;
  rol: 'SUPERUSUARIO' | 'JEFE_CARRERA';
  id_carrera?: number;
}

export interface CreateCarreraForm {
  nombre: string;
}

export interface UpdateAvailabilityForm {
  disponibilidad: { [dia: string]: string[] };
}

// Tipos adicionales para registro
export interface UserProfile {
  id: number;
  email: string;
  nombre_completo: string;
  rol: 'SUPERUSUARIO' | 'JEFE_CARRERA';
  carrera?: Carrera;
}

export interface PasswordChangeForm {
  currentPassword: string;
  newPassword: string;
  confirmPassword: string;
}
