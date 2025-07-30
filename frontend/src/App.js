
import React from 'react';
import UnifiedCampaignManager from './components/UnifiedCampaignManager';
import EmailSender from './components/EmailSender';

function App() {
  return (
    <div style={styles.app}>
      <header style={styles.header}>
        <h1 style={styles.title}>Email Campaign Manager</h1>
        <p style={styles.subtitle}>Modern unified campaign management and email sending</p>
      </header>
      
      <UnifiedCampaignManager />
      <EmailSender />
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
