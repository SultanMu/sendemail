
import axios from 'axios';

// Use relative paths - Django will serve both frontend and API
const API_BASE_URL = '/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  withCredentials: false,
  timeout: 10000
});

// Request interceptor for debugging
api.interceptors.request.use(
  (config) => {
    console.log('Starting Request:', config.url);
    return config;
  },
  (error) => {
    console.log('Request Error:', error);
    return Promise.reject(error);
  }
);

// Response interceptor for debugging  
api.interceptors.response.use(
  (response) => {
    console.log('Response received:', response.config.url, response.status);
    return response;
  },
  (error) => {
    console.log('API Error:', error.response?.data || error.message);
    return Promise.reject(error);
  }
);

export const campaignAPI = {
  list: () => api.get('/campaigns/'),
  create: (data) => api.post('/campaigns/create', data),
  update: (campaignId, campaignName) => api.post(`/update-campaign?campaign_id=${campaignId}&campaign_name=${encodeURIComponent(campaignName)}`),
  delete: (campaignId) => api.post(`/delete-campaign?campaign_id=${campaignId}`),
};

export const emailAPI = {
  uploadXLS: (data) => api.post('/upload-xls/', data),
  getEmails: () => api.get('/list-emails/'),
  sendEmails: (data) => api.post('/send-emails/', data),
  deleteEmail: (data) => api.post('/delete-email', data),
  updateEmail: (data) => api.post('/update-email', data),
};

export const templateAPI = {
  getTemplates: () => api.get('/templates/'),
  createTemplate: (data) => api.post('/templates/create/', data),
  getTemplatePreview: (templateId) => api.get(`/template-preview/?template_id=${templateId}`),
};

export default api;
