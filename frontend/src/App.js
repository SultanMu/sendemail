
import React from 'react';
import UnifiedCampaignManager from './components/UnifiedCampaignManager';
import EmailSender from './components/EmailSender';

function App() {
  return (
    <div className="container">
      <header className="header">
        <h1>Email Sender Dashboard</h1>
        <p>Manage campaigns and send bulk emails</p>
      </header>
      
      <UnifiedCampaignManager />
      <EmailSender />
    </div>
  );
}

export default App;
