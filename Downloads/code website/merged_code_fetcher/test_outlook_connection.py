#!/usr/bin/env python3
"""
Test Outlook Email Connection
This script will test the specific Outlook account connection issue
"""

import imaplib
from flask import Flask
from database import db, init_db, EmailAccount

def create_app():
    """Create Flask app for testing"""
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'test-key'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///instance/code_fetcher.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    init_db(app)
    return app

def test_outlook_connection():
    """Test the specific Outlook account connection"""
    app = create_app()
    
    with app.app_context():
        print("🔍 OUTLOOK CONNECTION TEST")
        print("=" * 50)
        
        # Get the Outlook account
        outlook_account = EmailAccount.query.filter_by(provider='outlook').first()
        
        if not outlook_account:
            print("❌ No Outlook account found in database!")
            return
        
        print(f"📧 Testing account: {outlook_account.email}")
        print(f"🏢 Provider: {outlook_account.provider}")
        print(f"✅ Active: {outlook_account.is_active}")
        print(f"📅 Created: {outlook_account.created_at}")
        print(f"🕐 Last used: {outlook_account.last_used or 'Never'}")
        
        # Get IMAP settings
        imap_server, imap_port = outlook_account.get_imap_settings()
        print(f"🌐 IMAP Server: {imap_server}:{imap_port}")
        
        print("\n🔐 TESTING IMAP CONNECTION...")
        print("-" * 30)
        
        try:
            # Test IMAP connection
            print(f"1. Connecting to {imap_server}:{imap_port}...")
            mail = imaplib.IMAP4_SSL(imap_server, imap_port)
            print("✅ SSL connection established")
            
            print(f"2. Attempting login for {outlook_account.email}...")
            mail.login(outlook_account.email, outlook_account.password)
            print("✅ Login successful!")
            
            print("3. Selecting INBOX...")
            mail.select("INBOX")
            print("✅ INBOX selected")
            
            print("4. Searching for Netflix emails...")
            status, messages = mail.search(None, 'FROM "netflix"')
            if status == "OK" and messages[0]:
                message_count = len(messages[0].split())
                print(f"✅ Found {message_count} Netflix emails")
            else:
                print("⚠️  No Netflix emails found")
                
            print("5. Searching for recent emails...")
            status, messages = mail.search(None, 'ALL')
            if status == "OK" and messages[0]:
                total_count = len(messages[0].split())
                print(f"✅ Total emails in INBOX: {total_count}")
            else:
                print("⚠️  No emails found in INBOX")
            
            mail.close()
            mail.logout()
            print("✅ Connection closed successfully")
            
            print("\n🎉 CONNECTION TEST PASSED!")
            print("The Outlook account is working correctly.")
            print("Issue might be:")
            print("  • No recent Netflix verification emails")
            print("  • Netflix emails are in spam/junk folder")
            print("  • Netflix emails don't contain 4-digit codes")
            
        except imaplib.IMAP4.error as e:
            error_msg = str(e).lower()
            print(f"❌ IMAP Error: {e}")
            
            if "authentication failed" in error_msg or "login failed" in error_msg:
                print("\n🚨 AUTHENTICATION PROBLEM DETECTED!")
                print("=" * 50)
                print("SOLUTION: Outlook requires App Passwords for IMAP access")
                print("")
                print("Steps to fix:")
                print("1. Go to https://account.microsoft.com/security")
                print("2. Enable 2-Factor Authentication if not already enabled")
                print("3. Click 'Advanced security options'")
                print("4. Click 'Create a new app password'")
                print("5. Copy the 16-character App Password (no spaces)")
                print("6. Update your email account in the admin panel with this App Password")
                print("   (Replace the current password with the App Password)")
                print("")
                print("⚠️  IMPORTANT: Use the App Password, NOT your regular Microsoft password!")
                
        except Exception as e:
            print(f"❌ Unexpected error: {e}")
            print("\nPossible issues:")
            print("  • Network connectivity problems")
            print("  • Firewall blocking IMAP connections")
            print("  • Outlook server temporarily unavailable")

if __name__ == "__main__":
    test_outlook_connection()
