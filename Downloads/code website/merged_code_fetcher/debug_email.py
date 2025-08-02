#!/usr/bin/env python3
"""
Debug script to test email functionality
"""

import os
import sys
from flask import Flask
from database import db, init_db, EmailAccount, AdminUser
from email_reader import EmailCodeReader

def create_test_app():
    """Create a test Flask app"""
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'test-key'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///instance/code_fetcher.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    init_db(app)
    return app

def test_email_accounts():
    """Test email account functionality"""
    app = create_test_app()
    
    with app.app_context():
        print("=== EMAIL ACCOUNT DEBUG TEST ===")
        
        # Check if we have any email accounts
        accounts = EmailAccount.query.all()
        print(f"Total email accounts in database: {len(accounts)}")
        
        for account in accounts:
            print(f"Account: {account.email} ({account.provider}) - Active: {account.is_active}")
            
        # Check active accounts
        active_accounts = EmailAccount.query.filter_by(is_active=True).all()
        print(f"Active email accounts: {len(active_accounts)}")
        
        if not active_accounts:
            print("❌ NO ACTIVE EMAIL ACCOUNTS FOUND!")
            print("This is likely why no codes are being fetched.")
            print("Please add email accounts through the admin panel.")
            return False
        
        # Test email reader
        print("\n=== TESTING EMAIL READER ===")
        reader = EmailCodeReader()
        
        # Test getting accounts
        db_accounts = reader.get_active_email_accounts()
        print(f"Email reader found {len(db_accounts)} active accounts")
        
        for account in db_accounts:
            print(f"Testing connection to: {account.email}")
            
            # Test IMAP settings
            imap_server, imap_port = account.get_imap_settings()
            print(f"IMAP Settings: {imap_server}:{imap_port}")
            
            # Test connection (without actually connecting to avoid authentication issues)
            print(f"Provider: {account.provider}")
            
        # Test the main functions
        print("\n=== TESTING MAIN FUNCTIONS ===")
        try:
            netflix_result = reader.get_latest_netflix_code()
            print(f"Netflix code result: {netflix_result}")
        except Exception as e:
            print(f"❌ Error getting Netflix code: {str(e)}")
            
        try:
            chatgpt_result = reader.get_latest_chatgpt_code()
            print(f"ChatGPT code result: {chatgpt_result}")
        except Exception as e:
            print(f"❌ Error getting ChatGPT code: {str(e)}")
            
        return True

def test_database_connection():
    """Test database connection"""
    app = create_test_app()
    
    with app.app_context():
        print("=== DATABASE CONNECTION TEST ===")
        
        try:
            # Test basic database operations
            admin_count = AdminUser.query.count()
            account_count = EmailAccount.query.count()
            
            print(f"✅ Database connection successful")
            print(f"Admin users: {admin_count}")
            print(f"Email accounts: {account_count}")
            
            return True
            
        except Exception as e:
            print(f"❌ Database connection failed: {str(e)}")
            return False

def main():
    """Main debug function"""
    print("Starting email functionality debug...")
    
    # Test database connection
    if not test_database_connection():
        print("Database connection failed. Exiting.")
        return
    
    # Test email accounts
    if not test_email_accounts():
        print("Email account test failed.")
        return
    
    print("\n=== DEBUG COMPLETE ===")
    print("If you're still not getting codes, the issue might be:")
    print("1. Email credentials are incorrect")
    print("2. Email provider requires app-specific passwords")
    print("3. No recent Netflix/ChatGPT emails in the configured accounts")
    print("4. Email provider is blocking IMAP access")

if __name__ == "__main__":
    main()
