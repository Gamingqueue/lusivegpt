import imaplib
import email
import os
from email.header import decode_header
import re

class EmailCodeReader:
    def __init__(self):
        # Email accounts configuration - UPDATE THESE WITH YOUR DETAILS
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
        
        # ChatGPT verification phrases
        self.chatgpt_verification_phrases = [
            "please use the following code to help verify your identity",
            "we noticed a suspicious log-in on your account",
            "enter this code to verify it's you",
            "your verification code is",
            "verification code:",
            "here is your verification code",
        ]
        
        # Netflix verification phrases
        self.netflix_verification_phrases = [
            "netflix",
            "verification code",
            "sign-in code",
            "login code",
        ]

    def connect_to_email(self, account_config):
        """Connect to email account using IMAP"""
        try:
            print(f"Connecting to {account_config['provider']}: {account_config['imap_server']}:{account_config['imap_port']}")
            mail = imaplib.IMAP4_SSL(account_config['imap_server'], account_config['imap_port'])
            print(f"Logging in as {account_config['email']}")
            mail.login(account_config['email'], account_config['password'])
            print(f"✅ Successfully connected to {account_config['provider']}")
            return mail
        except Exception as e:
            print(f"❌ Failed to connect to {account_config['provider']} ({account_config['email']}): {str(e)}")
            print("Make sure you're using an App Password, not your regular password!")
            if account_config['provider'] == 'outlook':
                print("Generate Outlook App Password at: https://account.microsoft.com/security")
            elif account_config['provider'] == 'gmail':
                print("Generate Gmail App Password at: https://myaccount.google.com/apppasswords")
            return None

    def extract_netflix_code_from_text(self, text, subject=""):
        """Extract 4-digit Netflix code from email text"""
        # Check if this looks like a Netflix email
        combined_text = (text + " " + subject).lower()
        if not any(phrase in combined_text for phrase in self.netflix_verification_phrases):
            return None
        
        # Look for 4-digit codes
        matches = re.findall(r'\b\d{4}\b', text)
        if matches:
            # Return the first 4-digit code found
            return matches[0]
        return None

    def extract_chatgpt_code_from_text(self, text, subject=""):
        """Extract 6-digit ChatGPT code from email text"""
        # Check if this looks like a ChatGPT/OpenAI email
        combined_text = (text + " " + subject).lower()
        if not any(phrase in combined_text for phrase in self.chatgpt_verification_phrases):
            return None
        
        # Look for 6-digit codes
        matches = re.findall(r'\b\d{6}\b', text)
        if matches:
            # Return the first 6-digit code found
            return matches[0]
        return None

    def search_emails_for_code(self, account_config, service_type="netflix"):
        """Search emails in a specific account for verification codes"""
        mail = self.connect_to_email(account_config)
        if not mail:
            return None

        try:
            # Define search criteria based on service
            if service_type == "netflix":
                search_criteria = [
                    'FROM "netflix"',
                    'FROM "noreply@account.netflix.com"',
                    'SUBJECT "Netflix"',
                ]
                extract_func = self.extract_netflix_code_from_text
            else:  # chatgpt
                search_criteria = [
                    'FROM "openai.com"',
                    'FROM "noreply@openai.com"',
                    'FROM "chatgpt"',
                    'SUBJECT "OpenAI"',
                    'SUBJECT "ChatGPT"',
                ]
                extract_func = self.extract_chatgpt_code_from_text

            # Check multiple folders based on provider
            folders_to_check = account_config['folders']

            for folder in folders_to_check:
                try:
                    print(f"Checking folder: {folder} in {account_config['email']}")
                    mail.select(folder)
                    
                    # Try each search criteria
                    for criteria in search_criteria:
                        try:
                            print(f"Searching with criteria: {criteria}")
                            status, messages = mail.search(None, criteria)
                            if status == "OK" and messages[0]:
                                message_ids = messages[0].split()
                                print(f"Found {len(message_ids)} messages")
                                
                                # Check the most recent emails first (last 5)
                                for msg_id in reversed(message_ids[-5:]):
                                    try:
                                        status, msg_data = mail.fetch(msg_id, "(RFC822)")
                                        if status != "OK":
                                            continue

                                        msg = email.message_from_bytes(msg_data[0][1])
                                        
                                        # Get subject
                                        subject = ""
                                        if msg["Subject"]:
                                            subject_parts = decode_header(msg["Subject"])
                                            subject = ""
                                            for part, encoding in subject_parts:
                                                if isinstance(part, bytes):
                                                    subject += part.decode(encoding or "utf-8", errors="ignore")
                                                else:
                                                    subject += part

                                        # Get email body
                                        body = self.extract_email_body(msg)
                                        
                                        # Extract code
                                        code = extract_func(body, subject)
                                        if code:
                                            print(f"✅ Found {service_type} code: {code} in {account_config['email']}")
                                            return code
                                            
                                    except Exception as e:
                                        print(f"Error processing message: {str(e)}")
                                        continue
                        except Exception as e:
                            print(f"Error searching with criteria '{criteria}': {str(e)}")
                            continue
                            
                except Exception as e:
                    print(f"Error accessing folder '{folder}': {str(e)}")
                    continue

            return None

        except Exception as e:
            print(f"Error searching emails in {account_config['email']}: {str(e)}")
            return None
        finally:
            try:
                mail.close()
                mail.logout()
            except:
                pass

    def extract_email_body(self, msg):
        """Extract text content from email message"""
        body = ""
        
        if msg.is_multipart():
            for part in msg.walk():
                content_type = part.get_content_type()
                content_disposition = str(part.get("Content-Disposition", ""))
                
                if content_type == "text/plain" and "attachment" not in content_disposition:
                    try:
                        body = part.get_payload(decode=True).decode(errors="ignore")
                        break
                    except:
                        continue
            
            # If no plain text found, try HTML
            if not body.strip():
                for part in msg.walk():
                    content_type = part.get_content_type()
                    content_disposition = str(part.get("Content-Disposition", ""))
                    
                    if content_type == "text/html" and "attachment" not in content_disposition:
                        try:
                            html_body = part.get_payload(decode=True).decode(errors="ignore")
                            # Strip HTML tags
                            body = re.sub(r'<[^>]+>', ' ', html_body)
                            break
                        except:
                            continue
        else:
            try:
                body = msg.get_payload(decode=True).decode(errors="ignore")
            except:
                body = str(msg.get_payload())

        return body

    def get_latest_netflix_code(self):
        """
        Fetches the latest Netflix verification code from configured email accounts.
        Returns the 4-digit code or an error message.
        """
        try:
            print("🔍 Searching for Netflix codes in all configured email accounts...")
            
            # Try each configured email account
            for account_config in self.email_accounts:
                try:
                    print(f"Checking {account_config['provider']} account: {account_config['email']}")
                    code = self.search_emails_for_code(account_config, "netflix")
                    if code:
                        return code
                except Exception as e:
                    print(f"Error checking {account_config['email']} for Netflix codes: {str(e)}")
                    continue
            
            return "No recent Netflix verification codes found in any configured email accounts."
            
        except Exception as e:
            print(f"Error in get_latest_netflix_code: {str(e)}")
            return f"Error: {str(e)}"

    def get_latest_chatgpt_code(self):
        """
        Fetches the latest ChatGPT verification code from configured email accounts.
        Returns the 6-digit code or an error message.
        """
        try:
            print("🔍 Searching for ChatGPT codes in all configured email accounts...")
            
            # Try each configured email account
            for account_config in self.email_accounts:
                try:
                    print(f"Checking {account_config['provider']} account: {account_config['email']}")
                    code = self.search_emails_for_code(account_config, "chatgpt")
                    if code:
                        return code
                except Exception as e:
                    print(f"Error checking {account_config['email']} for ChatGPT codes: {str(e)}")
                    continue
            
            return "No recent ChatGPT verification codes found in any configured email accounts."
            
        except Exception as e:
            print(f"Error in get_latest_chatgpt_code: {str(e)}")
            return f"Error: {str(e)}"

# Global instance
email_reader = EmailCodeReader()

# Convenience functions for backward compatibility
def get_latest_netflix_code():
    return email_reader.get_latest_netflix_code()

def get_latest_chatgpt_code():
    return email_reader.get_latest_chatgpt_code()
