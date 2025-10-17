import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000/api';

export const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const dashboardAPI = {
  getMetrics: () => api.get('/dashboard/metrics'),
};

export const campaignsAPI = {
  getAll: () => api.get('/campaigns'),
  getRecent: () => api.get('/campaigns/recent'),
  getById: (id) => api.get(`/campaigns/${id}`),
  generate: (data) => api.post('/campaigns/generate', data),
};

export const marketIntelligenceAPI = {
  getAll: () => api.get('/market-intelligence'),
  getRecent: () => api.get('/market-intelligence/recent'),
};

export const servicesAPI = {
  getAll: () => api.get('/services'),
  getById: (id) => api.get(`/services/${id}`),
};
