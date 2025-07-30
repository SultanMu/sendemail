# Email Campaign Management System

A powerful Django-based email campaign management system with advanced template management, custom messaging, and campaign automation features.

## 🚀 Features

### Core Features
- **Campaign Management**: Create, update, and delete email campaigns
- **Email Management**: Upload emails via Excel files, manage recipient lists
- **Email Sending**: Send emails to campaign recipients with detailed tracking
- **Template Management**: Create, edit, and manage custom email templates
- **Custom Messages**: Personalized messaging for each campaign

### Advanced Template Features
- **Custom Template Creation**: Build your own email templates with HTML/CSS
- **Template Variables**: Define dynamic variables for personalization
- **Template Preview**: Preview templates with sample data before sending
- **Template Categories**: Organize templates by type or purpose
- **Responsive Design**: Mobile-friendly email templates
- **Template Versioning**: Track template changes and updates

### Enhanced Campaign Control
- **Custom Subject Lines**: Set unique subject lines per campaign
- **Custom Messages**: Override default messages with campaign-specific content
- **Template Selection**: Choose between default and custom templates
- **A/B Testing Ready**: Framework for testing different templates
- **Campaign Analytics**: Track email performance and engagement

## 📋 API Endpoints

### Campaign Management
```
GET    /campaigns/                    # List all campaigns
POST   /campaigns/create              # Create new campaign
POST   /update-campaign               # Update campaign details
POST   /delete-campaign               # Delete campaign
GET    /list-emails/                  # List emails for campaign
POST   /upload-xls/                   # Upload emails via Excel
POST   /send-emails/                  # Send emails (legacy)
POST   /campaigns/send-enhanced/      # Send emails with custom templates
POST   /campaigns/template-update/    # Update campaign template settings
```

### Template Management
```
GET    /templates/                    # List all templates
POST   /templates/create/             # Create new template
GET    /templates/<id>/               # Get template details
PUT    /templates/<id>/update/        # Update template
DELETE /templates/<id>/delete/        # Delete template
POST   /templates/preview/            # Preview template with sample data
```

## 🛠 Installation & Setup

### Prerequisites
- Python 3.8+
- Django 4.0+
- PostgreSQL (recommended) or SQLite

### Installation Steps

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd sendemail
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

4. **Create sample templates (optional)**
   ```bash
   python manage.py create_sample_templates
   ```

5. **Run the development server**
   ```bash
   python manage.py runserver
   ```

## 📖 Usage Examples

### Using Custom Templates

The system now supports custom templates that you can create and assign to campaigns. Here's how to use them:

#### 1. Create a Custom Template
- Go to the **Templates** page in the Streamlit app
- Click **"Create New Template"**
- Fill in the template details:
  - **Name**: Give your template a descriptive name
  - **Description**: Explain what the template is for
  - **Subject**: Default subject line for emails
  - **HTML Content**: Your email template HTML
  - **CSS Styles**: Optional styling
  - **Template Variables**: Define dynamic variables like `{{ name }}`, `{{ message }}`

#### 2. Assign Template to Campaign
- Go to the **Campaigns** page
- Find the **"Update Campaign Settings"** section
- Select your campaign from the dropdown
- Check **"Use Custom Template for this Campaign"**
- Select your custom template from the dropdown
- Click **"Update Campaign Settings"**

#### 3. Send Emails with Custom Template
- Go to the **Send Emails** page
- Select your campaign
- The **"Use Custom Template"** checkbox should be pre-selected
- Your custom template should appear in the template selection
- Add any custom message or subject if needed
- Click **"Send Emails"**

#### Example Template HTML
```html
<!DOCTYPE html>
<html>
<head>
    <title>Welcome Email</title>
</head>
<body>
    <h1>Hello {{ name }}!</h1>
    <p>{{ message }}</p>
    <p>Welcome to our platform!</p>
    <a href="{{ signup_url }}">Complete Registration</a>
</body>
</html>
```

### Creating a Custom Template via API

```python
# Example API request to create a template
POST /templates/create/
{
    "name": "Welcome Email",
    "description": "Professional welcome email template",
    "subject": "Welcome to Our Platform",
    "html_content": "<!DOCTYPE html><html><body><h1>Hello {{ name }}!</h1><p>{{ message }}</p></body></html>",
    "css_styles": "body { font-family: Arial; }",
    "is_active": true,
    "variables": [
        {
            "variable_name": "name",
            "display_name": "Recipient Name",
            "variable_type": "text",
            "is_required": true,
            "description": "The name of the recipient"
        },
        {
            "variable_name": "message",
            "display_name": "Welcome Message",
            "variable_type": "text",
            "default_value": "Welcome to our platform!",
            "is_required": false,
            "description": "Custom welcome message"
        }
    ]
}
```

### Setting Up a Campaign with Custom Template

```python
# 1. Create a campaign
POST /campaigns/create/
{
    "campaign_name": "Welcome Campaign 2024"
}

# 2. Update campaign with custom template
POST /campaigns/template-update/?campaign_id=1
{
    "template_id": 1,
    "custom_subject": "Welcome to Our Amazing Platform!",
    "custom_message": "We're excited to have you join our community. Here's what you can expect...",
    "use_custom_template": true
}

# 3. Upload email list
POST /upload-xls/?campaign_id=1
# Upload Excel file with 'name' and 'email_address' columns

# 4. Send emails with custom template
POST /campaigns/send-enhanced/?campaign_id=1
{
    "message": "Personalized welcome message for each recipient",
    "subject": "Welcome aboard!",
    "use_custom_template": true
}
```

### Template Preview

```python
# Preview a template with sample data
POST /templates/preview/
{
    "template_id": 1,
    "sample_data": {
        "name": "John Doe",
        "message": "Welcome to our platform!",
        "company": "Acme Corp"
    }
}
```

## 🎨 Template Variables

The system supports various types of template variables:

- **Text**: General text content
- **Email**: Email addresses
- **URL**: Web links
- **Date**: Date values
- **Number**: Numeric values

### Variable Usage in Templates

```html
<!-- Basic variable usage -->
<h1>Hello {{ name }}!</h1>
<p>{{ message }}</p>

<!-- Conditional rendering -->
{% if company %}
<p>Welcome from {{ company }}!</p>
{% endif %}

<!-- Default values -->
<p>Contact us at {{ support_email|default:'support@example.com' }}</p>

<!-- Loops for dynamic content -->
<ul>
{% for item in items %}
    <li>{{ item }}</li>
{% endfor %}
</ul>
```

## 📊 Sample Templates

The system comes with three pre-built sample templates:

1. **Welcome Email Template**: Professional welcome emails with customizable content
2. **Newsletter Template**: Modern newsletter layout with featured content sections
3. **Promotional Email Template**: Attractive promotional emails for sales and offers

To create these sample templates, run:
```bash
python manage.py create_sample_templates
```

## 🔧 Configuration

### Email Settings

Configure your email settings in `settings.py`:

```python
# Email configuration
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your-email@gmail.com'
EMAIL_HOST_PASSWORD = 'your-app-password'
DEFAULT_FROM_EMAIL = 'your-email@gmail.com'
```

### File Upload Settings

```python
# File upload settings for Excel files
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MAX_UPLOAD_SIZE = 5242880  # 5MB
```

## 🚀 Advanced Features

### A/B Testing Framework

The system is designed to support A/B testing:

```python
# Example A/B test setup
{
    "campaign_id": 1,
    "template_a": 1,
    "template_b": 2,
    "test_percentage": 10,
    "winner_criteria": "open_rate"
}
```

### Campaign Scheduling

Future enhancement for scheduled campaigns:

```python
# Example scheduled campaign
{
    "campaign_id": 1,
    "template_id": 1,
    "scheduled_time": "2024-01-15T10:00:00Z",
    "timezone": "UTC"
}
```

## 📈 Analytics & Tracking

The system tracks:
- Email delivery status
- Open rates
- Click rates
- Bounce rates
- Unsubscribe rates

## 🔒 Security Features

- **Input Validation**: All user inputs are validated
- **SQL Injection Protection**: Django ORM provides protection
- **File Upload Security**: Excel file validation
- **Rate Limiting**: Configurable rate limits for API endpoints

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📝 License

This project is licensed under the MIT License.

## 🆘 Support

For support and questions:
- Create an issue in the repository
- Contact the development team
- Check the documentation

## 🔄 Changelog

### Version 2.0.0
- Added custom template management
- Enhanced campaign control
- Template preview functionality
- Variable system for personalization
- Sample templates included

### Version 1.0.0
- Basic campaign management
- Email upload via Excel
- Simple email sending
- Fixed templates only
