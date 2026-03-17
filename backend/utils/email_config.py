import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

load_dotenv()

class EmailConfig:
    """Email configuration settings"""
    
    # Email settings
    SMTP_SERVER = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
    SMTP_PORT = int(os.getenv('SMTP_PORT', 587))
    SMTP_USERNAME = os.getenv('SMTP_USERNAME', '')
    SMTP_PASSWORD = os.getenv('SMTP_PASSWORD', '')
    FROM_EMAIL = os.getenv('FROM_EMAIL', 'noreply@freelancehub.com')
    FROM_NAME = os.getenv('FROM_NAME', 'FreelanceHub')
    
    # Base URL for links
    BASE_URL = os.getenv('BASE_URL', 'http://localhost:3000')
    
    @classmethod
    def is_configured(cls):
        """Check if email is configured"""
        return bool(cls.SMTP_USERNAME and cls.SMTP_PASSWORD)
    
    @classmethod
    def send_email(cls, to_email, subject, html_content, text_content=None):
        """Send an email"""
        if not cls.is_configured():
            print("⚠️ Email not configured. Skipping email send.")
            print(f"To: {to_email}")
            print(f"Subject: {subject}")
            print(f"Content: {html_content[:100]}...")
            return False
        
        try:
            # Create message
            msg = MIMEMultipart('alternative')
            msg['From'] = f"{cls.FROM_NAME} <{cls.FROM_EMAIL}>"
            msg['To'] = to_email
            msg['Subject'] = subject
            
            # Add text version
            if text_content:
                msg.attach(MIMEText(text_content, 'plain'))
            
            # Add HTML version
            msg.attach(MIMEText(html_content, 'html'))
            
            # Send email
            server = smtplib.SMTP(cls.SMTP_SERVER, cls.SMTP_PORT)
            server.starttls()
            server.login(cls.SMTP_USERNAME, cls.SMTP_PASSWORD)
            server.send_message(msg)
            server.quit()
            
            print(f"✅ Email sent to {to_email}")
            return True
            
        except Exception as e:
            print(f"❌ Failed to send email: {str(e)}")
            return False