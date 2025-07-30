#!/usr/bin/env python3
"""
Demo script for the Enhanced Email Campaign System
This script demonstrates all the new features and capabilities
"""

import requests
import json
import time
from datetime import datetime

# Configuration
API_BASE_URL = "http://localhost:8000/api"

def print_section(title):
    """Print a formatted section header"""
    print(f"\n{'='*60}")
    print(f"🎯 {title}")
    print(f"{'='*60}")

def print_success(message):
    """Print a success message"""
    print(f"✅ {message}")

def print_info(message):
    """Print an info message"""
    print(f"ℹ️ {message}")

def print_warning(message):
    """Print a warning message"""
    print(f"⚠️ {message}")

def make_api_request(endpoint, method="GET", data=None, params=None):
    """Make API request with error handling"""
    try:
        url = f"{API_BASE_URL}{endpoint}"
        if method == "GET":
            response = requests.get(url, params=params)
        elif method == "POST":
            response = requests.post(url, json=data, params=params)
        elif method == "PUT":
            response = requests.put(url, json=data)
        elif method == "DELETE":
            response = requests.delete(url)
        
        if response.status_code in [200, 201, 204]:
            return response.json() if response.content else {"message": "Success"}
        else:
            return {"error": f"API Error: {response.status_code} - {response.text}"}
    except requests.exceptions.ConnectionError:
        return {"error": "Cannot connect to the API server. Make sure Django is running on localhost:8000"}
    except Exception as e:
        return {"error": f"Request failed: {str(e)}"}

def demo_template_creation():
    """Demonstrate template creation features"""
    print_section("Template Creation Demo")
    
    # Create a professional welcome template
    welcome_template = {
        "name": "Professional Welcome Email",
        "description": "A modern, professional welcome email template with branding",
        "subject": "Welcome to {{ company_name|default:'Our Platform' }} - Let's Get Started!",
        "html_content": """
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Welcome</title>
    <style>
        body { 
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
            line-height: 1.6; 
            color: #333; 
            margin: 0; 
            padding: 0; 
        }
        .container { 
            max-width: 600px; 
            margin: 0 auto; 
            background-color: #ffffff; 
        }
        .header { 
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
            color: white; 
            padding: 40px 20px; 
            text-align: center; 
        }
        .content { 
            padding: 30px 20px; 
            background-color: #ffffff; 
        }
        .footer { 
            background-color: #f8f9fa; 
            color: #6c757d; 
            padding: 20px; 
            text-align: center; 
            font-size: 12px; 
        }
        .button { 
            display: inline-block; 
            padding: 12px 24px; 
            background-color: #007bff; 
            color: white; 
            text-decoration: none; 
            border-radius: 5px; 
            margin: 20px 0; 
        }
        .highlight { 
            background-color: #e3f2fd; 
            padding: 15px; 
            border-left: 4px solid #2196f3; 
            margin: 20px 0; 
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>Welcome to {{ company_name|default:'Our Platform' }}</h1>
            <p>We're excited to have you on board!</p>
        </div>
        <div class="content">
            <h2>Hello {{ name }}!</h2>
            <p>{{ message }}</p>
            
            <div class="highlight">
                <h3>🎉 What's Next?</h3>
                <ul>
                    <li>Complete your profile setup</li>
                    <li>Explore our features</li>
                    <li>Connect with our community</li>
                    <li>Start your first project</li>
                </ul>
            </div>
            
            {% if role %}
            <p><strong>Your Role:</strong> {{ role }}</p>
            {% endif %}
            
            <p style="text-align: center;">
                <a href="{{ start_url|default:'#' }}" class="button">Get Started Now</a>
            </p>
            
            <p>If you have any questions, don't hesitate to reach out to our support team at {{ support_email|default:'support@example.com' }}.</p>
        </div>
        <div class="footer">
            <p>© 2024 {{ company_name|default:'Our Company' }}. All rights reserved.</p>
            <p>This email was sent to {{ email }}. <a href="{{ unsubscribe_url|default:'#' }}">Unsubscribe</a></p>
        </div>
    </div>
</body>
</html>
        """,
        "css_styles": """
body { 
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
    line-height: 1.6; 
    color: #333; 
    margin: 0; 
    padding: 0; 
}
.container { 
    max-width: 600px; 
    margin: 0 auto; 
    background-color: #ffffff; 
}
.header { 
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
    color: white; 
    padding: 40px 20px; 
    text-align: center; 
}
.content { 
    padding: 30px 20px; 
    background-color: #ffffff; 
}
.footer { 
    background-color: #f8f9fa; 
    color: #6c757d; 
    padding: 20px; 
    text-align: center; 
    font-size: 12px; 
}
.button { 
    display: inline-block; 
    padding: 12px 24px; 
    background-color: #007bff; 
    color: white; 
    text-decoration: none; 
    border-radius: 5px; 
    margin: 20px 0; 
}
.highlight { 
    background-color: #e3f2fd; 
    padding: 15px; 
    border-left: 4px solid #2196f3; 
    margin: 20px 0; 
}
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
                "default_value": "Welcome to our platform! We're thrilled to have you join our community and can't wait to see what you'll accomplish.",
                "is_required": False,
                "description": "Personalized welcome message"
            },
            {
                "variable_name": "company_name",
                "display_name": "Company Name",
                "variable_type": "text",
                "default_value": "Our Platform",
                "is_required": False,
                "description": "Company or platform name"
            },
            {
                "variable_name": "role",
                "display_name": "User Role",
                "variable_type": "text",
                "is_required": False,
                "description": "User's role or position"
            },
            {
                "variable_name": "start_url",
                "display_name": "Start URL",
                "variable_type": "url",
                "default_value": "https://example.com/dashboard",
                "is_required": False,
                "description": "URL to get started"
            },
            {
                "variable_name": "support_email",
                "display_name": "Support Email",
                "variable_type": "email",
                "default_value": "support@example.com",
                "is_required": False,
                "description": "Support email address"
            },
            {
                "variable_name": "email",
                "display_name": "Recipient Email",
                "variable_type": "email",
                "is_required": False,
                "description": "Recipient's email address"
            }
        ]
    }
    
    print_info("Creating a professional welcome email template...")
    response = make_api_request("/templates/create/", method="POST", data=welcome_template)
    
    if "error" not in response:
        template_id = response['template_id']
        print_success(f"Template created successfully! ID: {template_id}")
        return template_id
    else:
        print_warning(f"Failed to create template: {response['error']}")
        return None

def demo_template_preview(template_id):
    """Demonstrate template preview functionality"""
    print_section("Template Preview Demo")
    
    if not template_id:
        print_warning("No template ID available for preview")
        return
    
    # Sample data for preview
    sample_data = {
        "name": "Sarah Johnson",
        "message": "Welcome to TechCorp! We're excited to have you join our team of innovators. Your expertise will be invaluable as we continue to push the boundaries of technology.",
        "company_name": "TechCorp Solutions",
        "role": "Senior Software Engineer",
        "start_url": "https://techcorp.com/onboarding",
        "support_email": "help@techcorp.com",
        "email": "sarah.johnson@techcorp.com"
    }
    
    print_info("Generating template preview with sample data...")
    preview_data = {
        "template_id": template_id,
        "sample_data": sample_data
    }
    
    response = make_api_request("/templates/preview/", method="POST", data=preview_data)
    
    if "error" not in response:
        print_success("Template preview generated successfully!")
        print_info(f"Subject: {response['subject']}")
        print_info(f"Variables used: {', '.join(response['variables_used'])}")
        print_info("HTML content rendered successfully")
    else:
        print_warning(f"Failed to generate preview: {response['error']}")

def demo_campaign_creation(template_id):
    """Demonstrate campaign creation with custom template"""
    print_section("Campaign Creation Demo")
    
    # Create a campaign
    campaign_data = {
        "campaign_name": "TechCorp Welcome Campaign 2024",
        "custom_subject": "Welcome to TechCorp - Your Journey Starts Here!",
        "custom_message": "We're thrilled to welcome you to the TechCorp family. Your expertise and passion will help us continue our mission of innovation and excellence.",
        "use_custom_template": True,
        "template_id": template_id
    }
    
    print_info("Creating a campaign with custom template...")
    response = make_api_request("/campaigns/create", method="POST", data=campaign_data)
    
    if "error" not in response:
        campaign_id = response['campaign_id']
        print_success(f"Campaign created successfully! ID: {campaign_id}")
        return campaign_id
    else:
        print_warning(f"Failed to create campaign: {response['error']}")
        return None

def demo_enhanced_email_sending(campaign_id):
    """Demonstrate enhanced email sending"""
    print_section("Enhanced Email Sending Demo")
    
    if not campaign_id:
        print_warning("No campaign ID available for email sending")
        return
    
    # Email sending data
    email_data = {
        "message": "Welcome to TechCorp! We're excited to have you join our team. Your expertise will be invaluable as we continue to push the boundaries of technology.",
        "subject": "Welcome aboard, Sarah!",
        "use_custom_template": True
    }
    
    print_info("Sending emails with custom template and personalized message...")
    response = make_api_request(
        f"/campaigns/send-enhanced/?campaign_id={campaign_id}",
        method="POST",
        data=email_data
    )
    
    if "error" not in response:
        print_success("Email sending initiated successfully!")
        print_info(f"Template used: {response.get('template_used', 'Custom Template')}")
        print_info(f"Message: {response.get('custom_message_used', 'Default message')}")
        if 'details' in response:
            details = response['details']
            print_info(f"Sent: {details.get('sent', 0)}, Failed: {details.get('failed', 0)}")
    else:
        print_warning(f"Failed to send emails: {response['error']}")

def demo_template_management():
    """Demonstrate template management features"""
    print_section("Template Management Demo")
    
    # List all templates
    print_info("Fetching all templates...")
    response = make_api_request("/templates/")
    
    if "error" not in response:
        templates = response
        print_success(f"Found {len(templates)} templates")
        
        for template in templates:
            print(f"  📧 {template['name']} (ID: {template['template_id']})")
            print(f"     Status: {'✅ Active' if template['is_active'] else '❌ Inactive'}")
            print(f"     Variables: {len(template['template_variables'])}")
            print(f"     Created: {template['created_at'][:10]}")
            print()
    else:
        print_warning(f"Failed to fetch templates: {response['error']}")

def demo_campaign_management():
    """Demonstrate campaign management features"""
    print_section("Campaign Management Demo")
    
    # List all campaigns
    print_info("Fetching all campaigns...")
    response = make_api_request("/campaigns/")
    
    if "error" not in response:
        campaigns = response
        print_success(f"Found {len(campaigns)} campaigns")
        
        for campaign in campaigns:
            print(f"  📋 {campaign['campaign_name']} (ID: {campaign['campaign_id']})")
            print(f"     Created: {campaign['created_at'][:10]}")
            print(f"     Updated: {campaign['updated_at'][:10]}")
            if campaign.get('custom_template'):
                print(f"     Template: {campaign['custom_template']['name']}")
            print()
    else:
        print_warning(f"Failed to fetch campaigns: {response['error']}")

def main():
    """Main demo function"""
    print_section("Email Campaign System - Feature Demo")
    print("This demo showcases all the new features of the enhanced email campaign system.")
    print("Make sure the Django server is running on localhost:8000")
    
    try:
        # Demo 1: Template Creation
        template_id = demo_template_creation()
        
        # Demo 2: Template Preview
        demo_template_preview(template_id)
        
        # Demo 3: Campaign Creation
        campaign_id = demo_campaign_creation(template_id)
        
        # Demo 4: Enhanced Email Sending
        demo_enhanced_email_sending(campaign_id)
        
        # Demo 5: Template Management
        demo_template_management()
        
        # Demo 6: Campaign Management
        demo_campaign_management()
        
        print_section("Demo Complete")
        print_success("All features demonstrated successfully!")
        print_info("You can now explore the Streamlit frontend at http://localhost:8501")
        print_info("Or use the API endpoints directly for programmatic access")
        
    except requests.exceptions.ConnectionError:
        print_warning("Cannot connect to the API server.")
        print_info("Please make sure Django is running on localhost:8000")
        print_info("Run: python manage.py runserver")
    except Exception as e:
        print_warning(f"Demo failed: {str(e)}")

if __name__ == "__main__":
    main() 