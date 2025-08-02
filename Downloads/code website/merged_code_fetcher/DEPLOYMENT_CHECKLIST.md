# Deployment Checklist for Render.com

## Pre-Deployment Setup

### 1. Repository Setup
- [ ] Fork/clone the repository to your GitHub account
- [ ] Ensure all files are committed and pushed to GitHub
- [ ] Verify `.gitignore` excludes sensitive files (.env, *.db, etc.)

### 2. Environment Variables Setup
Prepare these environment variables for Render.com:

#### Required Variables:
- [ ] `SECRET_KEY` - Generate a secure random key
- [ ] `FLASK_ENV` - Set to `production`
- [ ] `EMAIL_ACCOUNT` - Your Gmail address
- [ ] `EMAIL_PASSWORD` - Your Gmail app password (not regular password)

#### Optional Variables:
- [ ] `IMAP_SERVER` - Default: `imap.gmail.com`
- [ ] `ADMIN_USERNAME` - Default: `admin`
- [ ] `ADMIN_PASSWORD` - Default: `admin123` (change this!)
- [ ] `EMAIL_ACCOUNT_2` - Secondary email account (optional)
- [ ] `EMAIL_PASSWORD_2` - Secondary email password (optional)
- [ ] `IMAP_SERVER_2` - Secondary IMAP server (optional)

### 3. Gmail Setup
- [ ] Enable 2-Factor Authentication on Gmail
- [ ] Generate App Password:
  1. Go to Google Account settings
  2. Security → 2-Step Verification → App passwords
  3. Generate password for "Mail"
  4. Use this password in `EMAIL_PASSWORD`

## Render.com Deployment

### Option 1: Using render.yaml (Recommended)

1. **Create New Service**
   - [ ] Go to [Render.com](https://render.com) dashboard
   - [ ] Click "New" → "Blueprint"
   - [ ] Connect your GitHub repository
   - [ ] Render will detect `render.yaml` automatically

2. **Configure Environment Variables**
   - [ ] Add all required environment variables listed above
   - [ ] Ensure `DATABASE_URL` is automatically set by Render

3. **Deploy**
   - [ ] Click "Apply" to start deployment
   - [ ] Wait for database and web service to be created
   - [ ] Monitor deployment logs for any errors

### Option 2: Manual Setup

1. **Create PostgreSQL Database**
   - [ ] New → PostgreSQL
   - [ ] Choose a name (e.g., `code-fetcher-db`)
   - [ ] Note the connection string

2. **Create Web Service**
   - [ ] New → Web Service
   - [ ] Connect GitHub repository
   - [ ] Configure:
     - Build Command: `pip install -r requirements.txt`
     - Start Command: `gunicorn --bind 0.0.0.0:$PORT app:app`
   - [ ] Add all environment variables (including `DATABASE_URL`)

## Post-Deployment Verification

### 1. Application Health Check
- [ ] Visit your Render app URL
- [ ] Verify main page loads correctly
- [ ] Test Netflix and ChatGPT pages load
- [ ] Check admin panel login works

### 2. Database Verification
- [ ] Confirm database tables are created
- [ ] Verify admin user is created
- [ ] Check sample API keys are generated

### 3. API Testing
- [ ] Test API key validation endpoint
- [ ] Test code fetching (may show email config errors if not set up)
- [ ] Verify usage logging works

### 4. Admin Panel Testing
- [ ] Login to admin panel
- [ ] Create new API keys
- [ ] View usage statistics
- [ ] Test key management features

## Troubleshooting

### Common Issues:

1. **Build Failures**
   - Check requirements.txt for correct package versions
   - Verify Python version compatibility
   - Review build logs in Render dashboard

2. **Database Connection Errors**
   - Ensure DATABASE_URL is correctly set
   - Verify PostgreSQL service is running
   - Check database connection string format

3. **Email Configuration Errors**
   - Verify Gmail app password is correct
   - Check IMAP server settings
   - Ensure 2FA is enabled on Gmail account

4. **Admin Login Issues**
   - Check ADMIN_USERNAME and ADMIN_PASSWORD variables
   - Clear browser cache
   - Verify database initialization completed

### Monitoring:
- [ ] Set up Render monitoring/alerts
- [ ] Monitor application logs regularly
- [ ] Check database usage and limits
- [ ] Monitor API usage patterns

## Security Considerations

- [ ] Change default admin password
- [ ] Use strong SECRET_KEY
- [ ] Regularly rotate email passwords
- [ ] Monitor API key usage for abuse
- [ ] Set up proper logging and monitoring
- [ ] Consider rate limiting for production use

## Maintenance

- [ ] Regular database backups
- [ ] Monitor email account quotas
- [ ] Update dependencies periodically
- [ ] Review and clean up old API keys
- [ ] Monitor application performance

---

## Quick Commands

### Generate Secret Key:
```python
import secrets
print(secrets.token_hex(32))
```

### Test Database Connection:
```bash
# In Render shell
python -c "from app import app; from database import db; app.app_context().push(); print('DB connection:', db.engine.url)"
```

### Check Environment Variables:
```bash
# In Render shell
python -c "import os; print('EMAIL_ACCOUNT:', bool(os.getenv('EMAIL_ACCOUNT')))"
