import axios from 'axios';

const API_BASE_URL = 'http://127.0.0.1:8000/api/v1';

// Configuración para mostrar logs detallados en desarrollo
const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Interceptor para logs
api.interceptors.request.use(request => {
  console.log('API Request:', request.method.toUpperCase(), request.url, request.params || {});
  return request;
});

api.interceptors.response.use(
  response => {
    console.log('API Response:', response.status, response.config.url);
    return response;
  },
  error => {
    console.error('API Error:', error.response?.status, error.response?.data || error.message);
    return Promise.reject(error);
  }
);

export const carrerasService = {
  getAll: async () => {
    try {
      const response = await api.get('/carreras/');
      return response.data;
    } catch (error) {
      console.error('Error al obtener carreras:', error);
      throw error;
    }
  },
};

export const pensumsService = {
  getByCarrera: async (carreraId) => {
    try {
      const response = await api.get(`/pensums/by-carrera/${carreraId}`);
      return response.data;
    } catch (error) {
      console.error('Error al obtener pensums:', error);
      throw error;
    }
  },
};

export const prerrequisitosService = {
  getRutaPorCodigo: async (codigo, pensumId) => {
    try {
      console.log(`Consultando ruta para: ${codigo}, pensum: ${pensumId}`);
      const response = await api.get(`/prerrequisitos/ruta-por-codigo/${codigo}`, {
        params: { pensum_id: pensumId },
      });
      return response.data;
    } catch (error) {
      // Extraer el mensaje de error específico si existe
      const errorMessage = error.response?.data?.error || 
                          error.response?.data?.detail || 
                          'Error al obtener ruta académica';
      console.error('Error detallado:', errorMessage);
      
      // Si hay un mensaje de error detallado, lo incluimos en el objeto error
      if (errorMessage) {
        error.userMessage = errorMessage;
      }
      
      throw error;
    }
  }
};

export default {
  carrerasService,
  pensumsService,
  prerrequisitosService,
};