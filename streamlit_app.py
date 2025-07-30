import streamlit as st
import requests
import json
import pandas as pd
import plotly.express as px
from datetime import datetime
import base64

# Configuration
API_BASE_URL = "http://localhost:8000/api"

# Page configuration
st.set_page_config(
    page_title="Email Campaign Manager",
    page_icon="📧",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .section-header {
        font-size: 1.5rem;
        color: #2c3e50;
        margin-bottom: 1rem;
        border-bottom: 2px solid #3498db;
        padding-bottom: 0.5rem;
    }
    .success-box {
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        border-radius: 5px;
        padding: 1rem;
        margin: 1rem 0;
    }
    .error-box {
        background-color: #f8d7da;
        border: 1px solid #f5c6cb;
        border-radius: 5px;
        padding: 1rem;
        margin: 1rem 0;
    }
    .info-box {
        background-color: #d1ecf1;
        border: 1px solid #bee5eb;
        border-radius: 5px;
        padding: 1rem;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

def make_api_request(endpoint, method="GET", data=None, params=None, files=None):
    """Make API request with error handling"""
    try:
        url = f"{API_BASE_URL}{endpoint}"
        if method == "GET":
            response = requests.get(url, params=params)
        elif method == "POST":
            if files:
                # Handle file uploads
                response = requests.post(url, files=files, params=params)
            else:
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

def main():
    st.markdown('<h1 class="main-header">📧 Email Campaign Manager</h1>', unsafe_allow_html=True)
    
    # Sidebar navigation
    st.sidebar.title("Navigation")
    page = st.sidebar.selectbox(
        "Choose a page",
        ["Dashboard", "Campaigns", "Templates", "Email Management", "Send Emails", "Analytics"]
    )
    
    if page == "Dashboard":
        show_dashboard()
    elif page == "Campaigns":
        show_campaigns()
    elif page == "Templates":
        show_templates()
    elif page == "Email Management":
        show_email_management()
    elif page == "Send Emails":
        show_send_emails()
    elif page == "Analytics":
        show_analytics()

def show_dashboard():
    st.markdown('<h2 class="section-header">📊 Dashboard</h2>', unsafe_allow_html=True)
    
    # Get basic stats
    campaigns_response = make_api_request("/campaigns/")
    templates_response = make_api_request("/templates/")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if "error" not in campaigns_response:
            campaign_count = len(campaigns_response)
            st.metric("Total Campaigns", campaign_count)
        else:
            st.metric("Total Campaigns", "N/A")
    
    with col2:
        if "error" not in templates_response:
            template_count = len(templates_response)
            st.metric("Total Templates", template_count)
        else:
            st.metric("Total Templates", "N/A")
    
    with col3:
        st.metric("Active Templates", "Coming Soon")
    
    with col4:
        st.metric("Emails Sent Today", "Coming Soon")
    
    # Quick actions
    st.markdown('<h3 class="section-header">🚀 Quick Actions</h3>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📝 Create New Campaign", use_container_width=True):
            st.session_state.page = "Campaigns"
            st.rerun()
    
    with col2:
        if st.button("🎨 Create Template", use_container_width=True):
            st.session_state.page = "Templates"
            st.rerun()
    
    with col3:
        if st.button("📤 Send Emails", use_container_width=True):
            st.session_state.page = "Send Emails"
            st.rerun()

def show_campaigns():
    st.markdown('<h2 class="section-header">📋 Campaign Management</h2>', unsafe_allow_html=True)
    
    # Create new campaign
    with st.expander("➕ Create New Campaign", expanded=True):
        with st.form("create_campaign"):
            campaign_name = st.text_input("Campaign Name", placeholder="Enter campaign name")
            custom_subject = st.text_input("Custom Subject (Optional)", placeholder="Enter custom subject")
            custom_message = st.text_area("Custom Message (Optional)", placeholder="Enter custom message")
            
            # Template selection
            templates_response = make_api_request("/templates/")
            if "error" not in templates_response:
                template_options = {t["name"]: t["template_id"] for t in templates_response}
                template_options["Use Default Templates"] = None
                selected_template = st.selectbox("Select Template", list(template_options.keys()))
                use_custom_template = st.checkbox("Use Custom Template", value=False)
            else:
                st.warning("Could not load templates")
                use_custom_template = False
            
            submitted = st.form_submit_button("Create Campaign")
            
            if submitted and campaign_name:
                campaign_data = {
                    "campaign_name": campaign_name,
                    "custom_subject": custom_subject,
                    "custom_message": custom_message,
                    "use_custom_template": use_custom_template
                }
                
                if use_custom_template and selected_template != "Use Default Templates":
                    campaign_data["template_id"] = template_options[selected_template]
                
                response = make_api_request("/campaigns/create", method="POST", data=campaign_data)
                
                if "error" not in response:
                    st.success(f"Campaign '{campaign_name}' created successfully!")
                    st.balloons()
                else:
                    st.error(response["error"])
    
    # List existing campaigns
    st.markdown('<h3 class="section-header">📋 Existing Campaigns</h3>', unsafe_allow_html=True)
    
    campaigns_response = make_api_request("/campaigns/")
    
    if "error" not in campaigns_response:
        if campaigns_response:
            df = pd.DataFrame(campaigns_response)
            df['created_at'] = pd.to_datetime(df['created_at']).dt.strftime('%Y-%m-%d %H:%M')
            df['updated_at'] = pd.to_datetime(df['updated_at']).dt.strftime('%Y-%m-%d %H:%M')
            
            st.dataframe(
                df[['campaign_id', 'campaign_name', 'created_at', 'updated_at']],
                use_container_width=True,
                hide_index=True
            )
            
            # Campaign actions
            selected_campaign = st.selectbox("Select Campaign for Actions", 
                                           options=[c['campaign_name'] for c in campaigns_response])
            
            # Campaign Update Section
            st.markdown('<h4 class="section-header">⚙️ Update Campaign Settings</h4>', unsafe_allow_html=True)
            
            with st.form("update_campaign"):
                campaign_to_update = st.selectbox("Select Campaign to Update", 
                                               options=[c['campaign_name'] for c in campaigns_response])
                
                # Get campaign details
                campaign_to_update_id = next(c['campaign_id'] for c in campaigns_response if c['campaign_name'] == campaign_to_update)
                campaign_to_update_details = next(c for c in campaigns_response if c['campaign_id'] == campaign_to_update_id)
                
                # Update fields
                new_custom_subject = st.text_input("Custom Subject", value=campaign_to_update_details.get('custom_subject', ''))
                new_custom_message = st.text_area("Custom Message", value=campaign_to_update_details.get('custom_message', ''))
                
                # Template selection
                use_custom_template = st.checkbox("Use Custom Template for this Campaign", 
                                                value=campaign_to_update_details.get('use_custom_template', False))
                
                if use_custom_template:
                    templates_response = make_api_request("/templates/")
                    if "error" not in templates_response:
                        template_options = {t["name"]: t["template_id"] for t in templates_response}
                        
                        # Show current template if assigned
                        current_template_id = campaign_to_update_details.get('custom_template_id')
                        current_template_name = None
                        
                        if current_template_id:
                            for template in templates_response:
                                if template['template_id'] == current_template_id:
                                    current_template_name = template['name']
                                    break
                        
                        if current_template_name and current_template_name in template_options:
                            selected_template = st.selectbox(
                                "Select Custom Template for Campaign", 
                                list(template_options.keys()),
                                index=list(template_options.keys()).index(current_template_name)
                            )
                        else:
                            selected_template = st.selectbox("Select Custom Template for Campaign", list(template_options.keys()))
                    else:
                        st.warning("Could not load templates")
                        use_custom_template = False
                
                if st.form_submit_button("Update Campaign Settings"):
                    update_data = {
                        "custom_subject": new_custom_subject,
                        "custom_message": new_custom_message,
                        "use_custom_template": use_custom_template
                    }
                    
                    if use_custom_template:
                        update_data["template_id"] = template_options[selected_template]
                    
                    response = make_api_request(f"/campaigns/template-update/?campaign_id={campaign_to_update_id}", method="POST", data=update_data)
                    
                    if "error" not in response:
                        st.success(f"Campaign '{campaign_to_update}' updated successfully!")
                    else:
                        st.error(response["error"])
            
            # Quick actions
            col1, col2, col3 = st.columns(3)
            
            with col1:
                if st.button("🗑️ Delete Campaign"):
                    st.warning("Delete functionality coming soon!")
            
            with col2:
                if st.button("📊 View Details"):
                    st.info("Detailed view coming soon!")
            
            with col3:
                if st.button("📤 Send Emails"):
                    st.info("Go to the 'Send Emails' page to send emails for this campaign!")
        else:
            st.info("No campaigns found. Create your first campaign above!")
    else:
        st.error(campaigns_response["error"])

def show_templates():
    st.markdown('<h2 class="section-header">🎨 Template Management</h2>', unsafe_allow_html=True)
    
    # Create new template
    with st.expander("➕ Create New Template", expanded=True):
        with st.form("create_template"):
            template_name = st.text_input("Template Name", placeholder="Enter template name")
            description = st.text_area("Description", placeholder="Enter template description")
            subject = st.text_input("Default Subject", placeholder="Enter default subject line")
            
            # HTML Content Editor
            st.subheader("HTML Content")
            html_content = st.text_area(
                "HTML Content",
                height=300,
                placeholder="""<!DOCTYPE html>
<html>
<head>
    <title>Email Template</title>
</head>
<body>
    <h1>Hello {{ name }}!</h1>
    <p>{{ message }}</p>
</body>
</html>"""
            )
            
            # CSS Styles
            css_styles = st.text_area(
                "CSS Styles (Optional)",
                height=150,
                placeholder="body { font-family: Arial, sans-serif; }"
            )
            
            is_active = st.checkbox("Active", value=True)
            
            # Template Variables
            st.subheader("Template Variables")
            variables = []
            
            num_variables = st.number_input("Number of Variables", min_value=0, max_value=10, value=0)
            
            for i in range(num_variables):
                with st.container():
                    col1, col2 = st.columns(2)
                    with col1:
                        var_name = st.text_input(f"Variable Name {i+1}", key=f"var_name_{i}")
                        var_type = st.selectbox(f"Type {i+1}", ["text", "email", "url", "date", "number"], key=f"var_type_{i}")
                    with col2:
                        display_name = st.text_input(f"Display Name {i+1}", key=f"display_name_{i}")
                        is_required = st.checkbox(f"Required {i+1}", value=True, key=f"required_{i}")
                    
                    default_value = st.text_input(f"Default Value {i+1} (Optional)", key=f"default_value_{i}")
                    description = st.text_input(f"Description {i+1} (Optional)", key=f"description_{i}")
                    
                    if var_name and display_name:
                        variables.append({
                            "variable_name": var_name,
                            "display_name": display_name,
                            "variable_type": var_type,
                            "is_required": is_required,
                            "default_value": default_value,
                            "description": description
                        })
            
            submitted = st.form_submit_button("Create Template")
            
            if submitted and template_name and html_content:
                template_data = {
                    "name": template_name,
                    "description": description,
                    "subject": subject,
                    "html_content": html_content,
                    "css_styles": css_styles,
                    "is_active": is_active,
                    "variables": variables
                }
                
                response = make_api_request("/templates/create/", method="POST", data=template_data)
                
                if "error" not in response:
                    st.success(f"Template '{template_name}' created successfully!")
                    st.balloons()
                else:
                    st.error(response["error"])
    
    # List existing templates
    st.markdown('<h3 class="section-header">📋 Existing Templates</h3>', unsafe_allow_html=True)
    
    templates_response = make_api_request("/templates/")
    
    if "error" not in templates_response:
        if templates_response:
            # Create tabs for different views
            tab1, tab2 = st.tabs(["Table View", "Card View"])
            
            with tab1:
                df = pd.DataFrame(templates_response)
                df['created_at'] = pd.to_datetime(df['created_at']).dt.strftime('%Y-%m-%d %H:%M')
                df['variables_count'] = df['template_variables'].apply(len)
                
                st.dataframe(
                    df[['template_id', 'name', 'description', 'is_active', 'variables_count', 'created_at']],
                    use_container_width=True,
                    hide_index=True
                )
            
            with tab2:
                cols = st.columns(3)
                for i, template in enumerate(templates_response):
                    with cols[i % 3]:
                        with st.container():
                            st.markdown(f"""
                            <div style="border: 1px solid #ddd; padding: 1rem; border-radius: 5px; margin: 0.5rem 0;">
                                <h4>{template['name']}</h4>
                                <p><strong>ID:</strong> {template['template_id']}</p>
                                <p><strong>Status:</strong> {'✅ Active' if template['is_active'] else '❌ Inactive'}</p>
                                <p><strong>Variables:</strong> {len(template['template_variables'])}</p>
                                <p><strong>Created:</strong> {template['created_at'][:10]}</p>
                            </div>
                            """, unsafe_allow_html=True)
                            
                            if st.button(f"Preview {template['name']}", key=f"preview_{template['template_id']}"):
                                show_template_preview(template)
            
            # Template actions
            selected_template = st.selectbox("Select Template for Actions", 
                                           options=[t['name'] for t in templates_response])
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                if st.button("👁️ Preview Template"):
                    selected_template_data = next(t for t in templates_response if t['name'] == selected_template)
                    show_template_preview(selected_template_data)
            
            with col2:
                if st.button("✏️ Edit Template"):
                    st.info("Edit functionality coming soon!")
            
            with col3:
                if st.button("🗑️ Delete Template"):
                    st.warning("Delete functionality coming soon!")
        else:
            st.info("No templates found. Create your first template above!")
    else:
        st.error(templates_response["error"])

def show_template_preview(template):
    st.markdown('<h3 class="section-header">👁️ Template Preview</h3>', unsafe_allow_html=True)
    
    # Sample data input
    st.subheader("Sample Data")
    
    sample_data = {}
    for var in template['template_variables']:
        if var['variable_type'] == 'text':
            sample_data[var['variable_name']] = st.text_input(
                f"{var['display_name']} ({var['variable_name']})",
                value=var.get('default_value', ''),
                key=f"preview_{var['variable_name']}"
            )
        elif var['variable_type'] == 'email':
            sample_data[var['variable_name']] = st.text_input(
                f"{var['display_name']} ({var['variable_name']})",
                value=var.get('default_value', ''),
                key=f"preview_{var['variable_name']}"
            )
        elif var['variable_type'] == 'url':
            sample_data[var['variable_name']] = st.text_input(
                f"{var['display_name']} ({var['variable_name']})",
                value=var.get('default_value', ''),
                key=f"preview_{var['variable_name']}"
            )
    
    if st.button("Generate Preview"):
        preview_data = {
            "template_id": template['template_id'],
            "sample_data": sample_data
        }
        
        response = make_api_request("/templates/preview/", method="POST", data=preview_data)
        
        if "error" not in response:
            st.subheader("Preview Result")
            
            # Display rendered HTML
            st.markdown("**Rendered HTML:**")
            st.code(response['html_content'], language='html')
            
            # Display in iframe (if possible)
            try:
                html_content = response['html_content']
                st.markdown("**Live Preview:**")
                st.components.v1.html(html_content, height=400, scrolling=True)
            except Exception as e:
                st.warning(f"Could not render live preview: {str(e)}")
        else:
            st.error(response["error"])

def show_email_management():
    st.markdown('<h2 class="section-header">📧 Email Management</h2>', unsafe_allow_html=True)
    
    # Upload emails
    st.markdown('<h3 class="section-header">📤 Upload Emails</h3>', unsafe_allow_html=True)
    st.subheader("Upload Excel File")
    
    # Get campaigns for selection
    campaigns_response = make_api_request("/campaigns/")
    
    if "error" not in campaigns_response and campaigns_response:
        campaign_options = {c['campaign_name']: c['campaign_id'] for c in campaigns_response}
        selected_campaign = st.selectbox("Select Campaign", list(campaign_options.keys()))
        
        uploaded_file = st.file_uploader(
            "Choose an Excel file",
            type=['xlsx', 'xls', 'csv'],
            help="File should contain 'name' and 'email_address' columns"
        )
        
        if uploaded_file is not None and st.button("Upload Emails"):
            try:
                # Prepare the file for upload
                files = {'file': (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)}
                campaign_id = campaign_options[selected_campaign]
                
                # Make the API request
                response = make_api_request(
                    f"/upload-xls/?campaign_id={campaign_id}",
                    method="POST",
                    files=files
                )
                
                if "error" not in response:
                    st.success(f"✅ {response.get('message', 'Emails uploaded successfully!')}")
                    st.info(f"📁 File: {uploaded_file.name}")
                    st.info(f"🎯 Campaign: {selected_campaign}")
                else:
                    st.error(f"❌ Upload failed: {response['error']}")
                    
            except Exception as e:
                st.error(f"❌ Upload failed: {str(e)}")
                st.info("💡 Make sure your Excel file has 'name' and 'email_address' columns")
    else:
        st.warning("No campaigns available. Please create a campaign first.")
    
    # List emails
    st.markdown('<h3 class="section-header">📋 Email Lists</h3>', unsafe_allow_html=True)
    
    campaigns_response = make_api_request("/campaigns/")
    
    if "error" not in campaigns_response and campaigns_response:
        selected_campaign = st.selectbox("Select Campaign to View Emails", 
                                       options=[c['campaign_name'] for c in campaigns_response])
        
        if st.button("Load Emails"):
            campaign_id = next(c['campaign_id'] for c in campaigns_response if c['campaign_name'] == selected_campaign)
            emails_response = make_api_request(f"/list-emails/?campaign_id={campaign_id}")
            
            if "error" not in emails_response:
                if emails_response:
                    df = pd.DataFrame(emails_response)
                    df['added_at'] = pd.to_datetime(df['added_at']).dt.strftime('%Y-%m-%d %H:%M')
                    
                    st.dataframe(
                        df[['email_id', 'name', 'email_address', 'added_at']],
                        use_container_width=True,
                        hide_index=True
                    )
                    
                    st.success(f"Found {len(emails_response)} emails for campaign '{selected_campaign}'")
                else:
                    st.info(f"No emails found for campaign '{selected_campaign}'")
            else:
                st.error(emails_response["error"])
    else:
        st.info("No campaigns available. Please create a campaign first.")

def show_send_emails():
    st.markdown('<h2 class="section-header">📤 Send Emails</h2>', unsafe_allow_html=True)
    
    # Get campaigns
    campaigns_response = make_api_request("/campaigns/")
    
    if "error" not in campaigns_response and campaigns_response:
        with st.form("send_emails"):
            st.subheader("Campaign Selection")
            
            campaign_options = {c['campaign_name']: c['campaign_id'] for c in campaigns_response}
            selected_campaign = st.selectbox("Select Campaign", list(campaign_options.keys()))
            
            # Get campaign details
            campaign_id = campaign_options[selected_campaign]
            campaign_details = next(c for c in campaigns_response if c['campaign_id'] == campaign_id)
            
            st.subheader("Email Settings")
            
            # Template selection
            use_custom_template = st.checkbox("Use Custom Template", value=campaign_details.get('use_custom_template', False))
            
            if use_custom_template:
                templates_response = make_api_request("/templates/")
                if "error" not in templates_response:
                    template_options = {t["name"]: t["template_id"] for t in templates_response}
                    
                    # If campaign has a custom template assigned, show it as default
                    current_template_id = campaign_details.get('custom_template_id')
                    current_template_name = None
                    
                    if current_template_id:
                        for template in templates_response:
                            if template['template_id'] == current_template_id:
                                current_template_name = template['name']
                                break
                    
                    # Show current template if available, otherwise show all templates
                    if current_template_name and current_template_name in template_options:
                        st.info(f"📋 Current template: {current_template_name}")
                        selected_template = st.selectbox(
                            "Select Custom Template", 
                            list(template_options.keys()),
                            index=list(template_options.keys()).index(current_template_name)
                        )
                    else:
                        selected_template = st.selectbox("Select Custom Template", list(template_options.keys()))
                else:
                    st.warning("Could not load templates")
                    use_custom_template = False
            else:
                # Legacy template selection
                template_options = {
                    "AutoSAD v1": "1",
                    "AutoSAD v2": "3", 
                    "AutoSAD v3": "4",
                    "XCV AI": "2"
                }
                selected_template = st.selectbox("Select Default Template", list(template_options.keys()))
            
            # Custom message
            custom_message = st.text_area(
                "Custom Message",
                value=campaign_details.get('custom_message', ''),
                placeholder="Enter custom message for this campaign"
            )
            
            # Custom subject
            custom_subject = st.text_input(
                "Custom Subject",
                value=campaign_details.get('custom_subject', ''),
                placeholder="Enter custom subject line"
            )
            
            # Preview and send
            col1, col2 = st.columns(2)
            
            with col1:
                if st.form_submit_button("👁️ Preview"):
                    st.info("Preview functionality coming soon!")
            
            with col2:
                if st.form_submit_button("📤 Send Emails"):
                    campaign_id = campaign_options[selected_campaign]
                    
                    email_data = {
                        "message": custom_message,
                        "subject": custom_subject,
                        "use_custom_template": use_custom_template
                    }
                    
                    if use_custom_template:
                        email_data["template_id"] = template_options[selected_template]
                    else:
                        email_data["email_template"] = template_options[selected_template]
                    
                    response = make_api_request(
                        f"/campaigns/send-enhanced/?campaign_id={campaign_id}",
                        method="POST",
                        data=email_data
                    )
                    
                    if "error" not in response:
                        st.success("Emails sent successfully!")
                        st.json(response)
                    else:
                        st.error(response["error"])
    else:
        st.warning("No campaigns available. Please create a campaign first.")

def show_analytics():
    st.markdown('<h2 class="section-header">📊 Analytics</h2>', unsafe_allow_html=True)
    
    st.info("Analytics dashboard coming soon! This will include:")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **Campaign Analytics:**
        - Email delivery rates
        - Open rates
        - Click rates
        - Bounce rates
        - Unsubscribe rates
        """)
    
    with col2:
        st.markdown("""
        **Template Performance:**
        - Template usage statistics
        - A/B test results
        - Performance comparisons
        - Engagement metrics
        """)
    
    # Placeholder charts
    st.subheader("Sample Analytics")
    
    # Mock data for demonstration
    campaign_data = {
        'Campaign': ['Welcome Campaign', 'Newsletter', 'Promotional'],
        'Sent': [100, 150, 200],
        'Delivered': [95, 142, 185],
        'Opened': [45, 67, 89],
        'Clicked': [12, 23, 34]
    }
    
    df = pd.DataFrame(campaign_data)
    
    # Delivery rate chart
    fig1 = px.bar(df, x='Campaign', y=['Sent', 'Delivered', 'Opened', 'Clicked'],
                  title="Campaign Performance",
                  barmode='group')
    st.plotly_chart(fig1, use_container_width=True)
    
    # Engagement rate chart
    df['Open Rate'] = (df['Opened'] / df['Delivered'] * 100).round(2)
    df['Click Rate'] = (df['Clicked'] / df['Opened'] * 100).round(2)
    
    fig2 = px.line(df, x='Campaign', y=['Open Rate', 'Click Rate'],
                   title="Engagement Rates (%)")
    st.plotly_chart(fig2, use_container_width=True)

if __name__ == "__main__":
    main() 