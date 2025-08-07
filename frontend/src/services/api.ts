import axios, { AxiosResponse } from 'axios';
import { 
  Usuario, 
  AuthResponse, 
  LoginForm, 
  Carrera, 
  CreateCarreraForm,
  CreateUsuarioForm,
  Profesor,
  HorarioGenerado,
  ScheduleGenerationRequest,
  ScheduleGenerationResponse,
  UpdateAvailabilityForm
} from '../types';

// Configuración base de axios
const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
});

// Interceptor para agregar token de autenticación
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Interceptor para manejar errores de autenticación
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('access_token');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

// Servicios de autenticación
export const authService = {
  login: async (credentials: LoginForm): Promise<AuthResponse> => {
    const response: AxiosResponse<AuthResponse> = await api.post('/auth/login-json', credentials);
    return response.data;
  },

  logout: () => {
    localStorage.removeItem('access_token');
  },

  isAuthenticated: (): boolean => {
    return !!localStorage.getItem('access_token');
  },

  setToken: (token: string) => {
    localStorage.setItem('access_token', token);
  }
};

// Servicios de administración (Solo Superusuario)
export const adminService = {
  getCarreras: async (): Promise<Carrera[]> => {
    const response: AxiosResponse<Carrera[]> = await api.get('/admin/carreras');
    return response.data;
  },

  createCarrera: async (carrera: CreateCarreraForm): Promise<Carrera> => {
    const response: AxiosResponse<Carrera> = await api.post('/admin/carreras', carrera);
    return response.data;
  },

  createUsuario: async (usuario: CreateUsuarioForm): Promise<Usuario> => {
    const response: AxiosResponse<Usuario> = await api.post('/admin/users', usuario);
    return response.data;
  }
};

// Servicios de gestión de horarios
export const scheduleService = {
  getProfesoresByCarrera: async (carreraId: number): Promise<Profesor[]> => {
    const response: AxiosResponse<Profesor[]> = await api.get(`/schedule/profesores/${carreraId}`);
    return response.data;
  },

  updateProfesorAvailability: async (profesorId: number, data: UpdateAvailabilityForm): Promise<Profesor> => {
    const response: AxiosResponse<Profesor> = await api.put(`/schedule/profesor/${profesorId}/availability`, data);
    return response.data;
  },

  generateSchedule: async (request: ScheduleGenerationRequest): Promise<ScheduleGenerationResponse> => {
    const response: AxiosResponse<ScheduleGenerationResponse> = await api.post('/schedule/generate', request);
    return response.data;
  },

  getGrupoSchedule: async (grupoId: number, version: number = 1): Promise<HorarioGenerado[]> => {
    const response: AxiosResponse<HorarioGenerado[]> = await api.get(`/schedule/grupo/${grupoId}/horario`, {
      params: { version }
    });
    return response.data;
  },

  importProfesores: async (carreraId: number, file: File): Promise<any> => {
    const formData = new FormData();
    formData.append('file', file);
    const response = await api.post(`/schedule/import/profesores/${carreraId}`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data;
  },

  importMaterias: async (carreraId: number, file: File): Promise<any> => {
    const formData = new FormData();
    formData.append('file', file);
    const response = await api.post(`/schedule/import/materias/${carreraId}`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data;
  }
};

// Servicios de registro y perfil
export const registrationService = {
  registerJefeCarrera: async (userData: CreateUsuarioForm, carreraId: number): Promise<Usuario> => {
    const response: AxiosResponse<Usuario> = await api.post(`/register/jefe-carrera`, userData, {
      params: { id_carrera: carreraId }
    });
    return response.data;
  },

  getCarrerasDisponibles: async (): Promise<Carrera[]> => {
    const response: AxiosResponse<Carrera[]> = await api.get('/register/carreras-disponibles');
    return response.data;
  },

  changePassword: async (currentPassword: string, newPassword: string): Promise<any> => {
    const response = await api.post('/register/change-password', {
      current_password: currentPassword,
      new_password: newPassword
    });
    return response.data;
  },

  getUserProfile: async (): Promise<Usuario> => {
    const response: AxiosResponse<Usuario> = await api.get('/register/profile');
    return response.data;
  }
};

export default api;
