# Email Code Fetching Troubleshooting Guide

## Issue: Netflix verification codes not showing up after adding Outlook email account

### Most Common Causes & Solutions:

## 1. **Check if Email Account is Actually Added**

First, verify that your email account was successfully added to the database:

```bash
cd merged_code_fetcher
python -c "
from flask import Flask
from database import db, init_db, EmailAccount
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///instance/code_fetcher.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
init_db(app)
with app.app_context():
    accounts = EmailAccount.query.all()
    print(f'Total email accounts: {len(accounts)}')
    for account in accounts:
        print(f'- {account.email} ({account.provider}) - Active: {account.is_active}')
"
```

**If no accounts are shown:** The email account wasn't saved properly. Try adding it again through the admin panel.

## 2. **Outlook/Hotmail Authentication Issues**

Outlook requires **App Passwords** instead of regular passwords for IMAP access.

### Steps to fix Outlook authentication:

1. **Enable 2-Factor Authentication** on your Microsoft account
2. **Generate an App Password:**
   - Go to https://account.microsoft.com/security
   - Click "Advanced security options"
   - Click "Create a new app password"
   - Copy the generated password (16 characters, no spaces)
3. **Update your email account** in the admin panel with the App Password (not your regular password)

## 3. **Test Email Connection**

Run this test to check if the email connection works:

```bash
cd merged_code_fetcher
python debug_email.py
```

This will show:
- How many email accounts are configured
- Whether the Flask context is working
- Any connection errors

## 4. **Check for Recent Netflix Emails**

The system only looks for **recent** Netflix emails. Make sure you have:

1. **Recent Netflix verification emails** in your inbox
2. **Emails from Netflix** (from netflix.com or noreply@account.netflix.com)
3. **4-digit verification codes** in the email content

## 5. **Manual Test of Netflix Code Fetching**

Test the Netflix code fetching manually:

```bash
cd merged_code_fetcher
python -c "
from flask import Flask
from database import db, init_db
from email_reader import get_latest_netflix_code
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///instance/code_fetcher.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
init_db(app)
with app.app_context():
    result = get_latest_netflix_code()
    print('Netflix code result:', result)
"
```

## 6. **Common Error Messages & Solutions**

### "Error: No email accounts configured"
- **Solution:** Add email accounts through the admin panel at `/admin/email-accounts`

### "Failed to connect to [email]: [535] authentication failed"
- **Solution:** Use App Password for Outlook/Hotmail accounts
- **Solution:** Enable "Less secure app access" for Gmail (not recommended)
- **Solution:** Use OAuth2 for Gmail (recommended)

### "No recent Netflix verification codes found"
- **Solution:** Make sure you have recent Netflix emails with 4-digit codes
- **Solution:** Check spam/junk folders
- **Solution:** Try requesting a new Netflix verification code

### "Flask context error"
- **Solution:** Restart the Flask application
- **Solution:** Check that the app is running properly

## 7. **Step-by-Step Debugging Process**

1. **Verify Flask app is running:**
   ```bash
   cd merged_code_fetcher
   python app.py
   ```

2. **Check admin panel access:**
   - Go to http://localhost:5000/admin/login
   - Login with admin/admin123
   - Go to "Email Accounts" section

3. **Add/verify email account:**
   - Email: your-outlook-email@outlook.com
   - Password: **App Password** (16 characters from Microsoft)
   - Provider: Outlook

4. **Test Netflix code fetching:**
   - Go to http://localhost:5000/netflix
   - Enter a valid API key
   - Click "Get Netflix Code"

5. **Check console output:**
   - Look at the terminal where you ran `python app.py`
   - Check for debug messages about email accounts and connections

## 8. **Gmail-Specific Instructions**

If using Gmail instead of Outlook:

1. **Enable 2-Factor Authentication**
2. **Generate App Password:**
   - Go to Google Account settings
   - Security → 2-Step Verification → App passwords
   - Generate password for "Mail"
3. **Use the App Password** in the admin panel

## 9. **Hostinger Mail Instructions**

For Hostinger email accounts:
- Use your full email address as username
- Use your email password
- IMAP server: imap.hostinger.com (port 993)

## 10. **Still Not Working?**

If none of the above solutions work:

1. **Check the Flask application logs** for detailed error messages
2. **Verify your email provider allows IMAP access**
3. **Test with a different email provider** (Gmail, Outlook)
4. **Check firewall/antivirus** blocking IMAP connections
5. **Try with a fresh Netflix verification email**

## Quick Fix Checklist:

- [ ] Email account added to admin panel
- [ ] Using App Password (not regular password) for Outlook
- [ ] Email account is marked as "Active"
- [ ] Recent Netflix emails exist in the account
- [ ] Flask application is running without errors
- [ ] API key is valid and has remaining uses
- [ ] IMAP access is enabled for the email provider

---

**Need more help?** Check the console output when running the Flask app for detailed error messages.
