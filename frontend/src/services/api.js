
import axios from 'axios';

const API_BASE = '/email';

const api = axios.create({
  baseURL: API_BASE,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const campaignAPI = {
  list: () => api.get('/campaigns/'),
  create: (data) => api.post('/campaigns/create', data),
  update: (campaignId, campaignName) => 
    api.post(`/update-campaign?campaign_id=${campaignId}&campaign_name=${encodeURIComponent(campaignName)}`),
  delete: (campaignId) => 
    api.post(`/delete-campaign?campaign_id=${campaignId}`),
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
  send: (campaignId, emailTemplate, message) => 
    api.post(`/send-emails/?campaign_id=${campaignId}&email_template=${emailTemplate}`, 
      message ? { message } : {}),
};

export default api;
