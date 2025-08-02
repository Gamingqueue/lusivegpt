#!/usr/bin/env python3
"""
Quick Email Diagnosis Script
Run this to identify why Netflix codes aren't showing up
"""

import os
import sys
from flask import Flask
from database import db, init_db, EmailAccount, AdminUser, ApiKey
from email_reader import get_latest_netflix_code

def create_app():
    """Create Flask app for testing"""
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'test-key'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///instance/code_fetcher.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    init_db(app)
    return app

def main():
    """Main diagnostic function"""
    print("🔍 NETFLIX CODE FETCHING DIAGNOSIS")
    print("=" * 50)
    
    app = create_app()
    
    with app.app_context():
        # Step 1: Check database connection
        print("\n1️⃣ Checking database connection...")
        try:
            admin_count = AdminUser.query.count()
            print(f"✅ Database connected - {admin_count} admin users found")
        except Exception as e:
            print(f"❌ Database connection failed: {e}")
            return
        
        # Step 2: Check email accounts
        print("\n2️⃣ Checking email accounts...")
        try:
            all_accounts = EmailAccount.query.all()
            active_accounts = EmailAccount.query.filter_by(is_active=True).all()
            
            print(f"📧 Total email accounts: {len(all_accounts)}")
            print(f"✅ Active email accounts: {len(active_accounts)}")
            
            if not all_accounts:
                print("❌ NO EMAIL ACCOUNTS FOUND!")
                print("   → Go to http://localhost:5000/admin/login")
                print("   → Login with admin/admin123")
                print("   → Add email accounts in 'Email Accounts' section")
                return
            
            for account in all_accounts:
                status = "✅ Active" if account.is_active else "❌ Inactive"
                print(f"   - {account.email} ({account.provider}) {status}")
                
                if account.provider == 'outlook':
                    print("   ⚠️  OUTLOOK USERS: Make sure you're using an App Password!")
                    print("      Regular passwords don't work with Outlook IMAP")
                    
        except Exception as e:
            print(f"❌ Error checking email accounts: {e}")
            return
        
        # Step 3: Check API keys
        print("\n3️⃣ Checking API keys...")
        try:
            api_keys = ApiKey.query.filter_by(is_active=True).all()
            netflix_keys = [k for k in api_keys if k.can_use_service('netflix')]
            
            print(f"🔑 Active API keys: {len(api_keys)}")
            print(f"🎬 Netflix-compatible keys: {len(netflix_keys)}")
            
            if netflix_keys:
                sample_key = netflix_keys[0]
                print(f"   Sample key: {sample_key.key[:8]}... (uses: {sample_key.current_usage}/{sample_key.usage_limit})")
            else:
                print("❌ No Netflix-compatible API keys found!")
                
        except Exception as e:
            print(f"❌ Error checking API keys: {e}")
        
        # Step 4: Test Netflix code fetching
        print("\n4️⃣ Testing Netflix code fetching...")
        if not active_accounts:
            print("❌ Cannot test - no active email accounts")
            return
            
        try:
            print("🔄 Attempting to fetch Netflix code...")
            result = get_latest_netflix_code()
            
            if result.startswith("Error:"):
                print(f"❌ {result}")
                if "No email accounts configured" in result:
                    print("   → Add email accounts through admin panel")
                elif "authentication failed" in result.lower():
                    print("   → Check email credentials (use App Password for Outlook)")
            elif result.startswith("No recent"):
                print(f"⚠️  {result}")
                print("   → Make sure you have recent Netflix emails with 4-digit codes")
                print("   → Try requesting a new Netflix verification code")
            else:
                print(f"✅ SUCCESS! Found code: {result}")
                
        except Exception as e:
            print(f"❌ Error testing Netflix code fetching: {e}")
            import traceback
            traceback.print_exc()
    
    print("\n" + "=" * 50)
    print("📋 SUMMARY & NEXT STEPS:")
    print("=" * 50)
    
    with app.app_context():
        accounts = EmailAccount.query.filter_by(is_active=True).all()
        
        if not accounts:
            print("🚨 MAIN ISSUE: No email accounts configured")
            print("   1. Go to http://localhost:5000/admin/login")
            print("   2. Login with admin/admin123")
            print("   3. Go to 'Email Accounts' section")
            print("   4. Add your Outlook email with App Password")
        else:
            outlook_accounts = [a for a in accounts if a.provider == 'outlook']
            if outlook_accounts:
                print("🔐 OUTLOOK USERS - IMPORTANT:")
                print("   • Regular passwords DON'T work with Outlook")
                print("   • You MUST use an App Password:")
                print("     1. Go to https://account.microsoft.com/security")
                print("     2. Enable 2-Factor Authentication")
                print("     3. Generate App Password")
                print("     4. Update your email account with the App Password")
            
            print("\n📧 EMAIL REQUIREMENTS:")
            print("   • Must have recent Netflix emails")
            print("   • Emails must contain 4-digit verification codes")
            print("   • Check spam/junk folders too")
            
            print("\n🔧 IF STILL NOT WORKING:")
            print("   • Check console output when running Flask app")
            print("   • Try with a fresh Netflix verification email")
            print("   • Verify IMAP is enabled for your email provider")

if __name__ == "__main__":
    main()
