
import React from 'react';
import CampaignManager from './components/CampaignManager';
import EmailUploader from './components/EmailUploader';
import EmailManager from './components/EmailManager';
import EmailSender from './components/EmailSender';

function App() {
  return (
    <div className="container">
      <header className="header">
        <h1>Email Sender Dashboard</h1>
        <p>Manage campaigns and send bulk emails</p>
      </header>
      
      <div className="grid">
        <CampaignManager />
        <EmailUploader />
      </div>
      
      <EmailManager />
      <EmailSender />
    </div>
  );
}

export default App;
