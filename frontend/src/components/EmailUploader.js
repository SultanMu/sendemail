
import React, { useState } from 'react';
import { emailAPI } from '../services/api';

const EmailUploader = () => {
  const [campaignId, setCampaignId] = useState('');
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState({ text: '', type: '' });

  const uploadEmails = async (e) => {
    e.preventDefault();
    
    if (!campaignId) {
      showMessage('Please enter a campaign ID', 'error');
      return;
    }
    
    if (!file) {
      showMessage('Please select a file', 'error');
      return;
    }

    try {
      setLoading(true);
      const response = await emailAPI.upload(campaignId, file);
      showMessage(
        response.data.message + 
        (response.data['duplicate email count'] ? ` (${response.data['duplicate email count']} duplicates found)` : ''), 
        'success'
      );
      setCampaignId('');
      setFile(null);
      // Reset file input
      document.getElementById('excelFile').value = '';
    } catch (error) {
      showMessage(error.response?.data?.error || 'Error uploading emails', 'error');
    } finally {
      setLoading(false);
    }
  };

  const showMessage = (text, type) => {
    setMessage({ text, type });
    setTimeout(() => setMessage({ text: '', type: '' }), 5000);
  };

  return (
    <div className="section">
      <h2>Upload Emails</h2>
      
      <form onSubmit={uploadEmails}>
        <div className="form-group">
          <label htmlFor="uploadCampaignId">Campaign ID:</label>
          <input
            type="number"
            id="uploadCampaignId"
            className="form-control"
            value={campaignId}
            onChange={(e) => setCampaignId(e.target.value)}
            placeholder="Enter campaign ID"
            disabled={loading}
          />
        </div>
        
        <div className="form-group">
          <label htmlFor="excelFile">Excel File:</label>
          <input
            type="file"
            id="excelFile"
            className="form-control"
            accept=".xls,.xlsx,.csv"
            onChange={(e) => setFile(e.target.files[0])}
            disabled={loading}
          />
        </div>
        
        <button type="submit" className="btn" disabled={loading}>
          {loading ? 'Uploading...' : 'Upload Emails'}
        </button>
      </form>

      {message.text && (
        <div className={`alert ${message.type === 'error' ? 'alert-error' : 'alert-success'}`}>
          {message.text}
        </div>
      )}
    </div>
  );
};

export default EmailUploader;
