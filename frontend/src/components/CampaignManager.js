
import React, { useState, useEffect, useCallback } from 'react';
import { campaignAPI } from '../services/api';

const CampaignManager = () => {
  const [campaigns, setCampaigns] = useState([]);
  const [campaignName, setCampaignName] = useState('');
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState({ text: '', type: '' });

  const loadCampaigns = useCallback(async () => {
    try {
      setLoading(true);
      const response = await campaignAPI.list();
      setCampaigns(response.data);
    } catch (error) {
      showMessage('Error loading campaigns: ' + error.message, 'error');
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    loadCampaigns();
  }, [loadCampaigns]);

  const createCampaign = async (e) => {
    e.preventDefault();
    if (!campaignName.trim()) {
      showMessage('Please enter a campaign name', 'error');
      return;
    }

    try {
      setLoading(true);
      const response = await campaignAPI.create({ campaign_name: campaignName });
      showMessage(`Campaign created successfully! ID: ${response.data.campaign_id}`, 'success');
      setCampaignName('');
      loadCampaigns();
    } catch (error) {
      showMessage(error.response?.data?.error || 'Error creating campaign', 'error');
    } finally {
      setLoading(false);
    }
  };

  const updateCampaign = async (campaignId, currentName) => {
    const newName = prompt('Enter new campaign name:', currentName);
    if (!newName || newName === currentName) return;

    try {
      await campaignAPI.update(campaignId, newName);
      showMessage('Campaign updated successfully!', 'success');
      loadCampaigns();
    } catch (error) {
      showMessage(error.response?.data?.error || 'Error updating campaign', 'error');
    }
  };

  const deleteCampaign = async (campaignId) => {
    if (!window.confirm('Are you sure you want to delete this campaign and all its emails?')) return;

    try {
      await campaignAPI.delete(campaignId);
      showMessage('Campaign deleted successfully!', 'success');
      loadCampaigns();
    } catch (error) {
      showMessage(error.response?.data?.error || 'Error deleting campaign', 'error');
    }
  };

  const showMessage = (text, type) => {
    setMessage({ text, type });
    setTimeout(() => setMessage({ text: '', type: '' }), 5000);
  };

  return (
    <div className="section">
      <h2>Campaign Management</h2>
      
      <form onSubmit={createCampaign}>
        <div className="form-group">
          <label htmlFor="campaignName">Campaign Name:</label>
          <input
            type="text"
            id="campaignName"
            className="form-control"
            value={campaignName}
            onChange={(e) => setCampaignName(e.target.value)}
            placeholder="Enter campaign name"
            disabled={loading}
          />
        </div>
        
        <button type="submit" className="btn" disabled={loading}>
          {loading ? 'Creating...' : 'Create Campaign'}
        </button>
        <button type="button" className="btn" onClick={loadCampaigns} disabled={loading}>
          {loading ? 'Loading...' : 'Refresh Campaigns'}
        </button>
      </form>

      {message.text && (
        <div className={`alert ${message.type === 'error' ? 'alert-error' : 'alert-success'}`}>
          {message.text}
        </div>
      )}

      <div className="campaigns-list">
        {loading && <div className="loading">Loading campaigns...</div>}
        {!loading && campaigns.length === 0 && <p>No campaigns found.</p>}
        {campaigns.map(campaign => (
          <div key={campaign.campaign_id} className="item-card">
            <h4>{campaign.campaign_name}</h4>
            <p><strong>ID:</strong> {campaign.campaign_id}</p>
            <p><strong>Created:</strong> {new Date(campaign.created_at).toLocaleDateString()}</p>
            <div className="item-actions">
              <button 
                className="btn" 
                onClick={() => updateCampaign(campaign.campaign_id, campaign.campaign_name)}
              >
                Update
              </button>
              <button 
                className="btn btn-danger" 
                onClick={() => deleteCampaign(campaign.campaign_id)}
              >
                Delete
              </button>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default CampaignManager;
