#!/usr/bin/env python3
"""
Create a sample Excel file for testing email upload functionality
"""

import pandas as pd
import os

def create_sample_excel():
    """Create a sample Excel file with email data"""
    
    # Sample data
    data = {
        'name': [
            'John Doe',
            'Jane Smith',
            'Mike Johnson',
            'Sarah Wilson',
            'David Brown',
            'Emily Davis',
            'Robert Miller',
            'Lisa Garcia',
            'James Rodriguez',
            'Maria Martinez'
        ],
        'email_address': [
            'john.doe@example.com',
            'jane.smith@example.com',
            'mike.johnson@example.com',
            'sarah.wilson@example.com',
            'david.brown@example.com',
            'emily.davis@example.com',
            'robert.miller@example.com',
            'lisa.garcia@example.com',
            'james.rodriguez@example.com',
            'maria.martinez@example.com'
        ]
    }
    
    # Create DataFrame
    df = pd.DataFrame(data)
    
    # Create sample Excel file
    filename = 'sample_emails.xlsx'
    df.to_excel(filename, index=False)
    
    print(f"✅ Created sample Excel file: {filename}")
    print(f"📁 Location: {os.path.abspath(filename)}")
    print(f"📊 Contains {len(data['name'])} email addresses")
    print("\n📋 File structure:")
    print("   - name: Recipient names")
    print("   - email_address: Email addresses")
    print("\n💡 You can use this file to test the upload functionality in the Streamlit app!")

if __name__ == "__main__":
    create_sample_excel() 