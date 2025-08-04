import React, { useState } from 'react';
import { templateAPI } from '../services/api';

const EmailTemplateEditor = ({ templates, refreshTemplates }) => {
  const [selectedTemplate, setSelectedTemplate] = useState('');
  const [templateName, setTemplateName] = useState('');
  const [subject, setSubject] = useState('');
  const [htmlContent, setHtmlContent] = useState('');
  const [message, setMessage] = useState({ text: '', type: '' });

  const handleTemplateChange = (e) => {
    const templateId = e.target.value;
    const template = templates.find((t) => t.template_id.toString() === templateId);
    if (template) {
      setSelectedTemplate(templateId);
      setTemplateName(template.template_name);
      setSubject(template.subject);
      setHtmlContent(template.html_content);
    } else {
      setSelectedTemplate('');
      setTemplateName('');
      setSubject('');
      setHtmlContent('');
    }
  };

  const handleSave = async () => {
    if (!selectedTemplate) {
      showMessage('Please select a template to update', 'error');
      return;
    }

    try {
      const templateData = {
        template_name: templateName,
        subject: subject,
        html_content: htmlContent,
      };
      await templateAPI.update(selectedTemplate, templateData);
      showMessage('Template updated successfully', 'success');
      refreshTemplates(); // Refresh the list
    } catch (error) {
      showMessage('Error updating template', 'error');
    }
  };

  const showMessage = (text, type) => {
    setMessage({ text, type });
    setTimeout(() => setMessage({ text: '', type: '' }), 5000);
  };

  return (
    <div className="section">
      <h2>Edit Email Template</h2>
      <div className="form-group">
        <label htmlFor="template-select">Select Template:</label>
        <select
          id="template-select"
          className="form-control"
          value={selectedTemplate}
          onChange={handleTemplateChange}
        >
          <option value="">Select a template</option>
          {templates.map((template) => (
            <option key={template.template_id} value={template.template_id}>
              {template.template_name}
            </option>
          ))}
        </select>
      </div>

      {selectedTemplate && (
        <div className="editor-container">
          <div className="editor-form">
            <div className="form-group">
              <label htmlFor="template-name">Template Name:</label>
              <input
                type="text"
                id="template-name"
                className="form-control"
                value={templateName}
                onChange={(e) => setTemplateName(e.target.value)}
              />
            </div>
            <div className="form-group">
              <label htmlFor="subject">Subject:</label>
              <input
                type="text"
                id="subject"
                className="form-control"
                value={subject}
                onChange={(e) => setSubject(e.target.value)}
              />
            </div>
            <div className="form-group">
              <label htmlFor="html-content">HTML Content:</label>
              <textarea
                id="html-content"
                className="form-control"
                rows="15"
                value={htmlContent}
                onChange={(e) => setHtmlContent(e.target.value)}
              />
            </div>
            <button className="btn btn-success" onClick={handleSave}>
              Save Template
            </button>
          </div>
          <div className="editor-preview">
            <h3>Live Preview</h3>
            <iframe
              srcDoc={htmlContent}
              title="Template Preview"
              className="preview-iframe"
            />
          </div>
        </div>
      )}

      {message.text && (
        <div className={`alert ${message.type === 'error' ? 'alert-error' : 'alert-success'}`}>
          {message.text}
        </div>
      )}

      <style>{`
        .editor-container {
          display: flex;
          gap: 20px;
        }
        .editor-form {
          flex: 1;
        }
        .editor-preview {
          flex: 1;
          border: 1px solid #ccc;
          padding: 10px;
        }
        .preview-iframe {
          width: 100%;
          height: 500px;
          border: none;
        }
      `}</style>
    </div>
  );
};

export default EmailTemplateEditor;
