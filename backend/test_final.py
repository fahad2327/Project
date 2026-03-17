# test_final.py
from flask import Flask
from flask_mail import Mail, Message
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
app.config['MAIL_SERVER'] = os.getenv('SMTP_SERVER')
app.config['MAIL_PORT'] = int(os.getenv('SMTP_PORT', 587))
app.config['MAIL_USE_TLS'] = os.getenv('MAIL_USE_TLS', 'True').lower() == 'true'
app.config['MAIL_USERNAME'] = os.getenv('SMTP_USERNAME')
app.config['MAIL_PASSWORD'] = os.getenv('SMTP_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = os.getenv('FROM_EMAIL')

mail = Mail(app)

with app.app_context():
    try:
        msg = Message(
            subject="Test from FreelanceHub",
            recipients=[os.getenv('SMTP_USERNAME')],
            body="If you received this, email is working!"
        )
        mail.send(msg)
        print("✅ Email sent successfully!")
    except Exception as e:
        print(f"❌ Failed: {e}")