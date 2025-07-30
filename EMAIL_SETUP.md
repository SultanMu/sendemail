# 📧 Email Configuration Guide

## 🔧 Quick Fix for Email Authentication Error

The error you're seeing is because the email credentials are not properly configured. Here's how to fix it:

### **Step 1: Test Current Configuration**

Run the email test script:
```bash
python test_email_config.py
```

### **Step 2: Configure Email Settings**

#### **For Gmail (Recommended):**

1. **Enable 2-Factor Authentication:**
   - Go to https://myaccount.google.com/security
   - Enable 2-Step Verification

2. **Generate App Password:**
   - Go to https://myaccount.google.com/apppasswords
   - Select "Mail" and generate a password
   - Copy the 16-character password

3. **Set Environment Variables:**
   ```bash
   EMAIL_HOST=smtp.gmail.com
   EMAIL_HOST_USER=your_email@gmail.com
   EMAIL_HOST_PASSWORD=your_16_character_app_password
   ```

#### **For Office 365:**

```bash
EMAIL_HOST=smtp.office365.com
EMAIL_HOST_USER=your_email@domain.com
EMAIL_HOST_PASSWORD=your_password
```

### **Step 3: Update Docker Environment**

#### **Option A: Update docker-compose.yml**

Add these environment variables to the `app` service in `docker-compose.yml`:

```yaml
app:
  # ... existing config ...
  environment:
    # ... existing variables ...
    EMAIL_HOST: smtp.gmail.com
    EMAIL_HOST_USER: your_email@gmail.com
    EMAIL_HOST_PASSWORD: your_app_password
```

#### **Option B: Create .env file**

Create a `.env` file in your project root:

```env
EMAIL_HOST=smtp.gmail.com
EMAIL_HOST_USER=your_email@gmail.com
EMAIL_HOST_PASSWORD=your_app_password
```

### **Step 4: Restart the Application**

```bash
# Stop containers
docker-compose down

# Start with new configuration
docker-compose up -d
```

### **Step 5: Test Email Sending**

1. Go to Streamlit app: http://localhost:8501
2. Navigate to "Send Emails"
3. Try sending a test email

## 🔍 Troubleshooting

### **Common Issues:**

1. **"Username and Password not accepted"**
   - Use App Password for Gmail (not regular password)
   - Check if 2FA is enabled
   - Verify email address is correct

2. **"Connection refused"**
   - Check if EMAIL_HOST is correct
   - Try different ports (587 for TLS, 465 for SSL)

3. **"Authentication failed"**
   - Double-check email and password
   - Ensure no extra spaces in environment variables

### **Alternative Email Providers:**

| Provider | EMAIL_HOST | Port | Notes |
|----------|------------|------|-------|
| Gmail | smtp.gmail.com | 587 | Requires App Password |
| Outlook | smtp-mail.outlook.com | 587 | Use regular password |
| Yahoo | smtp.mail.yahoo.com | 587 | Requires App Password |
| Office 365 | smtp.office365.com | 587 | Use regular password |

## 🚀 Quick Test

After configuration, test with:

```bash
# Test email configuration
python test_email_config.py

# If successful, try sending emails from the app
```

## 📝 Example Configuration

**For Gmail:**
```env
EMAIL_HOST=smtp.gmail.com
EMAIL_HOST_USER=myemail@gmail.com
EMAIL_HOST_PASSWORD=abcd efgh ijkl mnop
```

**For Office 365:**
```env
EMAIL_HOST=smtp.office365.com
EMAIL_HOST_USER=myemail@company.com
EMAIL_HOST_PASSWORD=mypassword123
```

---

**Need help?** Run `python test_email_config.py` for detailed diagnostics and setup instructions. 