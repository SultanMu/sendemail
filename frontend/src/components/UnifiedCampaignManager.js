
import React, { useState, useEffect } from 'react';
import { campaignAPI, emailAPI } from '../services/api';

const UnifiedCampaignManager = () => {
  const [step, setStep] = useState(1);
  const [campaignName, setCampaignName] = useState('');
  const [selectedCampaign, setSelectedCampaign] = useState(null);
  const [file, setFile] = useState(null);
  const [emails, setEmails] = useState([]);
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState({ text: '', type: '' });
  const [dragActive, setDragActive] = useState(false);

  const showMessage = (text, type) => {
    setMessage({ text, type });
    setTimeout(() => setMessage({ text: '', type: '' }), 5000);
  };

  const createCampaign = async (e) => {
    e.preventDefault();
    if (!campaignName.trim()) {
      showMessage('Please enter a campaign name', 'error');
      return;
    }

    try {
      setLoading(true);
      const response = await campaignAPI.create({ campaign_name: campaignName });
      setSelectedCampaign(response.data);
      setStep(2);
      showMessage('Campaign created successfully!', 'success');
    } catch (error) {
      showMessage(error.response?.data?.error || 'Error creating campaign', 'error');
    } finally {
      setLoading(false);
    }
  };

  const handleDrag = (e) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === 'dragenter' || e.type === 'dragover') {
      setDragActive(true);
    } else if (e.type === 'dragleave') {
      setDragActive(false);
    }
  };

  const handleDrop = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      setFile(e.dataTransfer.files[0]);
    }
  };

  const uploadEmails = async () => {
    if (!file) {
      showMessage('Please select a file', 'error');
      return;
    }

    try {
      setLoading(true);
      const response = await emailAPI.upload(selectedCampaign.campaign_id, file);
      showMessage('Emails uploaded successfully!', 'success');
      setStep(3);
      loadEmails();
    } catch (error) {
      showMessage(error.response?.data?.error || 'Error uploading emails', 'error');
    } finally {
      setLoading(false);
    }
  };

  const loadEmails = async () => {
    try {
      setLoading(true);
      const response = await emailAPI.list(selectedCampaign.campaign_id);
      setEmails(response.data);
    } catch (error) {
      showMessage('Error loading emails', 'error');
      setEmails([]);
    } finally {
      setLoading(false);
    }
  };

  const deleteEmail = async (emailAddress, campaignId) => {
    try {
      await emailAPI.delete(emailAddress, campaignId);
      showMessage('Email deleted successfully!', 'success');
      loadEmails();
    } catch (error) {
      showMessage(error.response?.data?.error || 'Error deleting email', 'error');
    }
  };

  const resetFlow = () => {
    setStep(1);
    setCampaignName('');
    setSelectedCampaign(null);
    setFile(null);
    setEmails([]);
    setMessage({ text: '', type: '' });
  };

  return (
    <div style={styles.container}>
      {/* Progress Bar */}
      <div style={styles.progressContainer}>
        <div style={styles.progressBar}>
          {[1, 2, 3].map(num => (
            <div key={num} style={{
              ...styles.progressStep,
              ...(step >= num ? styles.progressStepActive : {}),
              ...(step === num ? styles.progressStepCurrent : {})
            }}>
              <span style={styles.progressNumber}>{num}</span>
              <span style={styles.progressLabel}>
                {num === 1 ? 'Create Campaign' : num === 2 ? 'Upload Emails' : 'Manage Emails'}
              </span>
            </div>
          ))}
        </div>
      </div>

      {/* Message Display */}
      {message.text && (
        <div style={{
          ...styles.alert,
          ...(message.type === 'error' ? styles.alertError : styles.alertSuccess)
        }}>
          {message.text}
        </div>
      )}

      {/* Step 1: Campaign Creation */}
      {step === 1 && (
        <div style={styles.card}>
          <h2 style={styles.cardTitle}>Create New Campaign</h2>
          <form onSubmit={createCampaign} style={styles.form}>
            <div style={styles.inputGroup}>
              <label style={styles.label}>Campaign Name</label>
              <input
                type="text"
                value={campaignName}
                onChange={(e) => setCampaignName(e.target.value)}
                placeholder="Enter a descriptive campaign name"
                style={styles.input}
                disabled={loading}
              />
            </div>
            <button 
              type="submit" 
              style={{...styles.button, ...styles.buttonPrimary}}
              disabled={loading}
            >
              {loading ? 'Creating...' : 'Create Campaign & Continue'}
            </button>
          </form>
        </div>
      )}

      {/* Step 2: File Upload */}
      {step === 2 && selectedCampaign && (
        <div style={styles.card}>
          <h2 style={styles.cardTitle}>Upload Email List</h2>
          <p style={styles.campaignInfo}>
            Campaign: <strong>{selectedCampaign.campaign_name}</strong> (ID: {selectedCampaign.campaign_id})
          </p>
          
          <div
            style={{
              ...styles.dropZone,
              ...(dragActive ? styles.dropZoneActive : {}),
              ...(file ? styles.dropZoneWithFile : {})
            }}
            onDragEnter={handleDrag}
            onDragLeave={handleDrag}
            onDragOver={handleDrag}
            onDrop={handleDrop}
            onClick={() => document.getElementById('fileInput').click()}
          >
            <input
              id="fileInput"
              type="file"
              accept=".xls,.xlsx,.csv"
              onChange={(e) => setFile(e.target.files[0])}
              style={styles.hiddenInput}
            />
            
            {file ? (
              <div style={styles.fileSelected}>
                <div style={styles.fileIcon}>📄</div>
                <div>
                  <div style={styles.fileName}>{file.name}</div>
                  <div style={styles.fileSize}>{(file.size / 1024).toFixed(1)} KB</div>
                </div>
              </div>
            ) : (
              <div style={styles.dropZoneContent}>
                <div style={styles.uploadIcon}>📁</div>
                <div style={styles.uploadText}>
                  <strong>Click to upload</strong> or drag and drop
                </div>
                <div style={styles.uploadSubtext}>
                  Excel files (.xls, .xlsx) or CSV files
                </div>
              </div>
            )}
          </div>

          <div style={styles.buttonGroup}>
            <button 
              onClick={resetFlow} 
              style={{...styles.button, ...styles.buttonSecondary}}
            >
              Back
            </button>
            <button 
              onClick={uploadEmails}
              style={{...styles.button, ...styles.buttonPrimary}}
              disabled={!file || loading}
            >
              {loading ? 'Uploading...' : 'Upload & Continue'}
            </button>
          </div>
        </div>
      )}

      {/* Step 3: Email Management */}
      {step === 3 && selectedCampaign && (
        <div style={styles.card}>
          <div style={styles.emailHeader}>
            <div>
              <h2 style={styles.cardTitle}>Email List</h2>
              <p style={styles.campaignInfo}>
                Campaign: <strong>{selectedCampaign.campaign_name}</strong> ({emails.length} emails)
              </p>
            </div>
            <div style={styles.buttonGroup}>
              <button 
                onClick={() => setStep(2)} 
                style={{...styles.button, ...styles.buttonSecondary}}
              >
                Add More Emails
              </button>
              <button 
                onClick={resetFlow} 
                style={{...styles.button, ...styles.buttonOutline}}
              >
                New Campaign
              </button>
            </div>
          </div>

          {loading && <div style={styles.loading}>Loading emails...</div>}
          
          {!loading && emails.length === 0 && (
            <div style={styles.emptyState}>
              <div style={styles.emptyIcon}>📧</div>
              <div style={styles.emptyText}>No emails found</div>
              <div style={styles.emptySubtext}>Upload an Excel file to get started</div>
            </div>
          )}

          {emails.length > 0 && (
            <div style={styles.emailList}>
              {emails.map(email => (
                <div key={`${email.email_id}-${email.campaign_id}`} style={styles.emailCard}>
                  <div style={styles.emailInfo}>
                    <div style={styles.emailName}>{email.name || 'No name'}</div>
                    <div style={styles.emailAddress}>{email.email_address}</div>
                    <div style={styles.emailDate}>
                      Added: {new Date(email.added_at).toLocaleDateString()}
                    </div>
                  </div>
                  <button 
                    onClick={() => deleteEmail(email.email_address, email.campaign_id)}
                    style={{...styles.button, ...styles.buttonDanger}}
                  >
                    Delete
                  </button>
                </div>
              ))}
            </div>
          )}
        </div>
      )}
    </div>
  );
};

const styles = {
  container: {
    maxWidth: '800px',
    margin: '0 auto',
    padding: '20px',
    fontFamily: 'system-ui, -apple-system, sans-serif'
  },
  progressContainer: {
    marginBottom: '30px'
  },
  progressBar: {
    display: 'flex',
    justifyContent: 'space-between',
    position: 'relative'
  },
  progressStep: {
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
    flex: 1,
    position: 'relative'
  },
  progressStepActive: {
    color: '#10b981'
  },
  progressStepCurrent: {
    color: '#3b82f6'
  },
  progressNumber: {
    width: '40px',
    height: '40px',
    borderRadius: '50%',
    backgroundColor: '#e5e7eb',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    fontWeight: 'bold',
    marginBottom: '8px',
    color: '#374151'
  },
  progressLabel: {
    fontSize: '14px',
    textAlign: 'center'
  },
  card: {
    backgroundColor: 'white',
    borderRadius: '12px',
    padding: '30px',
    boxShadow: '0 4px 6px -1px rgba(0, 0, 0, 0.1)',
    border: '1px solid #e5e7eb'
  },
  cardTitle: {
    fontSize: '24px',
    fontWeight: 'bold',
    marginBottom: '8px',
    color: '#111827'
  },
  campaignInfo: {
    color: '#6b7280',
    marginBottom: '20px'
  },
  form: {
    display: 'flex',
    flexDirection: 'column',
    gap: '20px'
  },
  inputGroup: {
    display: 'flex',
    flexDirection: 'column',
    gap: '8px'
  },
  label: {
    fontSize: '14px',
    fontWeight: '500',
    color: '#374151'
  },
  input: {
    padding: '12px 16px',
    border: '1px solid #d1d5db',
    borderRadius: '8px',
    fontSize: '16px',
    outline: 'none',
    transition: 'border-color 0.2s',
    ':focus': {
      borderColor: '#3b82f6'
    }
  },
  button: {
    padding: '12px 24px',
    borderRadius: '8px',
    fontSize: '14px',
    fontWeight: '500',
    border: 'none',
    cursor: 'pointer',
    transition: 'all 0.2s',
    outline: 'none'
  },
  buttonPrimary: {
    backgroundColor: '#3b82f6',
    color: 'white'
  },
  buttonSecondary: {
    backgroundColor: '#6b7280',
    color: 'white'
  },
  buttonOutline: {
    backgroundColor: 'transparent',
    color: '#6b7280',
    border: '1px solid #d1d5db'
  },
  buttonDanger: {
    backgroundColor: '#ef4444',
    color: 'white',
    padding: '8px 16px',
    fontSize: '12px'
  },
  buttonGroup: {
    display: 'flex',
    gap: '12px'
  },
  dropZone: {
    border: '2px dashed #d1d5db',
    borderRadius: '12px',
    padding: '40px 20px',
    textAlign: 'center',
    cursor: 'pointer',
    transition: 'all 0.2s',
    marginBottom: '20px'
  },
  dropZoneActive: {
    borderColor: '#3b82f6',
    backgroundColor: '#eff6ff'
  },
  dropZoneWithFile: {
    borderColor: '#10b981',
    backgroundColor: '#f0fdf4'
  },
  dropZoneContent: {
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
    gap: '12px'
  },
  uploadIcon: {
    fontSize: '48px'
  },
  uploadText: {
    fontSize: '16px',
    color: '#374151'
  },
  uploadSubtext: {
    fontSize: '14px',
    color: '#6b7280'
  },
  fileSelected: {
    display: 'flex',
    alignItems: 'center',
    gap: '16px'
  },
  fileIcon: {
    fontSize: '32px'
  },
  fileName: {
    fontSize: '16px',
    fontWeight: '500',
    color: '#374151'
  },
  fileSize: {
    fontSize: '14px',
    color: '#6b7280'
  },
  hiddenInput: {
    display: 'none'
  },
  alert: {
    padding: '12px 16px',
    borderRadius: '8px',
    marginBottom: '20px',
    fontSize: '14px'
  },
  alertSuccess: {
    backgroundColor: '#d1fae5',
    color: '#065f46',
    border: '1px solid #10b981'
  },
  alertError: {
    backgroundColor: '#fee2e2',
    color: '#991b1b',
    border: '1px solid #ef4444'
  },
  emailHeader: {
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'flex-start',
    marginBottom: '20px'
  },
  loading: {
    textAlign: 'center',
    padding: '40px',
    color: '#6b7280'
  },
  emptyState: {
    textAlign: 'center',
    padding: '60px 20px'
  },
  emptyIcon: {
    fontSize: '64px',
    marginBottom: '16px'
  },
  emptyText: {
    fontSize: '18px',
    fontWeight: '500',
    color: '#374151',
    marginBottom: '8px'
  },
  emptySubtext: {
    fontSize: '14px',
    color: '#6b7280'
  },
  emailList: {
    display: 'flex',
    flexDirection: 'column',
    gap: '12px'
  },
  emailCard: {
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
    padding: '16px',
    border: '1px solid #e5e7eb',
    borderRadius: '8px',
    backgroundColor: '#f9fafb'
  },
  emailInfo: {
    display: 'flex',
    flexDirection: 'column',
    gap: '4px'
  },
  emailName: {
    fontWeight: '500',
    color: '#374151'
  },
  emailAddress: {
    color: '#6b7280',
    fontSize: '14px'
  },
  emailDate: {
    color: '#9ca3af',
    fontSize: '12px'
  }
};

export default UnifiedCampaignManager;
