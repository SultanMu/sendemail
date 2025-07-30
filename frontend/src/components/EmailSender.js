import React, { useState, useEffect } from 'react';
import { emailAPI, campaignAPI } from '../services/api';

const EmailSender = () => {
  const [campaigns, setCampaigns] = useState([]);
  const [campaignId, setCampaignId] = useState('');
  const [emailTemplate, setEmailTemplate] = useState('1');
  const [customMessage, setCustomMessage] = useState('');
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState({ text: '', type: '' });
  const [templatePreview, setTemplatePreview] = useState(null);
  const [loadingPreview, setLoadingPreview] = useState(false);

  useEffect(() => {
    const fetchCampaigns = async () => {
      try {
        const response = await campaignAPI.list();
        setCampaigns(response.data);
      } catch (error) {
        console.error('Error fetching campaigns:', error);
        showMessage('Error fetching campaigns', 'error');
      }
    };

    fetchCampaigns();
    loadTemplatePreview(emailTemplate); // Load initial template
  }, []);

  useEffect(() => {
    loadTemplatePreview(emailTemplate);
  }, [emailTemplate]);

  const loadTemplatePreview = async (templateId) => {
    try {
      setLoadingPreview(true);
      const response = await emailAPI.getTemplatePreview(templateId);
      setTemplatePreview(response.data);
    } catch (error) {
      console.error('Error loading template preview:', error);
      setTemplatePreview(null);
    } finally {
      setLoadingPreview(false);
    }
  };

  const sendEmails = async (e) => {
    e.preventDefault();

    if (!campaignId) {
      showMessage('Please select a campaign', 'error');
      return;
    }

    try {
      setLoading(true);
      const response = await emailAPI.send(campaignId, emailTemplate, customMessage);
      showMessage(
        `${response.data.message} - Sent: ${response.data.details.sent}, Failed: ${response.data.details.failed}`,
        'success'
      );
    } catch (error) {
      showMessage(error.response?.data?.error || 'Error sending emails', 'error');
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
      <h2>Send Emails</h2>

      <form onSubmit={sendEmails}>
        <div className="form-group">
          <label htmlFor="sendCampaignId">Select Campaign:</label>
          <select
            id="sendCampaignId"
            className="form-control"
            value={campaignId}
            onChange={(e) => setCampaignId(e.target.value)}
            disabled={loading}
          >
            <option value="">Select a campaign</option>
            {campaigns.map((campaign) => (
              <option key={campaign.campaign_id} value={campaign.campaign_id}>
                    {campaign.campaign_name}
                  </option>
            ))}
          </select>
        </div>

        <div className="form-group">
          <label htmlFor="emailTemplate">Email Template:</label>
          <select
            id="emailTemplate"
            className="form-control"
            value={emailTemplate}
            onChange={(e) => setEmailTemplate(e.target.value)}
            disabled={loading}
          >
            <option value="1">AutoSAD v1</option>
            <option value="2">XCV AI</option>
            <option value="3">AutoSAD v2</option>
            <option value="4">AutoSAD v3</option>
          </select>
        </div>

        <div className="form-group">
          <label htmlFor="customMessage">Custom Message (optional):</label>
          <textarea
            id="customMessage"
            className="form-control"
            rows="4"
            value={customMessage}
            onChange={(e) => setCustomMessage(e.target.value)}
            placeholder="Enter custom message or leave blank for default"
            disabled={loading}
          />
        </div>

        <button type="submit" className="btn btn-success" disabled={loading}>
          {loading ? 'Sending...' : 'Send Emails'}
        </button>
      </form>

      {/* Template Preview Section */}
      {templatePreview && (
        <div style={{ marginTop: '30px', border: '1px solid #ddd', borderRadius: '8px', overflow: 'hidden' }}>
          <div style={{ 
            padding: '15px', 
            backgroundColor: '#f8f9fa', 
            borderBottom: '1px solid #ddd',
            display: 'flex',
            justifyContent: 'space-between',
            alignItems: 'center'
          }}>
            <div>
              <h3 style={{ margin: '0 0 5px 0', fontSize: '18px', color: '#333' }}>
                Email Preview: {templatePreview.template_name}
              </h3>
              <p style={{ margin: '0', fontSize: '14px', color: '#666' }}>
                Subject: {templatePreview.subject}
              </p>
            </div>
            {loadingPreview && (
              <div style={{ fontSize: '14px', color: '#666' }}>Loading...</div>
            )}
          </div>
          <div style={{ 
            height: '400px', 
            overflow: 'auto',
            backgroundColor: '#fff'
          }}>
            <iframe
              srcDoc={templatePreview.html_content}
              style={{
                width: '100%',
                height: '100%',
                border: 'none',
                display: 'block'
              }}
              title="Email Template Preview"
            />
          </div>
        </div>
      )}

      {message.text && (
        <div className={`alert ${message.type === 'error' ? 'alert-error' : 'alert-success'}`}>
          {message.text}
        </div>
      )}
    </div>
  );
};

export default EmailSender;