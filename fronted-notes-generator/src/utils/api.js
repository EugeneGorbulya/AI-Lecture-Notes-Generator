import axios from 'axios';
import { getToken } from './auth';

const API = axios.create({
  baseURL: 'http://127.0.0.1:8000',
});

// Добавляем токен в каждый запрос
API.interceptors.request.use((config) => {
  const token = getToken();
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export default API;
