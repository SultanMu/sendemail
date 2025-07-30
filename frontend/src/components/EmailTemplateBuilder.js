
import React, { useState, useRef, useCallback } from 'react';
import { templateAPI } from '../services/api';

const EmailTemplateBuilder = () => {
  const [components, setComponents] = useState([]);
  const [selectedComponent, setSelectedComponent] = useState(null);
  const [templateName, setTemplateName] = useState('');
  const [subject, setSubject] = useState('');
  const [draggedComponent, setDraggedComponent] = useState(null);
  const [saving, setSaving] = useState(false);
  const [message, setMessage] = useState({ text: '', type: '' });
  const canvasRef = useRef(null);

  const showMessage = (text, type) => {
    setMessage({ text, type });
    setTimeout(() => setMessage({ text: '', type: '' }), 5000);
  };

  // Save template to database
  const saveTemplate = async () => {
    if (!templateName.trim()) {
      showMessage('Please enter a template name', 'error');
      return;
    }

    if (!subject.trim()) {
      showMessage('Please enter an email subject', 'error');
      return;
    }

    if (components.length === 0) {
      showMessage('Please add at least one component to your template', 'error');
      return;
    }

    try {
      setSaving(true);
      const htmlContent = generateHTML();
      
      await templateAPI.create({
        template_name: templateName,
        subject: subject,
        html_content: htmlContent
      });

      showMessage('Template saved successfully!', 'success');
      
      // Optionally reset form
      setTemplateName('');
      setSubject('');
      setComponents([]);
      setSelectedComponent(null);
      
    } catch (error) {
      showMessage(error.response?.data?.error || 'Error saving template', 'error');
    } finally {
      setSaving(false);
    }
  };

  // Available component types
  const componentTypes = [
    { 
      type: 'text', 
      label: 'Text Block', 
      icon: '📝',
      defaultProps: { 
        content: 'Click to edit text',
        fontSize: '16px',
        color: '#333333',
        textAlign: 'left',
        fontWeight: 'normal',
        fontFamily: 'Arial, sans-serif'
      }
    },
    { 
      type: 'heading', 
      label: 'Heading', 
      icon: 'H',
      defaultProps: { 
        content: 'Your Heading Here',
        fontSize: '24px',
        color: '#333333',
        textAlign: 'center',
        fontWeight: 'bold',
        fontFamily: 'Arial, sans-serif'
      }
    },
    { 
      type: 'image', 
      label: 'Image', 
      icon: '🖼️',
      defaultProps: { 
        src: 'https://via.placeholder.com/300x200',
        alt: 'Image',
        width: '300px',
        height: '200px',
        textAlign: 'center'
      }
    },
    { 
      type: 'button', 
      label: 'Button', 
      icon: '🔘',
      defaultProps: { 
        text: 'Click Here',
        backgroundColor: '#007bff',
        color: '#ffffff',
        padding: '12px 24px',
        borderRadius: '4px',
        textAlign: 'center',
        href: '#'
      }
    },
    { 
      type: 'divider', 
      label: 'Divider', 
      icon: '—',
      defaultProps: { 
        height: '1px',
        backgroundColor: '#cccccc',
        margin: '20px 0'
      }
    },
    { 
      type: 'spacer', 
      label: 'Spacer', 
      icon: '⬜',
      defaultProps: { 
        height: '30px'
      }
    }
  ];

  // Handle drag start from component palette
  const handleDragStart = (e, componentType) => {
    setDraggedComponent(componentType);
    e.dataTransfer.effectAllowed = 'copy';
  };

  // Handle drop on canvas
  const handleDrop = useCallback((e) => {
    e.preventDefault();
    if (!draggedComponent) return;

    const rect = canvasRef.current.getBoundingClientRect();
    const y = e.clientY - rect.top;
    
    // Find insertion index based on Y position
    let insertIndex = components.length;
    for (let i = 0; i < components.length; i++) {
      const componentElement = document.getElementById(`component-${i}`);
      if (componentElement) {
        const componentRect = componentElement.getBoundingClientRect();
        const componentY = componentRect.top - rect.top;
        if (y < componentY + componentRect.height / 2) {
          insertIndex = i;
          break;
        }
      }
    }

    const newComponent = {
      id: Date.now(),
      type: draggedComponent.type,
      props: { ...draggedComponent.defaultProps }
    };

    const newComponents = [...components];
    newComponents.splice(insertIndex, 0, newComponent);
    setComponents(newComponents);
    setDraggedComponent(null);
  }, [draggedComponent, components]);

  const handleDragOver = (e) => {
    e.preventDefault();
    e.dataTransfer.dropEffect = 'copy';
  };

  // Update component property
  const updateComponentProp = (componentId, propName, value) => {
    setComponents(components.map(comp => 
      comp.id === componentId 
        ? { ...comp, props: { ...comp.props, [propName]: value } }
        : comp
    ));
  };

  // Delete component
  const deleteComponent = (componentId) => {
    setComponents(components.filter(comp => comp.id !== componentId));
    setSelectedComponent(null);
  };

  // Move component up/down
  const moveComponent = (componentId, direction) => {
    const index = components.findIndex(comp => comp.id === componentId);
    if (index === -1) return;
    
    const newIndex = direction === 'up' ? index - 1 : index + 1;
    if (newIndex < 0 || newIndex >= components.length) return;

    const newComponents = [...components];
    [newComponents[index], newComponents[newIndex]] = [newComponents[newIndex], newComponents[index]];
    setComponents(newComponents);
  };

  // Generate HTML
  const generateHTML = () => {
    const htmlComponents = components.map(comp => {
      switch (comp.type) {
        case 'text':
          return `<p style="font-size: ${comp.props.fontSize}; color: ${comp.props.color}; text-align: ${comp.props.textAlign}; font-weight: ${comp.props.fontWeight}; font-family: ${comp.props.fontFamily}; margin: 10px 0;">${comp.props.content}</p>`;
        
        case 'heading':
          return `<h2 style="font-size: ${comp.props.fontSize}; color: ${comp.props.color}; text-align: ${comp.props.textAlign}; font-weight: ${comp.props.fontWeight}; font-family: ${comp.props.fontFamily}; margin: 20px 0;">${comp.props.content}</h2>`;
        
        case 'image':
          return `<div style="text-align: ${comp.props.textAlign}; margin: 10px 0;"><img src="${comp.props.src}" alt="${comp.props.alt}" style="width: ${comp.props.width}; height: ${comp.props.height}; max-width: 100%;" /></div>`;
        
        case 'button':
          return `<div style="text-align: ${comp.props.textAlign}; margin: 20px 0;"><a href="${comp.props.href}" style="display: inline-block; background-color: ${comp.props.backgroundColor}; color: ${comp.props.color}; padding: ${comp.props.padding}; text-decoration: none; border-radius: ${comp.props.borderRadius};">${comp.props.text}</a></div>`;
        
        case 'divider':
          return `<div style="height: ${comp.props.height}; background-color: ${comp.props.backgroundColor}; margin: ${comp.props.margin};"></div>`;
        
        case 'spacer':
          return `<div style="height: ${comp.props.height};"></div>`;
        
        default:
          return '';
      }
    }).join('');

    return `
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>${subject}</title>
</head>
<body style="margin: 0; padding: 20px; font-family: Arial, sans-serif; background-color: #f4f4f4;">
    <div style="max-width: 600px; margin: 0 auto; background-color: #ffffff; padding: 20px; border-radius: 8px;">
        ${htmlComponents}
    </div>
</body>
</html>`;
  };

  // Render component in canvas
  const renderComponent = (component, index) => {
    const isSelected = selectedComponent?.id === component.id;
    
    return (
      <div
        key={component.id}
        id={`component-${index}`}
        style={{
          border: isSelected ? '2px solid #007bff' : '1px solid transparent',
          margin: '2px 0',
          padding: '4px',
          cursor: 'pointer',
          position: 'relative'
        }}
        onClick={() => setSelectedComponent(component)}
      >
        {component.type === 'text' && (
          <p style={{
            fontSize: component.props.fontSize,
            color: component.props.color,
            textAlign: component.props.textAlign,
            fontWeight: component.props.fontWeight,
            fontFamily: component.props.fontFamily,
            margin: '10px 0'
          }}>
            {component.props.content}
          </p>
        )}
        
        {component.type === 'heading' && (
          <h2 style={{
            fontSize: component.props.fontSize,
            color: component.props.color,
            textAlign: component.props.textAlign,
            fontWeight: component.props.fontWeight,
            fontFamily: component.props.fontFamily,
            margin: '20px 0'
          }}>
            {component.props.content}
          </h2>
        )}
        
        {component.type === 'image' && (
          <div style={{ textAlign: component.props.textAlign, margin: '10px 0' }}>
            <img 
              src={component.props.src} 
              alt={component.props.alt}
              style={{
                width: component.props.width,
                height: component.props.height,
                maxWidth: '100%'
              }}
            />
          </div>
        )}
        
        {component.type === 'button' && (
          <div style={{ textAlign: component.props.textAlign, margin: '20px 0' }}>
            <a
              href={component.props.href}
              style={{
                display: 'inline-block',
                backgroundColor: component.props.backgroundColor,
                color: component.props.color,
                padding: component.props.padding,
                textDecoration: 'none',
                borderRadius: component.props.borderRadius
              }}
            >
              {component.props.text}
            </a>
          </div>
        )}
        
        {component.type === 'divider' && (
          <div style={{
            height: component.props.height,
            backgroundColor: component.props.backgroundColor,
            margin: component.props.margin
          }}></div>
        )}
        
        {component.type === 'spacer' && (
          <div style={{
            height: component.props.height,
            backgroundColor: '#f0f0f0',
            border: '1px dashed #ccc',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            fontSize: '12px',
            color: '#666'
          }}>
            Spacer ({component.props.height})
          </div>
        )}
        
        {isSelected && (
          <div style={{
            position: 'absolute',
            top: '-30px',
            right: '0',
            display: 'flex',
            gap: '4px'
          }}>
            <button
              onClick={(e) => { e.stopPropagation(); moveComponent(component.id, 'up'); }}
              style={{ padding: '2px 6px', fontSize: '12px' }}
            >
              ↑
            </button>
            <button
              onClick={(e) => { e.stopPropagation(); moveComponent(component.id, 'down'); }}
              style={{ padding: '2px 6px', fontSize: '12px' }}
            >
              ↓
            </button>
            <button
              onClick={(e) => { e.stopPropagation(); deleteComponent(component.id); }}
              style={{ padding: '2px 6px', fontSize: '12px', backgroundColor: '#dc3545', color: 'white' }}
            >
              ✕
            </button>
          </div>
        )}
      </div>
    );
  };

  // Render property editor
  const renderPropertyEditor = () => {
    if (!selectedComponent) {
      return <p style={{ color: '#666', fontStyle: 'italic' }}>Select a component to edit its properties</p>;
    }

    const component = selectedComponent;
    
    return (
      <div>
        <h4>Edit {component.type} properties:</h4>
        
        {(component.type === 'text' || component.type === 'heading') && (
          <>
            <div style={{ marginBottom: '10px' }}>
              <label>Content:</label>
              <textarea
                value={component.props.content}
                onChange={(e) => updateComponentProp(component.id, 'content', e.target.value)}
                style={{ width: '100%', minHeight: '60px', padding: '4px' }}
              />
            </div>
            <div style={{ marginBottom: '10px' }}>
              <label>Font Size:</label>
              <input
                type="text"
                value={component.props.fontSize}
                onChange={(e) => updateComponentProp(component.id, 'fontSize', e.target.value)}
                style={{ width: '100%', padding: '4px' }}
              />
            </div>
            <div style={{ marginBottom: '10px' }}>
              <label>Color:</label>
              <input
                type="color"
                value={component.props.color}
                onChange={(e) => updateComponentProp(component.id, 'color', e.target.value)}
                style={{ width: '100%', padding: '4px' }}
              />
            </div>
            <div style={{ marginBottom: '10px' }}>
              <label>Text Align:</label>
              <select
                value={component.props.textAlign}
                onChange={(e) => updateComponentProp(component.id, 'textAlign', e.target.value)}
                style={{ width: '100%', padding: '4px' }}
              >
                <option value="left">Left</option>
                <option value="center">Center</option>
                <option value="right">Right</option>
              </select>
            </div>
            <div style={{ marginBottom: '10px' }}>
              <label>Font Weight:</label>
              <select
                value={component.props.fontWeight}
                onChange={(e) => updateComponentProp(component.id, 'fontWeight', e.target.value)}
                style={{ width: '100%', padding: '4px' }}
              >
                <option value="normal">Normal</option>
                <option value="bold">Bold</option>
              </select>
            </div>
          </>
        )}

        {component.type === 'image' && (
          <>
            <div style={{ marginBottom: '10px' }}>
              <label>Image URL:</label>
              <input
                type="text"
                value={component.props.src}
                onChange={(e) => updateComponentProp(component.id, 'src', e.target.value)}
                style={{ width: '100%', padding: '4px' }}
              />
            </div>
            <div style={{ marginBottom: '10px' }}>
              <label>Alt Text:</label>
              <input
                type="text"
                value={component.props.alt}
                onChange={(e) => updateComponentProp(component.id, 'alt', e.target.value)}
                style={{ width: '100%', padding: '4px' }}
              />
            </div>
            <div style={{ marginBottom: '10px' }}>
              <label>Width:</label>
              <input
                type="text"
                value={component.props.width}
                onChange={(e) => updateComponentProp(component.id, 'width', e.target.value)}
                style={{ width: '100%', padding: '4px' }}
              />
            </div>
            <div style={{ marginBottom: '10px' }}>
              <label>Height:</label>
              <input
                type="text"
                value={component.props.height}
                onChange={(e) => updateComponentProp(component.id, 'height', e.target.value)}
                style={{ width: '100%', padding: '4px' }}
              />
            </div>
            <div style={{ marginBottom: '10px' }}>
              <label>Alignment:</label>
              <select
                value={component.props.textAlign}
                onChange={(e) => updateComponentProp(component.id, 'textAlign', e.target.value)}
                style={{ width: '100%', padding: '4px' }}
              >
                <option value="left">Left</option>
                <option value="center">Center</option>
                <option value="right">Right</option>
              </select>
            </div>
          </>
        )}

        {component.type === 'button' && (
          <>
            <div style={{ marginBottom: '10px' }}>
              <label>Button Text:</label>
              <input
                type="text"
                value={component.props.text}
                onChange={(e) => updateComponentProp(component.id, 'text', e.target.value)}
                style={{ width: '100%', padding: '4px' }}
              />
            </div>
            <div style={{ marginBottom: '10px' }}>
              <label>Link URL:</label>
              <input
                type="text"
                value={component.props.href}
                onChange={(e) => updateComponentProp(component.id, 'href', e.target.value)}
                style={{ width: '100%', padding: '4px' }}
              />
            </div>
            <div style={{ marginBottom: '10px' }}>
              <label>Background Color:</label>
              <input
                type="color"
                value={component.props.backgroundColor}
                onChange={(e) => updateComponentProp(component.id, 'backgroundColor', e.target.value)}
                style={{ width: '100%', padding: '4px' }}
              />
            </div>
            <div style={{ marginBottom: '10px' }}>
              <label>Text Color:</label>
              <input
                type="color"
                value={component.props.color}
                onChange={(e) => updateComponentProp(component.id, 'color', e.target.value)}
                style={{ width: '100%', padding: '4px' }}
              />
            </div>
            <div style={{ marginBottom: '10px' }}>
              <label>Alignment:</label>
              <select
                value={component.props.textAlign}
                onChange={(e) => updateComponentProp(component.id, 'textAlign', e.target.value)}
                style={{ width: '100%', padding: '4px' }}
              >
                <option value="left">Left</option>
                <option value="center">Center</option>
                <option value="right">Right</option>
              </select>
            </div>
          </>
        )}

        {component.type === 'divider' && (
          <>
            <div style={{ marginBottom: '10px' }}>
              <label>Height:</label>
              <input
                type="text"
                value={component.props.height}
                onChange={(e) => updateComponentProp(component.id, 'height', e.target.value)}
                style={{ width: '100%', padding: '4px' }}
              />
            </div>
            <div style={{ marginBottom: '10px' }}>
              <label>Color:</label>
              <input
                type="color"
                value={component.props.backgroundColor}
                onChange={(e) => updateComponentProp(component.id, 'backgroundColor', e.target.value)}
                style={{ width: '100%', padding: '4px' }}
              />
            </div>
          </>
        )}

        {component.type === 'spacer' && (
          <div style={{ marginBottom: '10px' }}>
            <label>Height:</label>
            <input
              type="text"
              value={component.props.height}
              onChange={(e) => updateComponentProp(component.id, 'height', e.target.value)}
              style={{ width: '100%', padding: '4px' }}
            />
          </div>
        )}
      </div>
    );
  };

  return (
    <div style={{ display: 'flex', height: '100vh', fontFamily: 'Arial, sans-serif' }}>
      {/* Component Palette */}
      <div style={{ 
        width: '200px', 
        backgroundColor: '#f8f9fa', 
        padding: '20px', 
        borderRight: '1px solid #ddd',
        overflowY: 'auto'
      }}>
        <h3 style={{ margin: '0 0 20px 0' }}>Components</h3>
        {componentTypes.map((comp) => (
          <div
            key={comp.type}
            draggable
            onDragStart={(e) => handleDragStart(e, comp)}
            style={{
              padding: '12px',
              margin: '8px 0',
              backgroundColor: '#ffffff',
              border: '1px solid #ddd',
              borderRadius: '4px',
              cursor: 'grab',
              display: 'flex',
              alignItems: 'center',
              gap: '8px'
            }}
          >
            <span style={{ fontSize: '18px' }}>{comp.icon}</span>
            <span style={{ fontSize: '14px' }}>{comp.label}</span>
          </div>
        ))}
      </div>

      {/* Canvas */}
      <div style={{ flex: 1, display: 'flex', flexDirection: 'column' }}>
        {/* Header */}
        <div style={{ padding: '20px', borderBottom: '1px solid #ddd', backgroundColor: '#ffffff' }}>
          <div style={{ display: 'flex', gap: '20px', marginBottom: '15px' }}>
            <div style={{ flex: 1 }}>
              <label>Template Name:</label>
              <input
                type="text"
                value={templateName}
                onChange={(e) => setTemplateName(e.target.value)}
                placeholder="Enter template name"
                style={{ width: '100%', padding: '8px', marginTop: '4px' }}
              />
            </div>
            <div style={{ flex: 1 }}>
              <label>Email Subject:</label>
              <input
                type="text"
                value={subject}
                onChange={(e) => setSubject(e.target.value)}
                placeholder="Enter email subject"
                style={{ width: '100%', padding: '8px', marginTop: '4px' }}
              />
            </div>
          </div>
          <div style={{ display: 'flex', gap: '10px' }}>
            <button
              onClick={saveTemplate}
              disabled={saving}
              style={{
                padding: '10px 20px',
                backgroundColor: saving ? '#6c757d' : '#dc3545',
                color: 'white',
                border: 'none',
                borderRadius: '4px',
                cursor: saving ? 'not-allowed' : 'pointer'
              }}
            >
              {saving ? 'Saving...' : 'Save Template'}
            </button>
            <button
              onClick={() => {
                const html = generateHTML();
                const blob = new Blob([html], { type: 'text/html' });
                const url = URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.href = url;
                a.download = `${templateName || 'email-template'}.html`;
                a.click();
                URL.revokeObjectURL(url);
              }}
              style={{
                padding: '10px 20px',
                backgroundColor: '#28a745',
                color: 'white',
                border: 'none',
                borderRadius: '4px',
                cursor: 'pointer'
              }}
            >
              Export HTML
            </button>
            <button
              onClick={() => {
                const preview = window.open('', '_blank');
                preview.document.write(generateHTML());
                preview.document.close();
              }}
              style={{
                padding: '10px 20px',
                backgroundColor: '#007bff',
                color: 'white',
                border: 'none',
                borderRadius: '4px',
                cursor: 'pointer'
              }}
            >
              Preview
            </button>
          </div>
          
          {/* Message Display */}
          {message.text && (
            <div style={{
              marginTop: '15px',
              padding: '10px',
              borderRadius: '4px',
              backgroundColor: message.type === 'error' ? '#f8d7da' : '#d4edda',
              color: message.type === 'error' ? '#721c24' : '#155724',
              border: `1px solid ${message.type === 'error' ? '#f5c6cb' : '#c3e6cb'}`
            }}>
              {message.text}
            </div>
          )}
        </div>

        {/* Canvas Area */}
        <div
          ref={canvasRef}
          onDrop={handleDrop}
          onDragOver={handleDragOver}
          style={{
            flex: 1,
            backgroundColor: '#f4f4f4',
            padding: '20px',
            overflowY: 'auto'
          }}
        >
          <div style={{
            maxWidth: '600px',
            margin: '0 auto',
            backgroundColor: '#ffffff',
            padding: '20px',
            borderRadius: '8px',
            minHeight: '400px',
            border: draggedComponent ? '2px dashed #007bff' : '1px solid #ddd'
          }}>
            {components.length === 0 ? (
              <div style={{
                textAlign: 'center',
                color: '#666',
                fontSize: '18px',
                padding: '60px 20px'
              }}>
                Drag components here to start building your email template
              </div>
            ) : (
              components.map(renderComponent)
            )}
          </div>
        </div>
      </div>

      {/* Property Panel */}
      <div style={{
        width: '300px',
        backgroundColor: '#f8f9fa',
        padding: '20px',
        borderLeft: '1px solid #ddd',
        overflowY: 'auto'
      }}>
        <h3 style={{ margin: '0 0 20px 0' }}>Properties</h3>
        {renderPropertyEditor()}
      </div>
    </div>
  );
};

export default EmailTemplateBuilder;
