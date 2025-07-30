import axios from 'axios';

// Use relative /api path that will be handled by Django
const API_BASE_URL = process.env.REACT_APP_API_URL || '/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add request interceptor for debugging
api.interceptors.request.use(request => {
  console.log('Starting Request:', request.url);
  return request;
});

// Add response interceptor for error handling
api.interceptors.response.use(
  response => response,
  error => {
    console.error('API Error:', error.response?.data || error.message);
    return Promise.reject(error);
  }
);

export const campaignAPI = {
  list: () => api.get('/campaigns/'),
  create: (data) => api.post('/campaigns/create', data),
  update: (campaignId, campaignName) => 
    api.post(`/update-campaign?campaign_id=${campaignId}&campaign_name=${encodeURIComponent(campaignName)}`),
  delete: (campaignId) => 
    api.post(`/delete-campaign?campaign_id=${campaignId}`),
  getEmails: (campaignId) => 
    api.get(`/list-emails/?campaign_id=${campaignId}`),
};

export const emailAPI = {
  list: (campaignId) => 
    api.get(`/list-emails/?campaign_id=${campaignId}`),
  upload: (campaignId, file) => {
    const formData = new FormData();
    formData.append('file', file);
    return api.post(`/upload-xls/?campaign_id=${campaignId}`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
  },
  delete: (emailAddress, campaignId) => 
    api.post(`/delete-email?email_add=${encodeURIComponent(emailAddress)}&campaign_id=${campaignId}`),
  send: (campaignId, emailTemplate, customMessage) => {
    const url = `/send-emails/?campaign_id=${campaignId}&email_template=${emailTemplate}`;
    return api.post(url, { message: customMessage });
  },
  getTemplatePreview: (templateId) => {
    return api.get(`/template-preview/?template_id=${templateId}`);
  }
};

// Template API
export const templateAPI = {
  list: () => api.get('/templates/'),
  create: (templateData) => api.post('/templates/create/', templateData),
};

export default api;