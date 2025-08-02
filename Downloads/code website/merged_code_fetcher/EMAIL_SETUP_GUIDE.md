# 📧 Email Setup Guide

## Quick Setup Instructions

You now have a simplified email reader that works with both **Gmail** and **Outlook** accounts. Follow these steps to configure it:

### Step 1: Edit email_reader.py

Open `merged_code_fetcher/email_reader.py` and update the email configuration at the top:

```python
self.email_accounts = [
    {
        "email": "your-outlook@outlook.com",      # Replace with your Outlook email
        "password": "your-outlook-app-password",  # Replace with Outlook App Password
        "provider": "outlook",
        "imap_server": "outlook.office365.com",
        "imap_port": 993,
        "folders": ["INBOX", "Junk Email", "Deleted Items"]
    },
    {
        "email": "your-gmail@gmail.com",          # Replace with your Gmail email
        "password": "your-gmail-app-password",    # Replace with Gmail App Password
        "provider": "gmail",
        "imap_server": "imap.gmail.com",
        "imap_port": 993,
        "folders": ["INBOX", "[Gmail]/Spam", "[Gmail]/All Mail"]
    }
]
```

### Step 2: Generate App Passwords

#### For Outlook:
1. Go to https://account.microsoft.com/security
2. Enable 2-Factor Authentication (if not already enabled)
3. Click "Advanced security options"
4. Click "Create a new app password"
5. Copy the 16-character password (example: `abcd efgh ijkl mnop`)

#### For Gmail:
1. Go to https://myaccount.google.com/apppasswords
2. Enable 2-Factor Authentication (if not already enabled)
3. Select "Mail" as the app
4. Copy the 16-character password

### Step 3: Update the Configuration

Replace the placeholder values:

```python
# Example configuration:
self.email_accounts = [
    {
        "email": "john@outlook.com",              # Your actual Outlook email
        "password": "abcd efgh ijkl mnop",        # Your actual Outlook App Password
        "provider": "outlook",
        "imap_server": "outlook.office365.com",
        "imap_port": 993,
        "folders": ["INBOX", "Junk Email", "Deleted Items"]
    },
    {
        "email": "john@gmail.com",                # Your actual Gmail email
        "password": "wxyz 1234 5678 9012",       # Your actual Gmail App Password
        "provider": "gmail",
        "imap_server": "imap.gmail.com",
        "imap_port": 993,
        "folders": ["INBOX", "[Gmail]/Spam", "[Gmail]/All Mail"]
    }
]
```

### Step 4: Test the Setup

Run the Flask application:

```bash
cd merged_code_fetcher
python app.py
```

Then test the Netflix code fetching:
1. Go to http://localhost:5000/netflix
2. Enter a valid API key
3. Click "Get Netflix Code"

### Step 5: Check Console Output

The system will now:
- ✅ Try both email accounts automatically
- 🔍 Search in multiple folders (INBOX, Spam, Junk)
- 📧 Look for Netflix emails with 4-digit codes
- 🎯 Return the first code found

## How It Works

1. **Multiple Account Support**: The system tries both Gmail and Outlook accounts
2. **Smart Folder Search**: Checks INBOX, spam, and junk folders
3. **Netflix Detection**: Looks for emails from Netflix with 4-digit verification codes
4. **ChatGPT Support**: Also searches for 6-digit ChatGPT codes
5. **Detailed Logging**: Shows exactly what it's doing in the console

## Troubleshooting

### "Authentication Failed" Error
- Make sure you're using **App Passwords**, not regular passwords
- Verify 2-Factor Authentication is enabled
- Double-check the email address and password

### "No Netflix Codes Found"
- Make sure you have recent Netflix emails with 4-digit codes
- Check that the emails are from netflix.com domains
- Try requesting a new Netflix verification code

### Connection Issues
- Check your internet connection
- Verify IMAP is enabled for your email provider
- Try with just one email account first

## Benefits of This Setup

✅ **No Database Required**: All credentials are hardcoded in the file
✅ **Multiple Providers**: Works with both Gmail and Outlook
✅ **Automatic Fallback**: Tries all accounts until it finds a code
✅ **Comprehensive Search**: Checks multiple folders including spam
✅ **Easy Configuration**: Just update the credentials in one place

---

**That's it!** Your Netflix code fetching should now work with both Gmail and Outlook accounts.
