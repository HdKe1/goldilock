// Add these to your existing api.js file
import axios from "axios";
import { ACCESS_TOKEN } from "./constants";

const apiUrl = "/choreo-apis/goldilock/backend/v1";

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL ? import.meta.env.VITE_API_URL : apiUrl,
});

api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem(ACCESS_TOKEN);
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);


export const saveWPMAttempt = async (wpm) => {
  try {
    const response = await api.post('/api/save-attempt/', { wpm });
    return response.data;
  } catch (error) {
    console.error('Error saving WPM:', error);
    throw error;
  }
};

export const getUserStats = async () => {
  try {
    const response = await api.get('/api/user-stats/');
    return response.data;
  } catch (error) {
    console.error('Error fetching stats:', error);
    throw error;
  }
};

export default api;