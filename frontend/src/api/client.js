import axios from 'axios';

const API_BASE_URL = '/api';

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
  getAll: (params) => api.get('/campaigns', { params }),
  getRecent: () => api.get('/campaigns/recent'),
  getById: (id) => api.get(`/campaigns/${id}`),
  generate: (data) => api.post('/campaigns/generate', data),
  update: (id, data) => api.patch(`/campaigns/${id}`, data),
  delete: (id) => api.delete(`/campaigns/${id}`),
  regenerateIdeas: (id) => api.patch(`/campaigns/${id}/regenerate-ideas`),
  regenerateStrategies: (id) => api.patch(`/campaigns/${id}/regenerate-strategies`),
  submitFeedback: (id, data) => api.post(`/campaigns/${id}/feedback`, data),
};

export const marketIntelligenceAPI = {
  getAll: () => api.get('/market-intelligence'),
  getRecent: () => api.get('/market-intelligence/recent'),
};

export const servicesAPI = {
  getAll: () => api.get('/services'),
  getById: (id) => api.get(`/services/${id}`),
};
