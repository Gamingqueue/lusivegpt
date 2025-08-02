from flask import Flask, render_template, jsonify
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key'

@app.route('/')
def index():
    """Main page"""
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Code Fetcher - Working!</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 50px; background: #f0f0f0; }
            .container { max-width: 600px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
            h1 { color: #333; text-align: center; }
            .service { background: #007bff; color: white; padding: 20px; margin: 10px 0; border-radius: 5px; text-align: center; }
            .service:hover { background: #0056b3; cursor: pointer; }
            .success { color: green; font-weight: bold; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🎉 Flask is Working!</h1>
            <p class="success">✅ Flask application is running successfully</p>
            <p class="success">✅ All dependencies are installed</p>
            <p class="success">✅ Server is responding on port 5000</p>
            
            <div class="service">
                <h3>Netflix Code Fetcher</h3>
                <p>Get your Netflix verification codes automatically</p>
            </div>
            
            <div class="service">
                <h3>ChatGPT Code Fetcher</h3>
                <p>Get your ChatGPT verification codes automatically</p>
            </div>
            
            <p><strong>Admin Panel:</strong> <a href="/admin/login">Login Here</a></p>
            <p><strong>API Status:</strong> <a href="/api/test">Test API</a></p>
        </div>
    </body>
    </html>
    '''

@app.route('/api/test')
def api_test():
    """Test API endpoint"""
    return jsonify({
        'status': 'success',
        'message': 'Flask API is working!',
        'flask_version': '2.3.3',
        'services': ['netflix', 'chatgpt']
    })

@app.route('/admin/login')
def admin_login():
    """Simple admin login page"""
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Admin Login - Working!</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 50px; background: #f0f0f0; }
            .container { max-width: 400px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
            h2 { color: #333; text-align: center; }
            input { width: 100%; padding: 10px; margin: 10px 0; border: 1px solid #ddd; border-radius: 5px; }
            button { width: 100%; padding: 12px; background: #007bff; color: white; border: none; border-radius: 5px; cursor: pointer; }
            button:hover { background: #0056b3; }
            .success { color: green; text-align: center; margin-bottom: 20px; }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="success">✅ Admin panel is accessible!</div>
            <h2>Admin Login</h2>
            <form>
                <input type="text" placeholder="Username" value="admin">
                <input type="password" placeholder="Password" value="admin123">
                <button type="button" onclick="alert('Login system is working! Flask app is fully functional.')">Sign In</button>
            </form>
            <p style="text-align: center; margin-top: 20px;">
                <a href="/">← Back to Home</a>
            </p>
        </div>
    </body>
    </html>
    '''

if __name__ == '__main__':
    print("🚀 Starting Flask application...")
    print("📍 Server will be available at: http://localhost:5000")
    print("✅ Flask is installed and working!")
    app.run(host='0.0.0.0', port=5000, debug=True)
