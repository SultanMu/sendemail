#!/usr/bin/env python3
"""
Test script to verify custom template functionality
"""

import requests
import json

# Configuration
API_BASE_URL = "http://localhost:8000/api"

def test_custom_templates():
    """Test the custom template functionality"""
    
    print("🧪 Testing Custom Template Functionality")
    print("=" * 50)
    
    # Step 1: Create a custom template
    print("\n1️⃣ Creating a custom template...")
    template_data = {
        "name": "Test Custom Template",
        "description": "A test template for verification",
        "subject": "Test Email Subject",
        "html_content": """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Test Template</title>
        </head>
        <body>
            <h1>Hello {{ name }}!</h1>
            <p>{{ message }}</p>
            <p>This is a test custom template.</p>
        </body>
        </html>
        """,
        "css_styles": "body { font-family: Arial, sans-serif; }",
        "is_active": True,
        "variables": []
    }
    
    response = requests.post(f"{API_BASE_URL}/templates/create/", json=template_data)
    
    if response.status_code == 201:
        template = response.json()
        template_id = template['template_id']
        print(f"✅ Template created with ID: {template_id}")
    else:
        print(f"❌ Failed to create template: {response.text}")
        return
    
    # Step 2: Create a campaign
    print("\n2️⃣ Creating a campaign...")
    campaign_data = {
        "campaign_name": "Test Campaign for Custom Template",
        "custom_subject": "Test Campaign Subject",
        "custom_message": "Test campaign message",
        "use_custom_template": True,
        "template_id": template_id
    }
    
    response = requests.post(f"{API_BASE_URL}/campaigns/create", json=campaign_data)
    
    if response.status_code == 201:
        campaign = response.json()
        campaign_id = campaign['campaign_id']
        print(f"✅ Campaign created with ID: {campaign_id}")
    else:
        print(f"❌ Failed to create campaign: {response.text}")
        return
    
    # Step 3: List campaigns to verify template assignment
    print("\n3️⃣ Listing campaigns to verify template assignment...")
    response = requests.get(f"{API_BASE_URL}/campaigns/")
    
    if response.status_code == 200:
        campaigns = response.json()
        print(f"✅ Found {len(campaigns)} campaigns")
        
        # Find our test campaign
        test_campaign = None
        for campaign in campaigns:
            if campaign['campaign_name'] == "Test Campaign for Custom Template":
                test_campaign = campaign
                break
        
        if test_campaign:
            print(f"✅ Test campaign found:")
            print(f"   - Campaign ID: {test_campaign['campaign_id']}")
            print(f"   - Use Custom Template: {test_campaign['use_custom_template']}")
            print(f"   - Custom Template ID: {test_campaign['custom_template_id']}")
            print(f"   - Custom Subject: {test_campaign['custom_subject']}")
            print(f"   - Custom Message: {test_campaign['custom_message']}")
            
            if test_campaign['custom_template']:
                print(f"   - Template Name: {test_campaign['custom_template']['name']}")
        else:
            print("❌ Test campaign not found in list")
    else:
        print(f"❌ Failed to list campaigns: {response.text}")
    
    # Step 4: List templates to verify our template is available
    print("\n4️⃣ Listing templates...")
    response = requests.get(f"{API_BASE_URL}/templates/")
    
    if response.status_code == 200:
        templates = response.json()
        print(f"✅ Found {len(templates)} templates")
        
        # Find our test template
        test_template = None
        for template in templates:
            if template['name'] == "Test Custom Template":
                test_template = template
                break
        
        if test_template:
            print(f"✅ Test template found:")
            print(f"   - Template ID: {test_template['template_id']}")
            print(f"   - Name: {test_template['name']}")
            print(f"   - Active: {test_template['is_active']}")
        else:
            print("❌ Test template not found in list")
    else:
        print(f"❌ Failed to list templates: {response.text}")
    
    # Step 5: Test campaign update
    print("\n5️⃣ Testing campaign update...")
    update_data = {
        "custom_subject": "Updated Test Subject",
        "custom_message": "Updated test message",
        "use_custom_template": True,
        "template_id": template_id
    }
    
    response = requests.post(
        f"{API_BASE_URL}/campaigns/template-update/?campaign_id={campaign_id}",
        json=update_data
    )
    
    if response.status_code == 200:
        updated_campaign = response.json()
        print(f"✅ Campaign updated successfully:")
        print(f"   - Updated Subject: {updated_campaign['custom_subject']}")
        print(f"   - Updated Message: {updated_campaign['custom_message']}")
        print(f"   - Use Custom Template: {updated_campaign['use_custom_template']}")
        print(f"   - Custom Template ID: {updated_campaign['custom_template_id']}")
    else:
        print(f"❌ Failed to update campaign: {response.text}")
    
    print("\n🎉 Custom template functionality test completed!")
    print("\n📋 Summary:")
    print(f"   - Template ID: {template_id}")
    print(f"   - Campaign ID: {campaign_id}")
    print("   - You can now test this in the Streamlit app:")
    print("     1. Go to Campaigns page and update the campaign settings")
    print("     2. Go to Send Emails page and select the campaign")
    print("     3. Check 'Use Custom Template' and select your template")

if __name__ == "__main__":
    try:
        test_custom_templates()
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to the API. Make sure the Django server is running on http://localhost:8000")
    except Exception as e:
        print(f"❌ Error: {str(e)}") 