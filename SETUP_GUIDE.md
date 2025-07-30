# Quick Setup Guide - Enhanced Email Campaign System

This guide will help you set up and start using the enhanced email campaign system with custom template management and a beautiful Streamlit frontend.

## 🚀 Quick Start (Recommended)

### Option 1: One-Click Start (Windows)
```bash
# Double-click the file or run in command prompt
start_app.bat
```

### Option 2: One-Click Start (Mac/Linux)
```bash
# Make executable and run
chmod +x start_app.sh
./start_app.sh
```

### Option 3: Manual Start
```bash
# Install dependencies
pip install -r requirements.txt

# Run the launcher
python run_app.py
```

## 🎨 Streamlit Frontend Features

The new Streamlit frontend provides a beautiful, user-friendly interface for:

### 📊 Dashboard
- Overview of campaigns and templates
- Quick action buttons
- System statistics

### 📋 Campaign Management
- Create new campaigns with custom templates
- View existing campaigns in a table format
- Campaign actions (edit, delete, view details)

### 🎨 Template Management
- **Visual Template Editor**: Create templates with HTML/CSS
- **Template Variables**: Define dynamic variables for personalization
- **Template Preview**: See how emails look before sending
- **Template Gallery**: View templates in table or card format
- **Live Preview**: Render templates with sample data

### 📧 Email Management
- Upload email lists via Excel files
- View email lists for campaigns
- Email management interface

### 📤 Send Emails
- Select campaigns and templates
- Customize messages and subjects
- Send emails with custom templates
- Preview before sending

### 📊 Analytics (Coming Soon)
- Campaign performance metrics
- Template usage statistics
- Engagement analytics

## 🛠 Manual Setup (Advanced)

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run Database Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 3. Create Sample Templates (Optional)
```bash
python manage.py create_sample_templates
```

### 4. Start the Application

#### Start Both Backend and Frontend
```bash
python run_app.py
# Choose option 1 when prompted
```

#### Start Only Django Backend
```bash
python manage.py runserver
```

#### Start Only Streamlit Frontend
```bash
streamlit run streamlit_app.py
```

## 🌐 Access Points

Once started, you can access:

- **🎨 Streamlit Frontend**: http://localhost:8501
- **📧 Django Backend API**: http://localhost:8000
- **📚 Django Admin**: http://localhost:8000/admin

## 🧪 Testing the New Features

### Using the Streamlit Frontend

1. **Create a Template**:
   - Go to "Templates" page
   - Click "Create New Template"
   - Fill in template details and HTML content
   - Add template variables
   - Click "Create Template"

2. **Preview a Template**:
   - Go to "Templates" page
   - Click "Preview" on any template
   - Enter sample data
   - Click "Generate Preview"

3. **Create a Campaign**:
   - Go to "Campaigns" page
   - Click "Create New Campaign"
   - Select a custom template
   - Add custom subject and message
   - Click "Create Campaign"

4. **Send Emails**:
   - Go to "Send Emails" page
   - Select a campaign
   - Choose template and customize message
   - Click "Send Emails"

### Using the API Directly

You can still use the API endpoints directly:

```bash
# Create a template
curl -X POST http://localhost:8000/api/templates/create/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "My Template",
    "subject": "Welcome",
    "html_content": "<h1>Hello {{ name }}!</h1>",
    "variables": [{"variable_name": "name", "display_name": "Name", "variable_type": "text"}]
  }'

# Preview template
curl -X POST http://localhost:8000/api/templates/preview/ \
  -H "Content-Type: application/json" \
  -d '{"template_id": 1, "sample_data": {"name": "John"}}'
```

## 📋 Available API Endpoints

### Template Management
- `GET /api/templates/` - List all templates
- `POST /api/templates/create/` - Create new template
- `GET /api/templates/{id}/` - Get template details
- `PUT /api/templates/{id}/update/` - Update template
- `DELETE /api/templates/{id}/delete/` - Delete template
- `POST /api/templates/preview/` - Preview template

### Enhanced Campaign Management
- `POST /api/campaigns/template-update/` - Update campaign template settings
- `POST /api/campaigns/send-enhanced/` - Send emails with custom templates

### Legacy Endpoints (Still Available)
- `GET /api/campaigns/` - List campaigns
- `POST /api/campaigns/create` - Create campaign
- `POST /api/upload-xls/` - Upload emails
- `POST /api/send-emails/` - Send emails (legacy)

## 🎨 Template Variable Types

- **text**: General text content
- **email**: Email addresses
- **url**: Web links
- **date**: Date values
- **number**: Numeric values

## 📧 Email Configuration

Before sending emails, configure your email settings in `settings.py`:

```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your-email@gmail.com'
EMAIL_HOST_PASSWORD = 'your-app-password'
DEFAULT_FROM_EMAIL = 'your-email@gmail.com'
```

## 🔧 Troubleshooting

### Common Issues

1. **Port Already in Use**
   ```bash
   # Kill processes using ports 8000 or 8501
   # Windows
   netstat -ano | findstr :8000
   taskkill /PID <PID> /F
   
   # Mac/Linux
   lsof -ti:8000 | xargs kill -9
   ```

2. **Dependencies Not Found**
   ```bash
   pip install -r requirements.txt
   ```

3. **Database Migration Errors**
   ```bash
   python manage.py makemigrations mailer
   python manage.py migrate
   ```

4. **Streamlit Not Starting**
   ```bash
   # Check if streamlit is installed
   pip install streamlit
   streamlit --version
   ```

5. **API Connection Errors**
   - Ensure Django server is running on localhost:8000
   - Check if the API endpoints are accessible
   - Verify CORS settings if needed

### Debug Mode

Enable debug mode in `settings.py` for detailed error messages:
```python
DEBUG = True
```

## 📚 Next Steps

1. **Explore the Streamlit Interface**: Navigate through all pages
2. **Create Sample Templates**: Use the template creation form
3. **Test Template Preview**: See how templates render with sample data
4. **Create Campaigns**: Set up campaigns with custom templates
5. **Upload Email Lists**: Use Excel files with name and email_address columns
6. **Send Test Emails**: Use the enhanced sending interface

## 🆘 Need Help?

- **Frontend Issues**: Check Streamlit logs in the terminal
- **Backend Issues**: Check Django logs in the terminal
- **API Issues**: Use the test script: `python test_template_features.py`
- **Documentation**: Check the main README.md for detailed API documentation

## 🎯 Key Benefits of the Enhanced System

✅ **Beautiful UI**: Modern Streamlit interface for easy testing
✅ **Visual Template Editor**: Create templates with HTML/CSS
✅ **Template Preview**: See emails before sending
✅ **Template Variables**: Dynamic content personalization
✅ **Campaign Control**: Custom subjects and messages per campaign
✅ **One-Click Setup**: Easy startup with launcher scripts
✅ **Backward Compatibility**: Existing functionality still works
✅ **Sample Templates**: Ready-to-use templates included 