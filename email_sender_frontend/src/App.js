import React, { useState, useEffect } from 'react';
import UnifiedCampaignManager from './components/UnifiedCampaignManager';
import EmailSender from './components/EmailSender';
import EmailTemplateBuilder from './components/EmailTemplateBuilder';
import EmailTemplateEditor from './components/EmailTemplateEditor';
import { campaignAPI, templateAPI } from './services/api';
import Tabs from './components/Tabs';

function App() {
  const [campaigns, setCampaigns] = useState([]);
  const [templates, setTemplates] = useState([]);

  const fetchCampaigns = async () => {
    try {
      const response = await campaignAPI.list();
      setCampaigns(response.data);
    } catch (error) {
      console.error('Error fetching campaigns:', error);
    }
  };

  const fetchTemplates = async () => {
    try {
      const response = await templateAPI.list();
      setTemplates(response.data);
    } catch (error) {
      console.error('Error fetching templates:', error);
    }
  };

  useEffect(() => {
    fetchCampaigns();
    fetchTemplates();
  }, []);

  return (
    <div style={styles.app}>
      <header style={styles.header}>
        <h1 style={styles.title}>Email Campaign Manager</h1>
        <p style={styles.subtitle}>Modern unified campaign management and email sending</p>
      </header>

      <Tabs>
        <div label="Campaign Management">
          <UnifiedCampaignManager 
            campaigns={campaigns}
            refreshCampaigns={fetchCampaigns} 
          />
        </div>
        <div label="Send Email">
          <EmailSender 
            campaigns={campaigns} 
            templates={templates}
          />
        </div>
        <div label="Create Template">
          <EmailTemplateBuilder refreshTemplates={fetchTemplates} />
        </div>
        <div label="Edit Email Template">
          <EmailTemplateEditor 
            templates={templates} 
            refreshTemplates={fetchTemplates}
          />
        </div>
      </Tabs>
    </div>
  );
}

const styles = {
  app: {
    minHeight: '100vh',
    backgroundColor: '#f9fafb',
    fontFamily: 'system-ui, -apple-system, sans-serif'
  },
  header: {
    backgroundColor: 'white',
    borderBottom: '1px solid #e5e7eb',
    padding: '24px 0',
    marginBottom: '24px'
  },
  title: {
    fontSize: '32px',
    fontWeight: 'bold',
    color: '#111827',
    margin: '0 auto',
    textAlign: 'center',
    marginBottom: '8px'
  },
  subtitle: {
    fontSize: '16px',
    color: '#6b7280',
    margin: '0 auto',
    textAlign: 'center'
  }
};

export default App;
