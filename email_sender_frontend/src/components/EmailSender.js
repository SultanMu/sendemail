import React, { useState, useEffect } from 'react';
import { emailAPI, campaignAPI } from '../services/api';

const FinalEmailPreview = ({ templatePreview, customMessage, campaignId, campaigns }) => {
  const [campaignEmails, setCampaignEmails] = useState([]);
  const [loadingEmails, setLoadingEmails] = useState(false);

  useEffect(() => {
    const fetchCampaignEmails = async () => {
      if (!campaignId) return;
      
      try {
        setLoadingEmails(true);
        const response = await campaignAPI.getEmails(campaignId);
        setCampaignEmails(response.data);
      } catch (error) {
        console.error('Error fetching campaign emails:', error);
        setCampaignEmails([]);
      } finally {
        setLoadingEmails(false);
      }
    };

    fetchCampaignEmails();
  }, [campaignId]);

  const selectedCampaign = campaigns.find(c => c.campaign_id.toString() === campaignId);
  const sampleRecipient = campaignEmails.length > 0 ? campaignEmails[0] : null;
  const recipientEmail = sampleRecipient?.email || 'sample@example.com';
  const recipientName = sampleRecipient?.name || 'Sample Recipient';

  const defaultMessage = "Thank you for applying to the AUTOSAD Get Certified program. We're thrilled to have you on board and look forward to helping you gain the knowledge and credentials to excel in the AUTOSAD ecosystem. To finalize your enrollment and start your certification journey, simply click the link below to complete your registration process.";
  const finalMessage = customMessage || defaultMessage;

  return (
    <div style={{ marginTop: '20px', marginBottom: '20px' }}>
      <h3 style={{ marginBottom: '15px', color: '#333' }}>📧 Final Email Preview (What Will Be Sent)</h3>
      
      {/* Message Status Indicator */}
      <div style={{
        padding: '12px',
        marginBottom: '15px',
        backgroundColor: customMessage ? '#d4edda' : '#fff3cd',
        border: `1px solid ${customMessage ? '#c3e6cb' : '#ffeaa7'}`,
        borderRadius: '8px',
        fontSize: '14px'
      }}>
        {customMessage ? (
          <div>
            <strong style={{ color: '#155724' }}>✅ Custom Message Active:</strong>
            <div style={{ 
              marginTop: '8px', 
              padding: '8px', 
              backgroundColor: 'white', 
              borderRadius: '4px',
              fontStyle: 'italic',
              border: '1px solid #c3e6cb'
            }}>
              "{customMessage}"
            </div>
          </div>
        ) : (
          <div>
            <strong style={{ color: '#856404' }}>ℹ️ Using Default Message</strong>
            <div style={{ marginTop: '4px', color: '#856404' }}>
              Add a custom message above to personalize your emails
            </div>
          </div>
        )}
      </div>
      <div style={{ 
        border: '2px solid #28a745', 
        borderRadius: '8px', 
        overflow: 'hidden',
        boxShadow: '0 4px 12px rgba(40, 167, 69, 0.2)'
      }}>
        {/* Email Header */}
        <div style={{ 
          padding: '15px', 
          backgroundColor: '#f8f9fa',
          borderBottom: '1px solid #dee2e6',
          fontSize: '14px',
          fontFamily: 'monospace'
        }}>
          <div style={{ marginBottom: '8px' }}>
            <strong>From:</strong> info@autosad.ai
          </div>
          <div style={{ marginBottom: '8px' }}>
            <strong>To:</strong> {recipientEmail}
          </div>
          <div style={{ marginBottom: '8px' }}>
            <strong>Campaign:</strong> {selectedCampaign?.campaign_name || 'Selected Campaign'}
          </div>
          <div>
            <strong>Subject:</strong> {templatePreview.subject}
          </div>
        </div>
        
        {/* Campaign Info */}
        <div style={{ 
          padding: '15px', 
          backgroundColor: '#28a745', 
          color: 'white'
        }}>
          <h4 style={{ margin: '0 0 5px 0', fontSize: '18px' }}>
            📧 {templatePreview.template_name}
          </h4>
          <div style={{ fontSize: '14px', marginTop: '10px' }}>
            <div style={{ marginBottom: '5px' }}>
              <strong>Recipient Count:</strong> {loadingEmails ? 'Loading...' : campaignEmails.length} emails
            </div>
            {customMessage && (
              <div style={{ backgroundColor: 'rgba(255,255,255,0.2)', padding: '8px', borderRadius: '4px', marginTop: '8px' }}>
                <strong>Custom Message:</strong> {customMessage}
              </div>
            )}
            {!customMessage && (
              <div style={{ backgroundColor: 'rgba(255,255,255,0.2)', padding: '8px', borderRadius: '4px', marginTop: '8px' }}>
                <strong>Using Default Message</strong>
              </div>
            )}
          </div>
        </div>
        
        {/* Final Email Content */}
        <div style={{ 
          height: '500px', 
          overflow: 'auto',
          backgroundColor: '#fff'
        }}>
          <iframe
            srcDoc={templatePreview.html_content
              ?.replace('{{message}}', finalMessage)
              ?.replace('{{name}}', recipientName)}
            style={{
              width: '100%',
              height: '100%',
              border: 'none',
              display: 'block'
            }}
            title="Final Email Preview"
          />
        </div>
      </div>
    </div>
  );
};

const EmailSender = ({ campaigns, templates }) => {
  const [campaignId, setCampaignId] = useState('');
  const [emailTemplate, setEmailTemplate] = useState('');
  const [customMessage, setCustomMessage] = useState('');
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState({ text: '', type: '' });
  const [templatePreview, setTemplatePreview] = useState(null);
  const [loadingPreview, setLoadingPreview] = useState(false);
  const [previewError, setPreviewError] = useState(null);

  useEffect(() => {
    if (emailTemplate) {
      loadTemplatePreview(emailTemplate);
    } else {
      setTemplatePreview(null);
    }
  }, [emailTemplate]);

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
            <option value="">Select a template</option>
            {templates.map((template) => (
              <option key={template.template_id} value={template.template_id}>
                {template.template_name}
              </option>
            ))}
          </select>
        </div>

        {/* Template Preview Section */}
        <div style={{ marginTop: '20px', marginBottom: '20px' }}>
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

        {/* Preview Button */}
        <div style={{ marginTop: '20px', marginBottom: '20px' }}>
          <button
            type="button"
            onClick={() => {
              if (!campaignId) {
                showMessage('Please select a campaign first', 'error');
                return;
              }
              if (!templatePreview) {
                showMessage('Please wait for template to load', 'error');
                return;
              }
              // Scroll to the preview section
              const previewSection = document.getElementById('final-preview');
              if (previewSection) {
                previewSection.scrollIntoView({ behavior: 'smooth' });
              }
            }}
            className="btn btn-primary"
            disabled={!campaignId || !templatePreview}
            style={{
              padding: '12px 24px',
              fontSize: '16px',
              fontWeight: 'bold',
              marginRight: '15px'
            }}
          >
            🔍 Preview Final Email
          </button>
          
          <button type="submit" className="btn btn-success" disabled={loading || !campaignId}>
            {loading ? 'Sending...' : '📧 Send Emails'}
          </button>
        </div>

        {/* Final Email Preview with Custom Message */}
        {templatePreview && campaignId && (
          <div id="final-preview">
            <FinalEmailPreview 
              templatePreview={templatePreview}
              customMessage={customMessage}
              campaignId={campaignId}
              campaigns={campaigns}
            />
          </div>
        )}
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
