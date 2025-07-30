import React, { useState, useEffect } from 'react';
import { emailAPI, campaignAPI } from '../services/api';

const EmailSender = () => {
  const [campaigns, setCampaigns] = useState([]);
  const [campaignId, setCampaignId] = useState('');
  const [emailTemplate, setEmailTemplate] = useState('1');
  const [customMessage, setCustomMessage] = useState('');
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState({ text: '', type: '' });

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
  }, []);

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

      {message.text && (
        <div className={`alert ${message.type === 'error' ? 'alert-error' : 'alert-success'}`}>
          {message.text}
        </div>
      )}
    </div>
  );
};

export default EmailSender;