import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

load_dotenv()

def test_email():
    smtp_server = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
    smtp_port = int(os.getenv('SMTP_PORT', 587))
    username = os.getenv('SMTP_USERNAME')
    password = os.getenv('SMTP_PASSWORD')
    
    print(f"Testing email with: {username}")
    print(f"Password length: {len(password) if password else 0} characters")
    
    try:
        msg = MIMEMultipart('alternative')
        msg['From'] = username
        msg['To'] = username
        msg['Subject'] = "Test Email from FreelanceHub"
        
        html = """
        <html>
        <body>
            <h1>Test Email</h1>
            <p>If you receive this, email configuration is working!</p>
        </body>
        </html>
        """
        
        msg.attach(MIMEText(html, 'html'))
        
        print("Connecting to SMTP server...")
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        print("Logging in...")
        server.login(username, password)
        print("Sending email...")
        server.send_message(msg)
        server.quit()
        
        print("✅ Test email sent successfully! Check your inbox.")
        return True
    except Exception as e:
        print(f"❌ Failed: {e}")
        return False

if __name__ == "__main__":
    test_email()