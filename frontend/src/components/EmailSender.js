import React, { useState, useEffect } from 'react';
import { emailAPI, campaignAPI, templateAPI } from '../services/api';

const EmailSender = () => {
  const [campaigns, setCampaigns] = useState([]);
  const [templates, setTemplates] = useState([]);
  const [campaignId, setCampaignId] = useState('');
  const [emailTemplate, setEmailTemplate] = useState('1');
  const [customMessage, setCustomMessage] = useState('');
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState({ text: '', type: '' });
  const [templatePreview, setTemplatePreview] = useState(null);
  const [loadingPreview, setLoadingPreview] = useState(false);
  const [previewError, setPreviewError] = useState(null);

  const fetchTemplates = async () => {
    try {
      const response = await templateAPI.list();
      setTemplates(response.data);
    } catch (error) {
      console.error('Error fetching templates:', error);
      showMessage('Error fetching templates', 'error');
    }
  };

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
    fetchTemplates();
    loadTemplatePreview(emailTemplate); // Load initial template

    // Listen for custom events when new templates are created
    const handleTemplateCreated = () => {
      fetchTemplates();
    };

    window.addEventListener('templateCreated', handleTemplateCreated);

    return () => {
      window.removeEventListener('templateCreated', handleTemplateCreated);
    };
  }, []);

  useEffect(() => {
    loadTemplatePreview(emailTemplate);
  }, [emailTemplate]);

  // Expose refresh function globally for other components to use
  useEffect(() => {
    window.refreshTemplates = fetchTemplates;
    return () => {
      delete window.refreshTemplates;
    };
  }, []);

  const loadTemplatePreview = async (templateId) => {
    try {
      setLoadingPreview(true);
      setPreviewError(null);
      const response = await emailAPI.getTemplatePreview(templateId);
      setTemplatePreview(response.data);
    } catch (error) {
      console.error('Error loading template preview:', error);
      setTemplatePreview(null);
      setPreviewError('Failed to load template preview');
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
            {templates.map((template, index) => (
              <option key={`${template.template_id}-${template.type}-${index}`} value={template.template_id}>
                {template.template_name} {template.type === 'custom' && '(Custom)'}
              </option>
            ))}
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
      <div style={{ marginTop: '30px' }}>
        <h3 style={{ marginBottom: '15px', color: '#333' }}>Email Template Preview</h3>

        {loadingPreview && (
          <div style={{ 
            padding: '20px', 
            textAlign: 'center', 
            backgroundColor: '#f8f9fa',
            borderRadius: '8px',
            border: '1px solid #ddd'
          }}>
            <div style={{ fontSize: '16px', color: '#666' }}>Loading template preview...</div>
          </div>
        )}

        {templatePreview && !loadingPreview && (
          <div style={{ 
            border: '1px solid #ddd', 
            borderRadius: '8px', 
            overflow: 'hidden',
            boxShadow: '0 2px 8px rgba(0,0,0,0.1)'
          }}>
            <div style={{ 
              padding: '15px', 
              backgroundColor: '#f8f9fa', 
              borderBottom: '1px solid #ddd'
            }}>
              <h4 style={{ margin: '0 0 5px 0', fontSize: '18px', color: '#333' }}>
                {templatePreview.template_name}
              </h4>
              <p style={{ margin: '0', fontSize: '14px', color: '#666' }}>
                <strong>Subject:</strong> {templatePreview.subject}
              </p>
            </div>
            <div style={{ 
              height: '500px', 
              overflow: 'auto',
              backgroundColor: '#fff',
              border: '1px solid #eee'
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

        {previewError && !loadingPreview && (
          <div style={{ 
            padding: '20px', 
            textAlign: 'center', 
            backgroundColor: '#fef2f2',
            borderRadius: '8px',
            border: '1px solid #fecaca'
          }}>
            <div style={{ fontSize: '16px', color: '#dc2626' }}>
              {previewError}
            </div>
          </div>
        )}

        {!templatePreview && !loadingPreview && !previewError && (
          <div style={{ 
            padding: '20px', 
            textAlign: 'center', 
            backgroundColor: '#f8f9fa',
            borderRadius: '8px',
            border: '1px solid #ddd'
          }}>
            <div style={{ fontSize: '16px', color: '#666' }}>
              Select a template above to see the preview
            </div>
          </div>
        )}
      </div>

      {message.text && (
        <div className={`alert ${message.type === 'error' ? 'alert-error' : 'alert-success'}`}>
          {message.text}
        </div>
      )}
    </div>
  );
};

export default EmailSender;