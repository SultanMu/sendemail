
import React, { useState } from 'react';
import { emailAPI } from '../services/api';

const EmailManager = () => {
  const [listCampaignId, setListCampaignId] = useState('');
  const [deleteEmailAddress, setDeleteEmailAddress] = useState('');
  const [deleteEmailCampaignId, setDeleteEmailCampaignId] = useState('');
  const [emails, setEmails] = useState([]);
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState({ text: '', type: '' });

  const loadEmails = async () => {
    if (!listCampaignId) {
      showMessage('Please enter a campaign ID', 'error');
      return;
    }

    try {
      setLoading(true);
      const response = await emailAPI.list(listCampaignId);
      setEmails(response.data);
    } catch (error) {
      showMessage(error.response?.data?.error || 'Error loading emails', 'error');
      setEmails([]);
    } finally {
      setLoading(false);
    }
  };

  const deleteEmail = async () => {
    if (!deleteEmailAddress || !deleteEmailCampaignId) {
      showMessage('Please enter both email address and campaign ID', 'error');
      return;
    }

    await deleteEmailById(deleteEmailAddress, deleteEmailCampaignId);
  };

  const deleteEmailById = async (emailAddress, campaignId) => {
    try {
      await emailAPI.delete(emailAddress, campaignId);
      showMessage('Email deleted successfully!', 'success');
      setDeleteEmailAddress('');
      setDeleteEmailCampaignId('');
      
      // Refresh email list if campaign ID matches
      if (listCampaignId == campaignId) {
        loadEmails();
      }
    } catch (error) {
      showMessage(error.response?.data?.error || 'Error deleting email', 'error');
    }
  };

  const showMessage = (text, type) => {
    setMessage({ text, type });
    setTimeout(() => setMessage({ text: '', type: '' }), 5000);
  };

  return (
    <div className="section">
      <h2>Email Management</h2>
      
      <div className="grid">
        <div>
          <h3>List Emails</h3>
          <div className="form-group">
            <label htmlFor="listCampaignId">Campaign ID:</label>
            <input
              type="number"
              id="listCampaignId"
              className="form-control"
              value={listCampaignId}
              onChange={(e) => setListCampaignId(e.target.value)}
              placeholder="Enter campaign ID"
            />
          </div>
          <button className="btn" onClick={loadEmails} disabled={loading}>
            {loading ? 'Loading...' : 'Load Emails'}
          </button>
        </div>
        
        <div>
          <h3>Delete Email</h3>
          <div className="form-group">
            <label htmlFor="deleteEmailAddress">Email Address:</label>
            <input
              type="text"
              id="deleteEmailAddress"
              className="form-control"
              value={deleteEmailAddress}
              onChange={(e) => setDeleteEmailAddress(e.target.value)}
              placeholder="Enter email address"
            />
          </div>
          <div className="form-group">
            <label htmlFor="deleteEmailCampaignId">Campaign ID:</label>
            <input
              type="number"
              id="deleteEmailCampaignId"
              className="form-control"
              value={deleteEmailCampaignId}
              onChange={(e) => setDeleteEmailCampaignId(e.target.value)}
              placeholder="Enter campaign ID"
            />
          </div>
          <button className="btn btn-danger" onClick={deleteEmail}>
            Delete Email
          </button>
        </div>
      </div>

      {message.text && (
        <div className={`alert ${message.type === 'error' ? 'alert-error' : 'alert-success'}`}>
          {message.text}
        </div>
      )}

      <div className="emails-list">
        {loading && <div className="loading">Loading emails...</div>}
        {!loading && emails.length === 0 && listCampaignId && <p>No emails found for this campaign.</p>}
        {emails.length > 0 && (
          <>
            <h3>Emails ({emails.length} found)</h3>
            {emails.map(email => (
              <div key={`${email.email_id}-${email.campaign_id}`} className="item-card">
                <h4>{email.name || 'No name'}</h4>
                <p><strong>Email:</strong> {email.email_address}</p>
                <p><strong>Added:</strong> {new Date(email.added_at).toLocaleDateString()}</p>
                <div className="item-actions">
                  <button 
                    className="btn btn-danger" 
                    onClick={() => deleteEmailById(email.email_address, email.campaign_id)}
                  >
                    Delete
                  </button>
                </div>
              </div>
            ))}
          </>
        )}
      </div>
    </div>
  );
};

export default EmailManager;
