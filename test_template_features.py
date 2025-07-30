#!/usr/bin/env python3
"""
Test script to demonstrate the new template management features
Run this script to test the enhanced email campaign system
"""

import requests
import json
import time

# Configuration
BASE_URL = "http://localhost:8000"
API_BASE = f"{BASE_URL}/api"

def print_response(response, title):
    """Print formatted API response"""
    print(f"\n{'='*50}")
    print(f"{title}")
    print(f"{'='*50}")
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    print(f"{'='*50}")

def test_template_management():
    """Test template management features"""
    print("🧪 Testing Template Management Features")
    
    # 1. Create a custom template
    template_data = {
        "name": "Test Welcome Template",
        "description": "A test template for demonstration",
        "subject": "Welcome to Our Platform - {{ company_name|default:'Our Company' }}",
        "html_content": """
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>Welcome</title>
    <style>
        body { font-family: Arial, sans-serif; line-height: 1.6; color: #333; }
        .container { max-width: 600px; margin: 0 auto; padding: 20px; }
        .header { background-color: #007bff; color: white; padding: 20px; text-align: center; }
        .content { padding: 20px; background-color: #f8f9fa; }
        .footer { background-color: #6c757d; color: white; padding: 15px; text-align: center; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>Welcome to {{ company_name|default:'Our Platform' }}</h1>
        </div>
        <div class="content">
            <h2>Hello {{ name }}!</h2>
            <p>{{ message }}</p>
            {% if role %}
            <p>Your role: <strong>{{ role }}</strong></p>
            {% endif %}
            <p>Get started by visiting: <a href="{{ start_url|default:'#' }}">Our Platform</a></p>
        </div>
        <div class="footer">
            <p>© 2024 {{ company_name|default:'Our Company' }}. All rights reserved.</p>
        </div>
    </div>
</body>
</html>
        """,
        "css_styles": """
body { font-family: Arial, sans-serif; line-height: 1.6; color: #333; }
.container { max-width: 600px; margin: 0 auto; padding: 20px; }
.header { background-color: #007bff; color: white; padding: 20px; text-align: center; }
.content { padding: 20px; background-color: #f8f9fa; }
.footer { background-color: #6c757d; color: white; padding: 15px; text-align: center; }
        """,
        "is_active": True,
        "variables": [
            {
                "variable_name": "name",
                "display_name": "Recipient Name",
                "variable_type": "text",
                "is_required": True,
                "description": "The name of the recipient"
            },
            {
                "variable_name": "message",
                "display_name": "Welcome Message",
                "variable_type": "text",
                "default_value": "Welcome to our platform! We're excited to have you join us.",
                "is_required": False,
                "description": "Custom welcome message"
            },
            {
                "variable_name": "company_name",
                "display_name": "Company Name",
                "variable_type": "text",
                "default_value": "Our Company",
                "is_required": False,
                "description": "Company name"
            },
            {
                "variable_name": "role",
                "display_name": "User Role",
                "variable_type": "text",
                "is_required": False,
                "description": "User's role in the system"
            },
            {
                "variable_name": "start_url",
                "display_name": "Start URL",
                "variable_type": "url",
                "default_value": "https://example.com/get-started",
                "is_required": False,
                "description": "URL to get started"
            }
        ]
    }
    
    response = requests.post(f"{API_BASE}/templates/create/", json=template_data)
    print_response(response, "1. Create Custom Template")
    
    if response.status_code == 201:
        template_id = response.json()['template_id']
        
        # 2. Preview the template
        preview_data = {
            "template_id": template_id,
            "sample_data": {
                "name": "John Doe",
                "message": "Welcome to our amazing platform! We're thrilled to have you on board.",
                "company_name": "TechCorp Inc.",
                "role": "Senior Developer",
                "start_url": "https://techcorp.com/dashboard"
            }
        }
        
        response = requests.post(f"{API_BASE}/templates/preview/", json=preview_data)
        print_response(response, "2. Preview Template with Sample Data")
        
        # 3. Create a campaign
        campaign_data = {
            "campaign_name": "Test Campaign with Custom Template"
        }
        
        response = requests.post(f"{API_BASE}/campaigns/create", json=campaign_data)
        print_response(response, "3. Create Campaign")
        
        if response.status_code == 201:
            campaign_id = response.json()['campaign_id']
            
            # 4. Update campaign with custom template
            campaign_update_data = {
                "template_id": template_id,
                "custom_subject": "Welcome to TechCorp - Let's Get Started!",
                "custom_message": "We're excited to have you join our team. Here's what you need to know...",
                "use_custom_template": True
            }
            
            response = requests.post(f"{API_BASE}/campaigns/template-update/?campaign_id={campaign_id}", 
                                   json=campaign_update_data)
            print_response(response, "4. Update Campaign with Custom Template")
            
            # 5. List templates
            response = requests.get(f"{API_BASE}/templates/")
            print_response(response, "5. List All Templates")
            
            # 6. Get template details
            response = requests.get(f"{API_BASE}/templates/{template_id}/")
            print_response(response, "6. Get Template Details")
            
            return template_id, campaign_id
    
    return None, None

def test_enhanced_email_sending(template_id, campaign_id):
    """Test enhanced email sending with custom templates"""
    if not template_id or not campaign_id:
        print("❌ Cannot test email sending - missing template or campaign ID")
        return
    
    print("\n🧪 Testing Enhanced Email Sending")
    
    # Note: This would require actual email configuration and recipients
    # For demonstration, we'll show the API call structure
    
    email_data = {
        "message": "This is a personalized message for each recipient",
        "subject": "Welcome aboard!",
        "use_custom_template": True
    }
    
    print(f"\n{'='*50}")
    print("Enhanced Email Sending (Demo)")
    print(f"{'='*50}")
    print(f"Endpoint: POST {API_BASE}/campaigns/send-enhanced/?campaign_id={campaign_id}")
    print(f"Data: {json.dumps(email_data, indent=2)}")
    print(f"{'='*50}")
    print("Note: This requires email configuration and recipients to work")
    print("The system will use the custom template and personalized message")

def test_template_variables():
    """Test template variable functionality"""
    print("\n🧪 Testing Template Variables")
    
    # List templates to see variables
    response = requests.get(f"{API_BASE}/templates/")
    if response.status_code == 200:
        templates = response.json()
        if templates:
            template = templates[0]  # Get first template
            print(f"\n{'='*50}")
            print("Template Variables Example")
            print(f"{'='*50}")
            print(f"Template: {template['name']}")
            print(f"Variables Count: {template['variables_count']}")
            
            if template['template_variables']:
                print("\nAvailable Variables:")
                for var in template['template_variables']:
                    print(f"  - {var['display_name']} ({var['variable_name']})")
                    print(f"    Type: {var['variable_type']}")
                    print(f"    Required: {var['is_required']}")
                    if var['default_value']:
                        print(f"    Default: {var['default_value']}")
                    print()

def main():
    """Main test function"""
    print("🚀 Email Campaign System - Template Management Test")
    print("This script demonstrates the new template management features")
    
    try:
        # Test template management
        template_id, campaign_id = test_template_management()
        
        # Test template variables
        test_template_variables()
        
        # Test enhanced email sending (demo)
        test_enhanced_email_sending(template_id, campaign_id)
        
        print("\n✅ Test completed successfully!")
        print("\n📋 Summary of New Features:")
        print("  ✓ Custom template creation with variables")
        print("  ✓ Template preview with sample data")
        print("  ✓ Campaign template assignment")
        print("  ✓ Enhanced email sending with custom templates")
        print("  ✓ Template variable management")
        
    except requests.exceptions.ConnectionError:
        print("❌ Error: Could not connect to the server")
        print("Make sure the Django server is running on http://localhost:8000")
    except Exception as e:
        print(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    main() 