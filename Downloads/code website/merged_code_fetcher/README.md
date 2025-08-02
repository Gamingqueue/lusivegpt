# Code Fetcher - Netflix & ChatGPT Verification Code Service

A Flask web application that automatically fetches verification codes from Netflix and ChatGPT emails and provides them through a secure API with key-based authentication.

## Features

- 🔐 **Secure API Key System** - Generate and manage API keys with usage limits
- 📧 **Email Integration** - Automatically fetch codes from Gmail and other IMAP servers
- 🎯 **Multi-Service Support** - Support for Netflix and ChatGPT verification codes
- 👨‍💼 **Admin Dashboard** - Complete admin panel for key management and analytics
- 📊 **Usage Analytics** - Track API usage with detailed logs and statistics
- 🚀 **Production Ready** - Configured for deployment on Render.com

## Quick Start

### Local Development

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd merged_code_fetcher
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

5. **Run the application**
   ```bash
   python app.py
   ```

The application will be available at `http://localhost:5000`

### Deploy to Render.com

#### Option 1: Using render.yaml (Recommended)

1. **Fork this repository** to your GitHub account

2. **Connect to Render.com**
   - Go to [Render.com](https://render.com)
   - Connect your GitHub account
   - Create a new service from your forked repository

3. **Configure Environment Variables**
   Set these environment variables in Render dashboard:
   ```
   SECRET_KEY=your-secret-key-here
   FLASK_ENV=production
   EMAIL_ACCOUNT=your-email@gmail.com
   EMAIL_PASSWORD=your-app-password
   IMAP_SERVER=imap.gmail.com
   ADMIN_USERNAME=admin
   ADMIN_PASSWORD=your-secure-password
   ```

4. **Deploy**
   - Render will automatically detect the `render.yaml` file
   - It will create a PostgreSQL database and web service
   - The app will be deployed automatically

#### Option 2: Manual Setup

1. **Create PostgreSQL Database**
   - In Render dashboard, create a new PostgreSQL database
   - Note the connection string

2. **Create Web Service**
   - Create a new web service
   - Connect your GitHub repository
   - Set build command: `pip install -r requirements.txt`
   - Set start command: `gunicorn --bind 0.0.0.0:$PORT app:app`

3. **Configure Environment Variables**
   Add all the environment variables listed above, plus:
   ```
   DATABASE_URL=your-postgresql-connection-string
   ```

## Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `SECRET_KEY` | Flask secret key for sessions | `dev-secret-key-change-in-production` |
| `FLASK_ENV` | Environment (development/production) | `development` |
| `DATABASE_URL` | Database connection string | `sqlite:///code_fetcher.db` |
| `EMAIL_ACCOUNT` | Email account for fetching codes | Required |
| `EMAIL_PASSWORD` | Email app password | Required |
| `IMAP_SERVER` | IMAP server address | `imap.gmail.com` |
| `ADMIN_USERNAME` | Admin panel username | `admin` |
| `ADMIN_PASSWORD` | Admin panel password | `admin123` |

### Email Setup

For Gmail:
1. Enable 2-factor authentication
2. Generate an app password
3. Use the app password in `EMAIL_PASSWORD`

## API Usage

### Get Verification Code

```bash
POST /get-code
Content-Type: application/json

{
  "key": "your-api-key",
  "service": "netflix"  // or "chatgpt"
}
```

**Response:**
```json
{
  "code": "1234",
  "success": true,
  "remaining_uses": 4
}
```

### Validate API Key

```bash
POST /validate-key
Content-Type: application/json

{
  "key": "your-api-key",
  "service": "netflix"
}
```

**Response:**
```json
{
  "valid": true,
  "message": "Valid key - 5 uses remaining",
  "remaining_uses": 5,
  "service_type": "both"
}
```

## Admin Panel

Access the admin panel at `/admin` with your configured credentials.

Features:
- 📊 Dashboard with usage statistics
- 🔑 API key management (create, edit, delete)
- 📈 Usage analytics and logs
- ⚙️ Settings and configuration
- 👥 Bulk key operations

## Security Features

- 🔐 Secure password hashing
- 🛡️ Session protection
- 🚫 Rate limiting through usage limits
- 📝 Comprehensive audit logging
- 🔒 Environment-based configuration

## Database Schema

- **AdminUser**: Admin panel users
- **ApiKey**: API keys with usage limits and service restrictions
- **UsageLog**: Detailed usage tracking and analytics

## Troubleshooting

### Common Issues

1. **Email Connection Failed**
   - Verify IMAP settings
   - Check app password (not regular password)
   - Ensure 2FA is enabled for Gmail

2. **Database Connection Error**
   - Verify DATABASE_URL format
   - Check PostgreSQL service status on Render

3. **Admin Login Issues**
   - Check ADMIN_USERNAME and ADMIN_PASSWORD environment variables
   - Clear browser cache and cookies

### Logs

Check application logs in Render dashboard for detailed error information.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For issues and questions:
- Create an issue on GitHub
- Check the troubleshooting section
- Review the logs for error details
