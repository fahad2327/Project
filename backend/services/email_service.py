# # # # # # # # # # services/email_service.py

# # # # # # # # # from flask_mail import Message
# # # # # # # # # from flask import current_app, render_template
# # # # # # # # # from threading import Thread
# # # # # # # # # import logging

# # # # # # # # # class EmailService:
# # # # # # # # #     def __init__(self, mail):
# # # # # # # # #         self.mail = mail
# # # # # # # # #         self.base_url = current_app.config.get('BASE_URL', 'http://localhost:3000')
    
# # # # # # # # #     def send_async_email(self, msg):
# # # # # # # # #         """Send email asynchronously"""
# # # # # # # # #         try:
# # # # # # # # #             with current_app.app_context():
# # # # # # # # #                 self.mail.send(msg)
# # # # # # # # #                 logging.info(f"Email sent to {msg.recipients}")
# # # # # # # # #         except Exception as e:
# # # # # # # # #             logging.error(f"Failed to send email: {str(e)}")
    
# # # # # # # # #     def send_email(self, to_email, subject, template, **kwargs):
# # # # # # # # #         """Send email using template"""
# # # # # # # # #         try:
# # # # # # # # #             msg = Message(
# # # # # # # # #                 subject=subject,
# # # # # # # # #                 recipients=[to_email],
# # # # # # # # #                 sender=current_app.config.get('FROM_EMAIL', 'noreply@freelancehub.com')
# # # # # # # # #             )
            
# # # # # # # # #             # HTML content based on template
# # # # # # # # #             html_content = self.get_email_template(template, **kwargs)
# # # # # # # # #             msg.html = html_content
            
# # # # # # # # #             # Send asynchronously
# # # # # # # # #             Thread(target=self.send_async_email, args=(msg,)).start()
            
# # # # # # # # #             return True
# # # # # # # # #         except Exception as e:
# # # # # # # # #             logging.error(f"Error preparing email: {str(e)}")
# # # # # # # # #             return False
    
# # # # # # # # #     def get_email_template(self, template, **kwargs):
# # # # # # # # #         """Get email HTML template"""
        
# # # # # # # # #         templates = {
# # # # # # # # #             'welcome': self.welcome_template,
# # # # # # # # #             'verify_email': self.verify_email_template,
# # # # # # # # #             'application_received': self.application_received_template,
# # # # # # # # #             'application_accepted': self.application_accepted_template,
# # # # # # # # #             'application_rejected': self.application_rejected_template,
# # # # # # # # #             'password_reset': self.password_reset_template,
# # # # # # # # #             'new_message': self.new_message_template
# # # # # # # # #         }
        
# # # # # # # # #         template_func = templates.get(template, self.default_template)
# # # # # # # # #         return template_func(**kwargs)
    
# # # # # # # # #     def verify_email_template(self, **kwargs):
# # # # # # # # #         """Email verification template"""
# # # # # # # # #         name = kwargs.get('name', 'User')
# # # # # # # # #         verification_link = kwargs.get('verification_link', '#')
        
# # # # # # # # #         return f"""
# # # # # # # # #         <!DOCTYPE html>
# # # # # # # # #         <html>
# # # # # # # # #         <head>
# # # # # # # # #             <meta charset="UTF-8">
# # # # # # # # #             <meta name="viewport" content="width=device-width, initial-scale=1.0">
# # # # # # # # #         </head>
# # # # # # # # #         <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333; max-width: 600px; margin: 0 auto; padding: 20px;">
# # # # # # # # #             <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 30px; text-align: center; border-radius: 10px 10px 0 0;">
# # # # # # # # #                 <h1 style="color: white; margin: 0;">Welcome to FreelanceHub! 🚀</h1>
# # # # # # # # #             </div>
            
# # # # # # # # #             <div style="background: #f9f9f9; padding: 30px; border-radius: 0 0 10px 10px;">
# # # # # # # # #                 <h2>Hello {name},</h2>
# # # # # # # # #                 <p>Thank you for signing up! Please verify your email address to get started.</p>
                
# # # # # # # # #                 <div style="text-align: center; margin: 30px 0;">
# # # # # # # # #                     <a href="{verification_link}" style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 15px 40px; text-decoration: none; border-radius: 50px; font-weight: bold; display: inline-block;">
# # # # # # # # #                         Verify Email Address
# # # # # # # # #                     </a>
# # # # # # # # #                 </div>
                
# # # # # # # # #                 <p style="color: #666; font-size: 14px;">Or copy this link: <br> <a href="{verification_link}" style="color: #667eea;">{verification_link}</a></p>
                
# # # # # # # # #                 <p style="color: #666; font-size: 14px;">This link will expire in 24 hours.</p>
                
# # # # # # # # #                 <hr style="border: none; border-top: 1px solid #ddd; margin: 30px 0;">
                
# # # # # # # # #                 <p style="color: #999; font-size: 12px; text-align: center;">
# # # # # # # # #                     If you didn't create an account, please ignore this email.<br>
# # # # # # # # #                     &copy; 2026 FreelanceHub. All rights reserved.
# # # # # # # # #                 </p>
# # # # # # # # #             </div>
# # # # # # # # #         </body>
# # # # # # # # #         </html>
# # # # # # # # #         """
    
# # # # # # # # #     def application_received_template(self, **kwargs):
# # # # # # # # #         """Template for recruiter when someone applies"""
# # # # # # # # #         job_title = kwargs.get('job_title', 'a job')
# # # # # # # # #         freelancer_name = kwargs.get('freelancer_name', 'Someone')
# # # # # # # # #         proposed_rate = kwargs.get('proposed_rate', 'N/A')
# # # # # # # # #         dashboard_link = f"{self.base_url}/manage-jobs"
        
# # # # # # # # #         return f"""
# # # # # # # # #         <!DOCTYPE html>
# # # # # # # # #         <html>
# # # # # # # # #         <head>
# # # # # # # # #             <style>
# # # # # # # # #                 .container {{ max-width: 600px; margin: 0 auto; padding: 20px; font-family: Arial, sans-serif; }}
# # # # # # # # #                 .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 30px; text-align: center; border-radius: 10px 10px 0 0; }}
# # # # # # # # #                 .content {{ background: #f9f9f9; padding: 30px; border-radius: 0 0 10px 10px; }}
# # # # # # # # #                 .button {{ background: #667eea; color: white; padding: 12px 30px; text-decoration: none; border-radius: 5px; display: inline-block; margin: 20px 0; }}
# # # # # # # # #                 .details {{ background: white; padding: 20px; border-radius: 5px; margin: 20px 0; }}
# # # # # # # # #             </style>
# # # # # # # # #         </head>
# # # # # # # # #         <body>
# # # # # # # # #             <div class="container">
# # # # # # # # #                 <div class="header">
# # # # # # # # #                     <h1>New Application! 📝</h1>
# # # # # # # # #                 </div>
                
# # # # # # # # #                 <div class="content">
# # # # # # # # #                     <h2>Hello,</h2>
# # # # # # # # #                     <p>Good news! <strong>{freelancer_name}</strong> has applied for your job: <strong>"{job_title}"</strong></p>
                    
# # # # # # # # #                     <div class="details">
# # # # # # # # #                         <h3>Application Details:</h3>
# # # # # # # # #                         <p><strong>Freelancer:</strong> {freelancer_name}</p>
# # # # # # # # #                         <p><strong>Proposed Rate:</strong> ${proposed_rate}</p>
# # # # # # # # #                         <p><strong>Applied:</strong> Just now</p>
# # # # # # # # #                     </div>
                    
# # # # # # # # #                     <div style="text-align: center;">
# # # # # # # # #                         <a href="{dashboard_link}" class="button">View Application</a>
# # # # # # # # #                     </div>
                    
# # # # # # # # #                     <p style="color: #666; font-size: 14px;">Login to review the full application and respond.</p>
# # # # # # # # #                 </div>
# # # # # # # # #             </div>
# # # # # # # # #         </body>
# # # # # # # # #         </html>
# # # # # # # # #         """
    
# # # # # # # # #     def application_accepted_template(self, **kwargs):
# # # # # # # # #         """Template for freelancer when accepted"""
# # # # # # # # #         job_title = kwargs.get('job_title', 'a job')
# # # # # # # # #         recruiter_name = kwargs.get('recruiter_name', 'Recruiter')
# # # # # # # # #         dashboard_link = f"{self.base_url}/my-applications"
        
# # # # # # # # #         return f"""
# # # # # # # # #         <!DOCTYPE html>
# # # # # # # # #         <html>
# # # # # # # # #         <head>
# # # # # # # # #             <style>
# # # # # # # # #                 .container {{ max-width: 600px; margin: 0 auto; padding: 20px; font-family: Arial, sans-serif; }}
# # # # # # # # #                 .header {{ background: linear-gradient(135deg, #10b981 0%, #059669 100%); color: white; padding: 30px; text-align: center; border-radius: 10px 10px 0 0; }}
# # # # # # # # #                 .content {{ background: #f9f9f9; padding: 30px; border-radius: 0 0 10px 10px; }}
# # # # # # # # #                 .button {{ background: #10b981; color: white; padding: 12px 30px; text-decoration: none; border-radius: 5px; display: inline-block; margin: 20px 0; }}
# # # # # # # # #             </style>
# # # # # # # # #         </head>
# # # # # # # # #         <body>
# # # # # # # # #             <div class="container">
# # # # # # # # #                 <div class="header">
# # # # # # # # #                     <h1>Congratulations! 🎉</h1>
# # # # # # # # #                 </div>
                
# # # # # # # # #                 <div class="content">
# # # # # # # # #                     <h2>Great News!</h2>
# # # # # # # # #                     <p>Your application for <strong>"{job_title}"</strong> has been <strong style="color: #10b981;">ACCEPTED</strong>!</p>
                    
# # # # # # # # #                     <p>The recruiter will contact you soon with next steps.</p>
                    
# # # # # # # # #                     <div style="text-align: center;">
# # # # # # # # #                         <a href="{dashboard_link}" class="button">View Application Status</a>
# # # # # # # # #                     </div>
# # # # # # # # #                 </div>
# # # # # # # # #             </div>
# # # # # # # # #         </body>
# # # # # # # # #         </html>
# # # # # # # # #         """
    
# # # # # # # # #     def application_rejected_template(self, **kwargs):
# # # # # # # # #         """Template for freelancer when rejected"""
# # # # # # # # #         job_title = kwargs.get('job_title', 'a job')
# # # # # # # # #         dashboard_link = f"{self.base_url}/jobs"
        
# # # # # # # # #         return f"""
# # # # # # # # #         <!DOCTYPE html>
# # # # # # # # #         <html>
# # # # # # # # #         <head>
# # # # # # # # #             <style>
# # # # # # # # #                 .container {{ max-width: 600px; margin: 0 auto; padding: 20px; font-family: Arial, sans-serif; }}
# # # # # # # # #                 .header {{ background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%); color: white; padding: 30px; text-align: center; border-radius: 10px 10px 0 0; }}
# # # # # # # # #                 .content {{ background: #f9f9f9; padding: 30px; border-radius: 0 0 10px 10px; }}
# # # # # # # # #                 .button {{ background: #667eea; color: white; padding: 12px 30px; text-decoration: none; border-radius: 5px; display: inline-block; margin: 20px 0; }}
# # # # # # # # #             </style>
# # # # # # # # #         </head>
# # # # # # # # #         <body>
# # # # # # # # #             <div class="container">
# # # # # # # # #                 <div class="header">
# # # # # # # # #                     <h1>Application Update</h1>
# # # # # # # # #                 </div>
                
# # # # # # # # #                 <div class="content">
# # # # # # # # #                     <h2>Update on your application</h2>
# # # # # # # # #                     <p>Your application for <strong>"{job_title}"</strong> was not selected at this time.</p>
                    
# # # # # # # # #                     <p>Don't be discouraged! There are many other opportunities waiting for you.</p>
                    
# # # # # # # # #                     <div style="text-align: center;">
# # # # # # # # #                         <a href="{dashboard_link}" class="button">Browse More Jobs</a>
# # # # # # # # #                     </div>
# # # # # # # # #                 </div>
# # # # # # # # #             </div>
# # # # # # # # #         </body>
# # # # # # # # #         </html>
# # # # # # # # #         """
    
# # # # # # # # #     def welcome_template(self, **kwargs):
# # # # # # # # #         """Welcome email after verification"""
# # # # # # # # #         name = kwargs.get('name', 'User')
# # # # # # # # #         dashboard_link = f"{self.base_url}/dashboard"
        
# # # # # # # # #         return f"""
# # # # # # # # #         <!DOCTYPE html>
# # # # # # # # #         <html>
# # # # # # # # #         <head>
# # # # # # # # #             <style>
# # # # # # # # #                 .container {{ max-width: 600px; margin: 0 auto; padding: 20px; font-family: Arial, sans-serif; }}
# # # # # # # # #                 .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 30px; text-align: center; border-radius: 10px 10px 0 0; }}
# # # # # # # # #                 .content {{ background: #f9f9f9; padding: 30px; border-radius: 0 0 10px 10px; }}
# # # # # # # # #                 .button {{ background: #667eea; color: white; padding: 12px 30px; text-decoration: none; border-radius: 5px; display: inline-block; margin: 10px; }}
# # # # # # # # #                 .features {{ display: flex; flex-wrap: wrap; justify-content: space-around; margin: 30px 0; }}
# # # # # # # # #                 .feature {{ text-align: center; padding: 15px; }}
# # # # # # # # #             </style>
# # # # # # # # #         </head>
# # # # # # # # #         <body>
# # # # # # # # #             <div class="container">
# # # # # # # # #                 <div class="header">
# # # # # # # # #                     <h1>Welcome to FreelanceHub! 🎉</h1>
# # # # # # # # #                 </div>
                
# # # # # # # # #                 <div class="content">
# # # # # # # # #                     <h2>Hello {name}!</h2>
# # # # # # # # #                     <p>Your email has been verified. You're now ready to start your journey!</p>
                    
# # # # # # # # #                     <div class="features">
# # # # # # # # #                         <div class="feature">
# # # # # # # # #                             <div style="font-size: 40px;">🔍</div>
# # # # # # # # #                             <h4>Find Work</h4>
# # # # # # # # #                         </div>
# # # # # # # # #                         <div class="feature">
# # # # # # # # #                             <div style="font-size: 40px;">💼</div>
# # # # # # # # #                             <h4>Post Jobs</h4>
# # # # # # # # #                         </div>
# # # # # # # # #                         <div class="feature">
# # # # # # # # #                             <div style="font-size: 40px;">🤝</div>
# # # # # # # # #                             <h4>Connect</h4>
# # # # # # # # #                         </div>
# # # # # # # # #                     </div>
                    
# # # # # # # # #                     <div style="text-align: center;">
# # # # # # # # #                         <a href="{dashboard_link}" class="button">Go to Dashboard</a>
# # # # # # # # #                         <a href="{self.base_url}/profile" class="button" style="background: #764ba2;">Complete Profile</a>
# # # # # # # # #                     </div>
# # # # # # # # #                 </div>
# # # # # # # # #             </div>
# # # # # # # # #         </body>
# # # # # # # # #         </html>
# # # # # # # # #         """
# # # # # # # # # services/email_service.py
# # # # # # # # from flask_mail import Message
# # # # # # # # from flask import current_app
# # # # # # # # from threading import Thread
# # # # # # # # import logging
# # # # # # # # from utils.email_templates import EmailTemplates

# # # # # # # # class EmailService:
# # # # # # # #     def __init__(self, mail):
# # # # # # # #         self.mail = mail
# # # # # # # #         self.base_url = current_app.config.get('BASE_URL', 'http://localhost:3000')
    
# # # # # # # #     def send_async_email(self, msg):
# # # # # # # #         """Send email asynchronously"""
# # # # # # # #         try:
# # # # # # # #             with current_app.app_context():
# # # # # # # #                 self.mail.send(msg)
# # # # # # # #                 logging.info(f"✅ Email sent to {msg.recipients}")
# # # # # # # #         except Exception as e:
# # # # # # # #             logging.error(f"❌ Failed to send email: {str(e)}")
    
# # # # # # # #     def send_email(self, to_email, subject, html_content):
# # # # # # # #         """Send email with HTML content"""
# # # # # # # #         try:
# # # # # # # #             msg = Message(
# # # # # # # #                 subject=subject,
# # # # # # # #                 recipients=[to_email],
# # # # # # # #                 html=html_content,
# # # # # # # #                 sender=current_app.config.get('FROM_EMAIL', 'noreply@freelancehub.com')
# # # # # # # #             )
            
# # # # # # # #             # Send asynchronously
# # # # # # # #             Thread(target=self.send_async_email, args=(msg,)).start()
# # # # # # # #             logging.info(f"📧 Email queued for {to_email}: {subject}")
# # # # # # # #             return True
# # # # # # # #         except Exception as e:
# # # # # # # #             logging.error(f"❌ Error preparing email: {str(e)}")
# # # # # # # #             return False
    
# # # # # # # #     def send_verification_email(self, to_email, user_name, verification_token):
# # # # # # # #         """Send email verification"""
# # # # # # # #         html_content, subject = EmailTemplates.email_verification(user_name, verification_token)
# # # # # # # #         return self.send_email(to_email, subject, html_content)
    
# # # # # # # #     def send_welcome_email(self, to_email, user_name, user_type):
# # # # # # # #         """Send welcome email after verification"""
# # # # # # # #         html_content, subject = EmailTemplates.welcome_email(user_name, user_type)
# # # # # # # #         return self.send_email(to_email, subject, html_content)
    
# # # # # # # #     def send_job_posted_notification(self, to_email, recruiter_name, job_title, job_id):
# # # # # # # #         """Send notification to recruiter when job is posted"""
# # # # # # # #         html_content, subject = EmailTemplates.job_posted_notification(recruiter_name, job_title, job_id)
# # # # # # # #         return self.send_email(to_email, subject, html_content)
    
# # # # # # # #     def send_application_submitted_notification(self, to_email, recruiter_name, freelancer_name, job_title, job_id, application_id):
# # # # # # # #         """Send notification to recruiter when someone applies"""
# # # # # # # #         html_content, subject = EmailTemplates.application_submitted_notification(
# # # # # # # #             recruiter_name, freelancer_name, job_title, job_id, application_id
# # # # # # # #         )
# # # # # # # #         return self.send_email(to_email, subject, html_content)
    
# # # # # # # #     def send_application_status_update(self, to_email, freelancer_name, job_title, status, recruiter_notes=None, job_id=None):
# # # # # # # #         """Send status update to freelancer"""
# # # # # # # #         html_content, subject, _ = EmailTemplates.application_status_update(
# # # # # # # #             freelancer_name, job_title, status, recruiter_notes, job_id
# # # # # # # #         )
# # # # # # # #         return self.send_email(to_email, subject, html_content)

# # # # # # # # # Global instance (will be initialized in app.py)
# # # # # # # # email_service = None


# # # # # # # # services/email_service.py
# # # # # # # from flask_mail import Message
# # # # # # # from flask import current_app
# # # # # # # from threading import Thread
# # # # # # # import logging
# # # # # # # from database.db_config import get_db_connection
# # # # # # # from utils.email_templates import EmailTemplates
# # # # # # # import traceback

# # # # # # # class EmailService:
# # # # # # #     def __init__(self, mail):
# # # # # # #         self.mail = mail
# # # # # # #         self.base_url = current_app.config.get('BASE_URL', 'http://localhost:3000')
    
# # # # # # #     def log_email(self, user_id, recipient_email, email_type, subject, status, error_message=None):
# # # # # # #         """Log email in database"""
# # # # # # #         try:
# # # # # # #             connection = get_db_connection()
# # # # # # #             cursor = connection.cursor()
# # # # # # #             cursor.execute("""
# # # # # # #                 INSERT INTO email_logs 
# # # # # # #                 (user_id, recipient_email, email_type, subject, status, error_message, sent_at)
# # # # # # #                 VALUES (%s, %s, %s, %s, %s, %s, NOW())
# # # # # # #             """, (user_id, recipient_email, email_type, subject, status, error_message))
# # # # # # #             connection.commit()
# # # # # # #             cursor.close()
# # # # # # #             connection.close()
# # # # # # #         except Exception as e:
# # # # # # #             print(f"⚠️ Failed to log email: {e}")
    
# # # # # # #     def send_async_email(self, msg, user_id, recipient_email, email_type, subject):
# # # # # # #         """Send email asynchronously"""
# # # # # # #         try:
# # # # # # #             with current_app.app_context():
# # # # # # #                 self.mail.send(msg)
# # # # # # #                 print(f"✅ Email sent to {recipient_email}")
# # # # # # #                 self.log_email(user_id, recipient_email, email_type, subject, 'sent')
# # # # # # #         except Exception as e:
# # # # # # #             error_msg = str(e)
# # # # # # #             print(f"❌ Failed to send email: {error_msg}")
# # # # # # #             traceback.print_exc()
# # # # # # #             self.log_email(user_id, recipient_email, email_type, subject, 'failed', error_msg)
    
# # # # # # #     def send_email(self, to_email, subject, html_content, email_type='notification', user_id=None):
# # # # # # #         """Send email with HTML content"""
# # # # # # #         try:
# # # # # # #             msg = Message(
# # # # # # #                 subject=subject,
# # # # # # #                 recipients=[to_email],
# # # # # # #                 html=html_content,
# # # # # # #                 sender=current_app.config.get('FROM_EMAIL', 'noreply@freelancehub.com')
# # # # # # #             )
            
# # # # # # #             print(f"📧 Preparing to send email to {to_email}: {subject}")
            
# # # # # # #             # Send asynchronously
# # # # # # #             Thread(target=self.send_async_email, args=(msg, user_id, to_email, email_type, subject)).start()
# # # # # # #             return True
# # # # # # #         except Exception as e:
# # # # # # #             print(f"❌ Error preparing email: {str(e)}")
# # # # # # #             traceback.print_exc()
# # # # # # #             self.log_email(user_id, to_email, email_type, subject, 'failed', str(e))
# # # # # # #             return False
    
# # # # # # #     def send_application_confirmation(self, to_email, freelancer_name, job_title, company_name, user_id=None):
# # # # # # #         """Send confirmation email to freelancer after applying"""
# # # # # # #         html_content, subject = EmailTemplates.application_confirmation(
# # # # # # #             freelancer_name, job_title, company_name
# # # # # # #         )
# # # # # # #         return self.send_email(to_email, subject, html_content, 'application_received', user_id)
    
# # # # # # #     def send_application_submitted_notification(self, to_email, recruiter_name, freelancer_name, job_title, job_id, application_id, user_id=None):
# # # # # # #         """Send notification to recruiter when someone applies"""
# # # # # # #         html_content, subject = EmailTemplates.application_submitted_notification(
# # # # # # #             recruiter_name, freelancer_name, job_title, job_id, application_id
# # # # # # #         )
# # # # # # #         return self.send_email(to_email, subject, html_content, 'application_received', user_id)

# # # # # # # # Global instance
# # # # # # # email_service = None


# # # # # # # services/email_service.py
# # # # # # from flask_mail import Message
# # # # # # from flask import current_app
# # # # # # from threading import Thread
# # # # # # import logging
# # # # # # from database.db_config import get_db_connection
# # # # # # from utils.email_templates import EmailTemplates
# # # # # # import traceback

# # # # # # class EmailService:
# # # # # #     def __init__(self, mail=None):
# # # # # #         self.mail = mail
# # # # # #         # Don't access current_app here - it will be set when sending emails
# # # # # #         self.base_url = None  # Will be set in app context when sending
    
# # # # # #     def _get_base_url(self):
# # # # # #         """Get base URL from app config safely"""
# # # # # #         if self.base_url is None:
# # # # # #             try:
# # # # # #                 from flask import current_app
# # # # # #                 self.base_url = current_app.config.get('BASE_URL', 'http://localhost:3000')
# # # # # #             except RuntimeError:
# # # # # #                 # Fallback when outside app context
# # # # # #                 self.base_url = 'http://localhost:3000'
# # # # # #         return self.base_url
    
# # # # # #     def log_email(self, user_id, recipient_email, email_type, subject, status, error_message=None):
# # # # # #         """Log email in database"""
# # # # # #         try:
# # # # # #             connection = get_db_connection()
# # # # # #             cursor = connection.cursor()
# # # # # #             cursor.execute("""
# # # # # #                 INSERT INTO email_logs 
# # # # # #                 (user_id, recipient_email, email_type, subject, status, error_message, sent_at)
# # # # # #                 VALUES (%s, %s, %s, %s, %s, %s, NOW())
# # # # # #             """, (user_id, recipient_email, email_type, subject, status, error_message))
# # # # # #             connection.commit()
# # # # # #             cursor.close()
# # # # # #             connection.close()
# # # # # #             print(f"📝 Email logged: {status} - {subject}")
# # # # # #         except Exception as e:
# # # # # #             print(f"⚠️ Failed to log email: {e}")
    
# # # # # #     def send_async_email(self, msg, user_id, recipient_email, email_type, subject):
# # # # # #         """Send email asynchronously"""
# # # # # #         try:
# # # # # #             with current_app.app_context():
# # # # # #                 self.mail.send(msg)
# # # # # #                 print(f"✅ Email sent successfully to {recipient_email}")
# # # # # #                 self.log_email(user_id, recipient_email, email_type, subject, 'sent')
# # # # # #         except Exception as e:
# # # # # #             error_msg = str(e)
# # # # # #             print(f"❌ Failed to send email to {recipient_email}: {error_msg}")
# # # # # #             traceback.print_exc()
# # # # # #             self.log_email(user_id, recipient_email, email_type, subject, 'failed', error_msg)
    
# # # # # #     def send_email(self, to_email, subject, html_content, email_type='notification', user_id=None):
# # # # # #         """Send email with HTML content"""
# # # # # #         try:
# # # # # #             msg = Message(
# # # # # #                 subject=subject,
# # # # # #                 recipients=[to_email],
# # # # # #                 html=html_content,
# # # # # #                 sender=current_app.config.get('FROM_EMAIL', 'noreply@freelancehub.com')
# # # # # #             )
            
# # # # # #             print(f"📧 Queueing email to {to_email}: {subject}")
            
# # # # # #             # Send asynchronously
# # # # # #             Thread(target=self.send_async_email, args=(msg, user_id, to_email, email_type, subject)).start()
# # # # # #             return True
# # # # # #         except Exception as e:
# # # # # #             print(f"❌ Error preparing email: {str(e)}")
# # # # # #             traceback.print_exc()
# # # # # #             self.log_email(user_id, to_email, email_type, subject, 'failed', str(e))
# # # # # #             return False
    
# # # # # #     def send_verification_email(self, to_email, user_name, verification_token, user_id=None):
# # # # # #         """Send email verification"""
# # # # # #         base_url = self._get_base_url()
# # # # # #         html_content, subject = EmailTemplates.email_verification(user_name, verification_token, base_url)
# # # # # #         return self.send_email(to_email, subject, html_content, 'verification', user_id)
    
# # # # # #     def send_application_confirmation(self, to_email, freelancer_name, job_title, company_name, user_id=None):
# # # # # #         """Send confirmation email to freelancer after applying"""
# # # # # #         base_url = self._get_base_url()
# # # # # #         html_content, subject = EmailTemplates.application_confirmation(
# # # # # #             freelancer_name, job_title, company_name, base_url
# # # # # #         )
# # # # # #         return self.send_email(to_email, subject, html_content, 'application_received', user_id)
    
# # # # # #     def send_application_submitted_notification(self, to_email, recruiter_name, freelancer_name, job_title, job_id, application_id, user_id=None):
# # # # # #         """Send notification to recruiter when someone applies"""
# # # # # #         base_url = self._get_base_url()
# # # # # #         html_content, subject = EmailTemplates.application_submitted_notification(
# # # # # #             recruiter_name, freelancer_name, job_title, job_id, application_id, base_url
# # # # # #         )
# # # # # #         return self.send_email(to_email, subject, html_content, 'application_received', user_id)

# # # # # # # Global instance
# # # # # # email_service = None


# # # # # # services/email_service.py
# # # # # from flask_mail import Message
# # # # # from flask import current_app
# # # # # from threading import Thread
# # # # # import logging
# # # # # from database.db_config import get_db_connection
# # # # # from utils.email_templates import EmailTemplates
# # # # # import traceback

# # # # # class EmailService:
# # # # #     def __init__(self, mail=None):
# # # # #         self.mail = mail
# # # # #         self.base_url = None
    
# # # # #     def _get_base_url(self):
# # # # #         """Get base URL from app config safely"""
# # # # #         if self.base_url is None:
# # # # #             try:
# # # # #                 from flask import current_app
# # # # #                 self.base_url = current_app.config.get('BASE_URL', 'http://localhost:3000')
# # # # #             except RuntimeError:
# # # # #                 self.base_url = 'http://localhost:3000'
# # # # #         return self.base_url
    
# # # # #     def log_email(self, user_id, recipient_email, email_type, subject, status, error_message=None):
# # # # #         """Log email in database"""
# # # # #         try:
# # # # #             connection = get_db_connection()
# # # # #             cursor = connection.cursor()
# # # # #             cursor.execute("""
# # # # #                 INSERT INTO email_logs 
# # # # #                 (user_id, recipient_email, email_type, subject, status, error_message, sent_at)
# # # # #                 VALUES (%s, %s, %s, %s, %s, %s, NOW())
# # # # #             """, (user_id, recipient_email, email_type, subject, status, error_message))
# # # # #             connection.commit()
# # # # #             cursor.close()
# # # # #             connection.close()
# # # # #             print(f"📝 Email logged: {status} - {subject}")
# # # # #         except Exception as e:
# # # # #             print(f"⚠️ Failed to log email: {e}")
    
# # # # #     def send_async_email(self, msg, user_id, recipient_email, email_type, subject):
# # # # #         """Send email asynchronously"""
# # # # #         try:
# # # # #             with current_app.app_context():
# # # # #                 print(f"📧 Sending email to {recipient_email}...")
# # # # #                 self.mail.send(msg)
# # # # #                 print(f"✅ Email sent successfully to {recipient_email}")
# # # # #                 self.log_email(user_id, recipient_email, email_type, subject, 'sent')
# # # # #         except Exception as e:
# # # # #             error_msg = str(e)
# # # # #             print(f"❌ Failed to send email to {recipient_email}: {error_msg}")
# # # # #             traceback.print_exc()
# # # # #             self.log_email(user_id, recipient_email, email_type, subject, 'failed', error_msg)
    
# # # # #     def send_email(self, to_email, subject, html_content, email_type='notification', user_id=None):
# # # # #         """Send email with HTML content"""
# # # # #         try:
# # # # #             print(f"📧 Preparing email for {to_email}: {subject}")
            
# # # # #             msg = Message(
# # # # #                 subject=subject,
# # # # #                 recipients=[to_email],
# # # # #                 html=html_content,
# # # # #                 sender=current_app.config.get('FROM_EMAIL', 'noreply@freelancehub.com')
# # # # #             )
            
# # # # #             # Send asynchronously
# # # # #             Thread(target=self.send_async_email, args=(msg, user_id, to_email, email_type, subject)).start()
# # # # #             return True
# # # # #         except Exception as e:
# # # # #             print(f"❌ Error preparing email: {str(e)}")
# # # # #             traceback.print_exc()
# # # # #             self.log_email(user_id, to_email, email_type, subject, 'failed', str(e))
# # # # #             return False
    
# # # # #     def send_application_confirmation(self, to_email, freelancer_name, job_title, company_name, user_id=None):
# # # # #         """Send confirmation email to freelancer after applying"""
# # # # #         base_url = self._get_base_url()
# # # # #         html_content, subject = EmailTemplates.application_confirmation(
# # # # #             freelancer_name, job_title, company_name, base_url
# # # # #         )
# # # # #         return self.send_email(to_email, subject, html_content, 'application_received', user_id)
    
# # # # #     def send_application_submitted_notification(self, to_email, recruiter_name, freelancer_name, job_title, job_id, application_id, user_id=None):
# # # # #         """Send notification to recruiter when someone applies"""
# # # # #         base_url = self._get_base_url()
# # # # #         html_content, subject = EmailTemplates.application_submitted_notification(
# # # # #             recruiter_name, freelancer_name, job_title, job_id, application_id, base_url
# # # # #         )
# # # # #         return self.send_email(to_email, subject, html_content, 'application_received', user_id)

# # # # # # Global instance
# # # # # email_service = None


# # # # # services/email_service.py
# # # # from flask_mail import Message
# # # # from flask import current_app
# # # # from threading import Thread
# # # # import logging
# # # # from database.db_config import get_db_connection
# # # # from utils.email_templates import EmailTemplates
# # # # import traceback

# # # # class EmailService:
# # # #     def __init__(self, mail=None):
# # # #         self.mail = mail
# # # #         self.base_url = None
# # # #         print(f"🔧 EmailService initialized with mail: {mail is not None}")
    
# # # #     def _get_base_url(self):
# # # #         """Get base URL from app config safely"""
# # # #         if self.base_url is None:
# # # #             try:
# # # #                 from flask import current_app
# # # #                 self.base_url = current_app.config.get('BASE_URL', 'http://localhost:3000')
# # # #                 print(f"📌 Base URL set to: {self.base_url}")
# # # #             except RuntimeError:
# # # #                 self.base_url = 'http://localhost:3000'
# # # #                 print(f"📌 Base URL default: {self.base_url}")
# # # #         return self.base_url
    
# # # #     def log_email(self, user_id, recipient_email, email_type, subject, status, error_message=None):
# # # #         """Log email in database"""
# # # #         try:
# # # #             connection = get_db_connection()
# # # #             cursor = connection.cursor()
# # # #             cursor.execute("""
# # # #                 INSERT INTO email_logs 
# # # #                 (user_id, recipient_email, email_type, subject, status, error_message, sent_at)
# # # #                 VALUES (%s, %s, %s, %s, %s, %s, NOW())
# # # #             """, (user_id, recipient_email, email_type, subject, status, error_message))
# # # #             connection.commit()
# # # #             cursor.close()
# # # #             connection.close()
# # # #             print(f"📝 Email logged: {status} - {subject}")
# # # #         except Exception as e:
# # # #             print(f"⚠️ Failed to log email: {e}")
    
# # # #     def send_async_email(self, msg, user_id, recipient_email, email_type, subject):
# # # #         """Send email asynchronously"""
# # # #         try:
# # # #             with current_app.app_context():
# # # #                 print(f"📧 Attempting to send email to {recipient_email}...")
# # # #                 print(f"📧 Mail server: {current_app.config.get('MAIL_SERVER')}")
# # # #                 print(f"📧 Mail username: {current_app.config.get('MAIL_USERNAME')}")
                
# # # #                 self.mail.send(msg)
# # # #                 print(f"✅ Email sent successfully to {recipient_email}")
# # # #                 self.log_email(user_id, recipient_email, email_type, subject, 'sent')
# # # #         except Exception as e:
# # # #             error_msg = str(e)
# # # #             print(f"❌ Failed to send email to {recipient_email}: {error_msg}")
# # # #             print(f"❌ Error type: {type(e).__name__}")
# # # #             traceback.print_exc()
# # # #             self.log_email(user_id, recipient_email, email_type, subject, 'failed', error_msg)
    
# # # #     def send_email(self, to_email, subject, html_content, email_type='notification', user_id=None):
# # # #         """Send email with HTML content"""
# # # #         try:
# # # #             print(f"📧 Preparing email for {to_email}: {subject}")
# # # #             print(f"📧 HTML content length: {len(html_content)} chars")
            
# # # #             # Get sender email from config
# # # #             from flask import current_app
# # # #             sender = current_app.config.get('FROM_EMAIL', 'noreply@freelancehub.com')
# # # #             print(f"📧 Sender: {sender}")
            
# # # #             msg = Message(
# # # #                 subject=subject,
# # # #                 recipients=[to_email],
# # # #                 html=html_content,
# # # #                 sender=sender
# # # #             )
            
# # # #             # Send asynchronously
# # # #             print(f"📧 Starting async thread for email to {to_email}")
# # # #             Thread(target=self.send_async_email, args=(msg, user_id, to_email, email_type, subject)).start()
# # # #             print(f"📧 Async thread started for {to_email}")
# # # #             return True
# # # #         except Exception as e:
# # # #             print(f"❌ Error preparing email: {str(e)}")
# # # #             print(f"❌ Error type: {type(e).__name__}")
# # # #             traceback.print_exc()
# # # #             self.log_email(user_id, to_email, email_type, subject, 'failed', str(e))
# # # #             return False
    
# # # #     def send_application_confirmation(self, to_email, freelancer_name, job_title, company_name, user_id=None):
# # # #         """Send confirmation email to freelancer after applying"""
# # # #         print(f"📧 send_application_confirmation called for {to_email}")
# # # #         base_url = self._get_base_url()
# # # #         html_content, subject = EmailTemplates.application_confirmation(
# # # #             freelancer_name, job_title, company_name, base_url
# # # #         )
# # # #         return self.send_email(to_email, subject, html_content, 'application_received', user_id)
    
# # # #     def send_application_submitted_notification(self, to_email, recruiter_name, freelancer_name, job_title, job_id, application_id, user_id=None):
# # # #         """Send notification to recruiter when someone applies"""
# # # #         print(f"📧 send_application_submitted_notification called for {to_email}")
# # # #         base_url = self._get_base_url()
# # # #         html_content, subject = EmailTemplates.application_submitted_notification(
# # # #             recruiter_name, freelancer_name, job_title, job_id, application_id, base_url
# # # #         )
# # # #         return self.send_email(to_email, subject, html_content, 'application_received', user_id)

# # # # # Global instance
# # # # email_service = None

# # # # services/email_service.py
# # # from flask_mail import Message
# # # from flask import current_app
# # # from threading import Thread
# # # import logging
# # # from database.db_config import get_db_connection
# # # from utils.email_templates import EmailTemplates
# # # import traceback

# # # class EmailService:
# # #     def __init__(self, mail=None):
# # #         self.mail = mail
# # #         self.base_url = None
# # #         print(f"🔧 EmailService initialized with mail: {mail is not None}")
    
# # #     def _get_base_url(self):
# # #         """Get base URL from app config safely"""
# # #         if self.base_url is None:
# # #             try:
# # #                 from flask import current_app
# # #                 self.base_url = current_app.config.get('BASE_URL', 'http://localhost:3000')
# # #             except RuntimeError:
# # #                 self.base_url = 'http://localhost:3000'
# # #         return self.base_url
    
# # #     def log_email(self, user_id, recipient_email, email_type, subject, status, error_message=None):
# # #         """Log email in database"""
# # #         try:
# # #             connection = get_db_connection()
# # #             cursor = connection.cursor()
# # #             cursor.execute("""
# # #                 INSERT INTO email_logs 
# # #                 (user_id, recipient_email, email_type, subject, status, error_message, sent_at)
# # #                 VALUES (%s, %s, %s, %s, %s, %s, NOW())
# # #             """, (user_id, recipient_email, email_type, subject, status, error_message))
# # #             connection.commit()
# # #             cursor.close()
# # #             connection.close()
# # #             print(f"📝 Email logged: {status} - {subject}")
# # #         except Exception as e:
# # #             print(f"⚠️ Failed to log email: {e}")
    
# # #     def send_async_email(self, msg, user_id, recipient_email, email_type, subject):
# # #         """Send email asynchronously"""
# # #         try:
# # #             with current_app.app_context():
# # #                 print(f"📧 Sending email to {recipient_email}...")
# # #                 self.mail.send(msg)
# # #                 print(f"✅ Email sent successfully to {recipient_email}")
# # #                 self.log_email(user_id, recipient_email, email_type, subject, 'sent')
# # #         except Exception as e:
# # #             error_msg = str(e)
# # #             print(f"❌ Failed to send email to {recipient_email}: {error_msg}")
# # #             traceback.print_exc()
# # #             self.log_email(user_id, recipient_email, email_type, subject, 'failed', error_msg)
    
# # #     def send_email(self, to_email, subject, html_content, email_type='notification', user_id=None):
# # #         """Send email with HTML content"""
# # #         try:
# # #             print(f"📧 Preparing email for {to_email}: {subject}")
            
# # #             # Get sender email from config
# # #             from flask import current_app
# # #             sender = current_app.config.get('FROM_EMAIL', 'noreply@freelancehub.com')
            
# # #             msg = Message(
# # #                 subject=subject,
# # #                 recipients=[to_email],
# # #                 html=html_content,
# # #                 sender=sender
# # #             )
            
# # #             # Send asynchronously
# # #             Thread(target=self.send_async_email, args=(msg, user_id, to_email, email_type, subject)).start()
# # #             return True
# # #         except Exception as e:
# # #             print(f"❌ Error preparing email: {str(e)}")
# # #             traceback.print_exc()
# # #             self.log_email(user_id, to_email, email_type, subject, 'failed', str(e))
# # #             return False
    
# # #     def send_application_confirmation(self, to_email, freelancer_name, job_title, company_name, user_id=None):
# # #         """Send confirmation email to freelancer after applying"""
# # #         print(f"📧 send_application_confirmation called for {to_email}")
# # #         base_url = self._get_base_url()
# # #         html_content, subject = EmailTemplates.application_confirmation(
# # #             freelancer_name, job_title, company_name, base_url
# # #         )
# # #         return self.send_email(to_email, subject, html_content, 'application_received', user_id)
    
# # #     def send_application_submitted_notification(self, to_email, recruiter_name, freelancer_name, job_title, job_id, application_id, user_id=None):
# # #         """Send notification to recruiter when someone applies"""
# # #         print(f"📧 send_application_submitted_notification called for {to_email}")
# # #         base_url = self._get_base_url()
# # #         html_content, subject = EmailTemplates.application_submitted_notification(
# # #             recruiter_name, freelancer_name, job_title, job_id, application_id, base_url
# # #         )
# # #         return self.send_email(to_email, subject, html_content, 'application_received', user_id)
    
# # #     def send_job_posted_notification(self, to_email, recruiter_name, job_title, job_id, user_id=None):
# # #         """Send notification to recruiter when job is posted"""
# # #         print(f"📧 send_job_posted_notification called for {to_email}")
# # #         base_url = self._get_base_url()
# # #         html_content, subject = EmailTemplates.job_posted_notification(
# # #             recruiter_name, job_title, job_id, base_url
# # #         )
# # #         return self.send_email(to_email, subject, html_content, 'job_posted', user_id)
    
# # #     def send_application_status_update(self, to_email, freelancer_name, job_title, status, recruiter_notes=None, job_id=None, user_id=None):
# # #         """Send status update to freelancer"""
# # #         print(f"📧 send_application_status_update called for {to_email}")
# # #         base_url = self._get_base_url()
# # #         html_content, subject = EmailTemplates.application_status_update(
# # #             freelancer_name, job_title, status, recruiter_notes, job_id, base_url
# # #         )
# # #         return self.send_email(to_email, subject, html_content, 'application_status', user_id)


# # # services/email_service.py
# # from flask_mail import Message
# # from flask import current_app
# # import traceback

# # class EmailService:
# #     def __init__(self, mail=None):
# #         self.mail = mail
    
# #     def send_email(self, to_email, subject, html_content, user_id=None):
# #         """Base method to send emails"""
# #         try:
# #             if not self.mail:
# #                 print("❌ Mail object not initialized")
# #                 return False
            
# #             msg = Message(
# #                 subject=subject,
# #                 recipients=[to_email],
# #                 html=html_content,
# #                 sender=current_app.config.get('FROM_EMAIL')
# #             )
            
# #             self.mail.send(msg)
# #             print(f"✅ Email sent to {to_email}")
            
# #             # Log to database if user_id provided
# #             if user_id:
# #                 self._log_email(user_id, to_email, subject, 'sent')
            
# #             return True
# #         except Exception as e:
# #             print(f"❌ Failed to send email: {e}")
# #             traceback.print_exc()
# #             return False
    
# #     def _log_email(self, user_id, recipient_email, subject, status):
# #         """Log email to database"""
# #         try:
# #             from database.db_config import get_db_connection
# #             connection = get_db_connection()
# #             cursor = connection.cursor()
# #             cursor.execute("""
# #                 INSERT INTO email_logs 
# #                 (user_id, recipient_email, email_type, subject, status, sent_at)
# #                 VALUES (%s, %s, %s, %s, %s, NOW())
# #             """, (user_id, recipient_email, 'notification', subject, status))
# #             connection.commit()
# #             cursor.close()
# #             connection.close()
# #         except Exception as e:
# #             print(f"⚠️ Failed to log email: {e}")
    
# #     def send_application_confirmation(self, to_email, freelancer_name, job_title, company_name, user_id):
# #         """Send confirmation to freelancer"""
# #         subject = f"Application Confirmed: {job_title}"
# #         html_content = f"""
# #         <html>
# #             <body style="font-family: Arial, sans-serif;">
# #                 <h2>Application Submitted Successfully!</h2>
# #                 <p>Hello {freelancer_name},</p>
# #                 <p>Your application for <strong>{job_title}</strong> at <strong>{company_name}</strong> has been submitted.</p>
# #                 <p>The recruiter will review your application and contact you soon.</p>
# #                 <br>
# #                 <p>Best regards,<br>FreelanceHub Team</p>
# #             </body>
# #         </html>
# #         """
# #         return self.send_email(to_email, subject, html_content, user_id)
    
# #     def send_application_submitted_notification(self, to_email, recruiter_name, freelancer_name, job_title, job_id, application_id, user_id):
# #         """Send notification to recruiter"""
# #         subject = f"New Application: {freelancer_name} applied to {job_title}"
# #         html_content = f"""
# #         <html>
# #             <body style="font-family: Arial, sans-serif;">
# #                 <h2>New Job Application Received</h2>
# #                 <p>Hello {recruiter_name},</p>
# #                 <p><strong>{freelancer_name}</strong> has applied for your job: <strong>{job_title}</strong></p>
# #                 <p>View the application in your recruiter dashboard.</p>
# #                 <br>
# #                 <p>Best regards,<br>FreelanceHub Team</p>
# #             </body>
# #         </html>
# #         """
# #         return self.send_email(to_email, subject, html_content, user_id)



# from flask_mail import Message
# from flask import current_app
# import traceback

# class EmailService:
#     def __init__(self, mail=None):
#         self.mail = mail

#     def send_email(self, to_email, subject, html_content, user_id=None):
#         """Base method to send emails."""
#         try:
#             if not self.mail:
#                 print("❌ Mail object not initialized")
#                 return False

#             msg = Message(
#                 subject=subject,
#                 recipients=[to_email],
#                 html=html_content,
#                 sender=current_app.config.get('FROM_EMAIL')
#             )

#             self.mail.send(msg)
#             print(f"✅ Email sent to {to_email}")

#             if user_id:
#                 self._log_email(user_id, to_email, subject, 'sent')
#             return True
#         except Exception as e:
#             print(f"❌ Failed to send email: {e}")
#             traceback.print_exc()
#             return False

#     def _log_email(self, user_id, recipient_email, subject, status):
#         try:
#             from database.db_config import get_db_connection
#             conn = get_db_connection()
#             cur = conn.cursor()
#             cur.execute("""
#                 INSERT INTO email_logs (user_id, recipient_email, email_type, subject, status, sent_at)
#                 VALUES (%s, %s, %s, %s, %s, NOW())
#             """, (user_id, recipient_email, 'notification', subject, status))
#             conn.commit()
#             cur.close()
#             conn.close()
#         except Exception as e:
#             print(f"⚠️ Failed to log email: {e}")

#     # ==================== Responsive Email Wrapper ====================
#     def _base_template(self, inner_content):
#         return f"""
#         <!DOCTYPE html>
#         <html>
#         <head>
#             <meta charset="UTF-8">
#             <meta name="viewport" content="width=device-width, initial-scale=1.0">
#             <style>
#                 body {{ margin: 0; padding: 0; background-color: #f3f4f6; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; }}
#                 table {{ border-collapse: collapse; width: 100%; }}
#                 @media only screen and (max-width: 600px) {{
#                     .container {{ width: 100% !important; }}
#                     .content {{ padding: 20px !important; }}
#                     .button {{ width: 100% !important; display: block !important; text-align: center !important; }}
#                 }}
#             </style>
#         </head>
#         <body style="margin:0; padding:20px 0; background:#f3f4f6;">
#             <table align="center" border="0" cellpadding="0" cellspacing="0" width="100%" style="max-width:600px;">
#                 <tr>
#                     <td align="center" style="padding:20px 0;">
#                         <table width="100%" border="0" cellpadding="0" cellspacing="0" style="background:#ffffff; border-radius:16px; overflow:hidden; box-shadow:0 10px 25px -5px rgba(0,0,0,0.1);">
#                             <tr><td style="background:linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding:30px 20px; text-align:center;"><h1 style="color:white; margin:0; font-size:28px; font-weight:700;">⚡ FreelanceHub</h1><p style="color:rgba(255,255,255,0.9); margin:10px 0 0;">Your Gateway to Freelance Success</p></td></tr>
#                             <tr><td style="padding:30px 20px; background:#ffffff;" class="content">{inner_content}</td></tr>
#                             <tr><td style="background:#f9fafb; padding:20px; text-align:center; border-top:1px solid #e5e7eb;"><p style="color:#6b7280; font-size:14px; margin:5px 0;">© 2026 FreelanceHub. All rights reserved.</p><p style="color:#9ca3af; font-size:12px; margin:10px 0 0;">This email was sent to you because you're a member of FreelanceHub.<br>If you didn't expect this email, please ignore it.</p></td></tr>
#                         </table>
#                     </td>
#                 </tr>
#             </table>
#         </body>
#         </html>
#         """

#     # ==================== Registration Emails ====================
#     def send_verification_email(self, to_email, user_name, verification_link, user_id=None):
#         subject = "Verify Your Email - FreelanceHub"
#         inner = f"""
#         <div style="text-align:center; margin-bottom:20px;"><div style="font-size:48px; margin-bottom:10px;">🔐</div><h2 style="color:#1e293b; font-size:28px; font-weight:700;">Welcome, {user_name}!</h2></div>
#         <p style="font-size:16px; color:#475569; line-height:1.6; margin-bottom:20px;">Thank you for joining FreelanceHub. Please verify your email address to activate your account.</p>
#         <div style="text-align:center; margin:30px 0;"><a href="{verification_link}" style="background:linear-gradient(135deg, #667eea, #764ba2); color:white; padding:16px 40px; text-decoration:none; border-radius:50px; font-weight:600; display:inline-block;">Verify Email</a></div>
#         <p style="font-size:14px; color:#64748b; text-align:center;">This link expires in 24 hours. If you didn't create an account, please ignore this email.</p>
#         """
#         return self.send_email(to_email, subject, self._base_template(inner), user_id)

#     def send_welcome_email(self, to_email, user_name, user_type, user_id=None):
#         subject = f"Welcome to FreelanceHub, {user_name}! 🎉"
#         next_steps = "Browse jobs, complete your profile, and start applying!" if user_type=='freelancer' else "Post jobs, review applications, and find the perfect freelancer!"
#         inner = f"""
#         <div style="text-align:center; margin-bottom:20px;"><div style="font-size:48px; margin-bottom:10px;">🎉</div><h2 style="color:#1e293b; font-size:28px; font-weight:700;">Email Verified Successfully!</h2></div>
#         <p style="font-size:16px; color:#475569; line-height:1.6; margin-bottom:20px;">Hi <strong style="color:#667eea;">{user_name}</strong>,</p>
#         <p style="font-size:16px; color:#475569; line-height:1.6; margin-bottom:20px;">Your account is now active. {next_steps}</p>
#         <div style="background:#f8fafc; border-left:4px solid #667eea; padding:20px; border-radius:12px; margin:20px 0;"><h3 style="color:#1e293b; margin-bottom:10px;">🚀 Get Started</h3><ul style="color:#475569; margin:0 0 0 20px;"><li>Complete your profile to attract opportunities</li><li>Browse jobs and submit applications</li><li>Get notified when your status changes</li></ul></div>
#         <div style="text-align:center; margin:30px 0;"><a href="{current_app.config['BASE_URL']}/dashboard" style="background:linear-gradient(135deg, #10b981, #059669); color:white; padding:16px 40px; text-decoration:none; border-radius:50px; font-weight:600; display:inline-block;">Go to Dashboard</a></div>
#         """
#         return self.send_email(to_email, subject, self._base_template(inner), user_id)

#     # ==================== Job Posting ====================
#     def send_job_posted_notification(self, to_email, recruiter_name, job_title, job_id, user_id=None):
#         subject = f"✅ Job Posted: {job_title}"
#         job_link = f"{current_app.config['BASE_URL']}/recruiter/jobs/{job_id}"
#         inner = f"""
#         <h2 style="color:#1e293b; margin-bottom:20px;">Job Posted Successfully!</h2>
#         <p style="font-size:16px; color:#475569; line-height:1.6; margin-bottom:20px;">Hi <strong style="color:#667eea;">{recruiter_name}</strong>,</p>
#         <p style="font-size:16px; color:#475569; line-height:1.6; margin-bottom:20px;">Your job <strong>"{job_title}"</strong> is now live on FreelanceHub.</p>
#         <div style="background:#f0f9ff; border-left:4px solid #0ea5e9; padding:20px; border-radius:12px; margin:20px 0;"><h3 style="color:#0369a1; margin-bottom:10px;">📊 What's Next?</h3><ul style="color:#475569; margin-left:20px;"><li>Freelancers will start applying</li><li>You'll receive email notifications for each application</li><li>Review and shortlist candidates from your dashboard</li></ul></div>
#         <div style="text-align:center; margin:30px 0;"><a href="{job_link}" style="background:linear-gradient(135deg, #0ea5e9, #2563eb); color:white; padding:16px 40px; text-decoration:none; border-radius:50px; font-weight:600; display:inline-block;">View Your Job</a></div>
#         """
#         return self.send_email(to_email, subject, self._base_template(inner), user_id)

#     # ==================== Application Emails ====================
#     def send_application_confirmation(self, to_email, freelancer_name, job_title, company_name, user_id):
#         subject = f"✅ Application Confirmed: {job_title}"
#         inner = f"""
#         <div style="text-align:center; margin-bottom:20px;"><div style="font-size:48px; margin-bottom:10px;">🎉</div><h2 style="color:#1e293b; font-size:28px; font-weight:700;">Application Submitted!</h2></div>
#         <p style="font-size:16px; color:#475569; line-height:1.6; margin-bottom:20px;">Hi <strong style="color:#667eea;">{freelancer_name}</strong>,</p>
#         <p style="font-size:16px; color:#475569; line-height:1.6; margin-bottom:20px;">Your application for <strong>"{job_title}"</strong> at <strong>{company_name}</strong> has been submitted.</p>
#         <div style="background:#f8fafc; border-left:4px solid #667eea; padding:20px; border-radius:12px; margin:20px 0;"><h3 style="color:#1e293b; margin-bottom:10px;">✅ What happens next?</h3><ul style="color:#475569; margin:0 0 0 20px;"><li>The recruiter will review your application</li><li>You'll receive an email when they update the status</li><li>You can track all applications in your dashboard</li></ul></div>
#         <div style="text-align:center; margin:30px 0;"><a href="{current_app.config['BASE_URL']}/freelancer/applications" style="background:linear-gradient(135deg, #667eea, #764ba2); color:white; padding:16px 40px; text-decoration:none; border-radius:50px; font-weight:600; display:inline-block;">Track Your Application</a></div>
#         <p style="font-size:16px; color:#475569; text-align:center;">Good luck! 🤞</p>
#         """
#         return self.send_email(to_email, subject, self._base_template(inner), user_id)

#     def send_application_submitted_notification(self, application_id):
#         """Send notification to recruiter – fetches all data from DB."""
#         try:
#             from database.models import JobApplication, Job, User
#             app = JobApplication.get_by_id(application_id)
#             if not app:
#                 print(f"❌ Application {application_id} not found")
#                 return False
#             job = Job.get_by_id(app['job_id'])
#             freelancer = User.find_by_id(app['freelancer_id'])
#             recruiter = User.find_by_id(job['recruiter_id'])
#             if not all([job, freelancer, recruiter]):
#                 return False

#             to_email = recruiter['email']
#             recruiter_name = f"{recruiter['first_name']} {recruiter['last_name']}"
#             freelancer_name = f"{freelancer['first_name']} {freelancer['last_name']}"
#             job_title = job['title']
#             user_id = recruiter['id']

#             subject = f"New Application: {freelancer_name} applied to {job_title}"
#             inner = f"""
#             <div style="text-align:center; margin-bottom:20px;"><div style="font-size:48px; margin-bottom:10px;">📬</div><h2 style="color:#1e293b; font-size:28px; font-weight:700;">New Application Received!</h2></div>
#             <p style="font-size:16px; color:#475569; line-height:1.6; margin-bottom:20px;">Hi <strong style="color:#667eea;">{recruiter_name}</strong>,</p>
#             <p style="font-size:16px; color:#475569; line-height:1.6; margin-bottom:20px;"><span style="font-size:20px; font-weight:600; color:#667eea;">{freelancer_name}</span> has just applied to your job:<br><strong>"{job_title}"</strong></p>
#             <div style="background:#f0fdf4; border-left:4px solid #22c55e; padding:20px; border-radius:12px; margin:20px 0;"><div style="display:flex; align-items:center; gap:15px;"><div style="width:60px; height:60px; background:linear-gradient(135deg, #22c55e, #16a34a); border-radius:50%; display:flex; align-items:center; justify-content:center; color:white; font-size:24px;">👤</div><div><h3 style="color:#166534; margin-bottom:5px;">{freelancer_name}</h3><p style="color:#475569; margin:0;">Applied just now</p></div></div></div>
#             <div style="text-align:center; margin:30px 0;"><a href="{current_app.config['BASE_URL']}/recruiter/jobs/{job['id']}/applications" style="background:linear-gradient(135deg, #22c55e, #16a34a); color:white; padding:16px 40px; text-decoration:none; border-radius:50px; font-weight:600; display:inline-block;">👁️ Review Application</a></div>
#             <div style="background:#fef9c3; border-left:4px solid #eab308; padding:20px; border-radius:8px; margin:20px 0;"><p style="margin:0; color:#854d0e; font-size:14px;"><strong>⏰ Time is important!</strong> Review applications promptly to secure the best talent.</p></div>
#             """
#             return self.send_email(to_email, subject, self._base_template(inner), user_id)
#         except Exception as e:
#             traceback.print_exc()
#             return False

#     def send_application_status_update(self, to_email, freelancer_name, job_title, status, recruiter_notes=None, job_id=None, user_id=None):
#         status_display = status.title()
#         subject = f"📋 Application {status_display}: {job_title}"
#         notes_html = f'<div style="background:#f8fafc; border-left:4px solid #667eea; padding:15px; margin:20px 0; border-radius:8px;"><p style="margin:0 0 5px; color:#334155; font-weight:600;">📝 Recruiter\'s Note:</p><p style="margin:0; color:#475569;">{recruiter_notes}</p></div>' if recruiter_notes else ''
#         inner = f"""
#         <div style="text-align:center; margin-bottom:20px;"><div style="font-size:48px; margin-bottom:10px;">📋</div><h2 style="color:#1e293b; font-size:28px; font-weight:700;">Application {status_display}</h2></div>
#         <p style="font-size:16px; color:#475569; line-height:1.6; margin-bottom:20px;">Hi <strong style="color:#667eea;">{freelancer_name}</strong>,</p>
#         <p style="font-size:16px; color:#475569; line-height:1.6; margin-bottom:20px;">Your application for <strong>"{job_title}"</strong> is now <strong>{status_display}</strong>.</p>
#         {notes_html}
#         <p style="font-size:16px; color:#475569; line-height:1.6; margin-top:20px;">Check your dashboard for more details.</p>
#         <div style="text-align:center; margin:30px 0;"><a href="{current_app.config['BASE_URL']}/freelancer/applications" style="background:linear-gradient(135deg, #667eea, #764ba2); color:white; padding:16px 40px; text-decoration:none; border-radius:50px; font-weight:600; display:inline-block;">View My Applications</a></div>
#         """
#         return self.send_email(to_email, subject, self._base_template(inner), user_id)


# # Global placeholder – will be set in app.py
# email_service = None
from flask_mail import Message
from flask import current_app
import traceback

class EmailService:
    def __init__(self, mail=None):
        self.mail = mail

    def send_email(self, to_email, subject, html_content, user_id=None):
        """Base method to send emails."""
        try:
            if not self.mail:
                print("❌ Mail object not initialized")
                return False

            msg = Message(
                subject=subject,
                recipients=[to_email],
                html=html_content,
                sender=current_app.config.get('FROM_EMAIL')
            )

            self.mail.send(msg)
            print(f"✅ Email sent to {to_email}")

            if user_id:
                self._log_email(user_id, to_email, subject, 'sent')
            return True
        except Exception as e:
            print(f"❌ Failed to send email: {e}")
            traceback.print_exc()
            return False

    def _log_email(self, user_id, recipient_email, subject, status):
        try:
            from database.db_config import get_db_connection
            conn = get_db_connection()
            cur = conn.cursor()
            cur.execute("""
                INSERT INTO email_logs (user_id, recipient_email, email_type, subject, status, sent_at)
                VALUES (%s, %s, %s, %s, %s, NOW())
            """, (user_id, recipient_email, 'notification', subject, status))
            conn.commit()
            cur.close()
            conn.close()
        except Exception as e:
            print(f"⚠️ Failed to log email: {e}")

    # ==================== Responsive Email Wrapper ====================
    def _base_template(self, inner_content):
        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <style>
                body {{ margin: 0; padding: 0; background-color: #f3f4f6; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; }}
                table {{ border-collapse: collapse; width: 100%; }}
                @media only screen and (max-width: 600px) {{
                    .container {{ width: 100% !important; }}
                    .content {{ padding: 20px !important; }}
                    .button {{ width: 100% !important; display: block !important; text-align: center !important; }}
                }}
            </style>
        </head>
        <body style="margin:0; padding:20px 0; background:#f3f4f6;">
            <table align="center" border="0" cellpadding="0" cellspacing="0" width="100%" style="max-width:600px;">
                <tr>
                    <td align="center" style="padding:20px 0;">
                        <table width="100%" border="0" cellpadding="0" cellspacing="0" style="background:#ffffff; border-radius:16px; overflow:hidden; box-shadow:0 10px 25px -5px rgba(0,0,0,0.1);">
                            <tr><td style="background:linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding:30px 20px; text-align:center;"><h1 style="color:white; margin:0; font-size:28px; font-weight:700;">⚡ FreelanceHub</h1><p style="color:rgba(255,255,255,0.9); margin:10px 0 0;">Your Gateway to Freelance Success</p></td></tr>
                            <tr><td style="padding:30px 20px; background:#ffffff;" class="content">{inner_content}</td></tr>
                            <tr><td style="background:#f9fafb; padding:20px; text-align:center; border-top:1px solid #e5e7eb;"><p style="color:#6b7280; font-size:14px; margin:5px 0;">© 2026 FreelanceHub. All rights reserved.</p><p style="color:#9ca3af; font-size:12px; margin:10px 0 0;">This email was sent to you because you're a member of FreelanceHub.<br>If you didn't expect this email, please ignore it.</p></td></tr>
                        </table>
                    </td>
                </tr>
            </table>
        </body>
        </html>
        """

    # ==================== Registration Emails ====================
    def send_verification_email(self, to_email, user_name, verification_link, user_id=None):
        subject = "Verify Your Email - FreelanceHub"
        inner = f"""
        <div style="text-align:center; margin-bottom:20px;"><div style="font-size:48px; margin-bottom:10px;">🔐</div><h2 style="color:#1e293b; font-size:28px; font-weight:700;">Welcome, {user_name}!</h2></div>
        <p style="font-size:16px; color:#475569; line-height:1.6; margin-bottom:20px;">Thank you for joining FreelanceHub. Please verify your email address to activate your account.</p>
        <div style="text-align:center; margin:30px 0;"><a href="{verification_link}" style="background:linear-gradient(135deg, #667eea, #764ba2); color:white; padding:16px 40px; text-decoration:none; border-radius:50px; font-weight:600; display:inline-block;">Verify Email</a></div>
        <p style="font-size:14px; color:#64748b; text-align:center;">This link expires in 24 hours. If you didn't create an account, please ignore this email.</p>
        """
        return self.send_email(to_email, subject, self._base_template(inner), user_id)

    def send_welcome_email(self, to_email, user_name, user_type, user_id=None):
        subject = f"Welcome to FreelanceHub, {user_name}! 🎉"
        next_steps = "Browse jobs, complete your profile, and start applying!" if user_type=='freelancer' else "Post jobs, review applications, and find the perfect freelancer!"
        inner = f"""
        <div style="text-align:center; margin-bottom:20px;"><div style="font-size:48px; margin-bottom:10px;">🎉</div><h2 style="color:#1e293b; font-size:28px; font-weight:700;">Email Verified Successfully!</h2></div>
        <p style="font-size:16px; color:#475569; line-height:1.6; margin-bottom:20px;">Hi <strong style="color:#667eea;">{user_name}</strong>,</p>
        <p style="font-size:16px; color:#475569; line-height:1.6; margin-bottom:20px;">Your account is now active. {next_steps}</p>
        <div style="background:#f8fafc; border-left:4px solid #667eea; padding:20px; border-radius:12px; margin:20px 0;"><h3 style="color:#1e293b; margin-bottom:10px;">🚀 Get Started</h3><ul style="color:#475569; margin:0 0 0 20px;"><li>Complete your profile to attract opportunities</li><li>Browse jobs and submit applications</li><li>Get notified when your status changes</li></ul></div>
        <div style="text-align:center; margin:30px 0;"><a href="{current_app.config['BASE_URL']}/dashboard" style="background:linear-gradient(135deg, #10b981, #059669); color:white; padding:16px 40px; text-decoration:none; border-radius:50px; font-weight:600; display:inline-block;">Go to Dashboard</a></div>
        """
        return self.send_email(to_email, subject, self._base_template(inner), user_id)

    # ==================== Job Posting ====================
    def send_job_posted_notification(self, to_email, recruiter_name, job_title, job_id, user_id=None):
        subject = f"✅ Job Posted: {job_title}"
        job_link = f"{current_app.config['BASE_URL']}/recruiter/jobs/{job_id}"
        inner = f"""
        <h2 style="color:#1e293b; margin-bottom:20px;">Job Posted Successfully!</h2>
        <p style="font-size:16px; color:#475569; line-height:1.6; margin-bottom:20px;">Hi <strong style="color:#667eea;">{recruiter_name}</strong>,</p>
        <p style="font-size:16px; color:#475569; line-height:1.6; margin-bottom:20px;">Your job <strong>"{job_title}"</strong> is now live on FreelanceHub.</p>
        <div style="background:#f0f9ff; border-left:4px solid #0ea5e9; padding:20px; border-radius:12px; margin:20px 0;"><h3 style="color:#0369a1; margin-bottom:10px;">📊 What's Next?</h3><ul style="color:#475569; margin-left:20px;"><li>Freelancers will start applying</li><li>You'll receive email notifications for each application</li><li>Review and shortlist candidates from your dashboard</li></ul></div>
        <div style="text-align:center; margin:30px 0;"><a href="{job_link}" style="background:linear-gradient(135deg, #0ea5e9, #2563eb); color:white; padding:16px 40px; text-decoration:none; border-radius:50px; font-weight:600; display:inline-block;">View Your Job</a></div>
        """
        return self.send_email(to_email, subject, self._base_template(inner), user_id)

    # ==================== Application Emails ====================
    def send_application_confirmation(self, to_email, freelancer_name, job_title, company_name, user_id):
        subject = f"✅ Application Confirmed: {job_title}"
        inner = f"""
        <div style="text-align:center; margin-bottom:20px;"><div style="font-size:48px; margin-bottom:10px;">🎉</div><h2 style="color:#1e293b; font-size:28px; font-weight:700;">Application Submitted!</h2></div>
        <p style="font-size:16px; color:#475569; line-height:1.6; margin-bottom:20px;">Hi <strong style="color:#667eea;">{freelancer_name}</strong>,</p>
        <p style="font-size:16px; color:#475569; line-height:1.6; margin-bottom:20px;">Your application for <strong>"{job_title}"</strong> at <strong>{company_name}</strong> has been submitted.</p>
        <div style="background:#f8fafc; border-left:4px solid #667eea; padding:20px; border-radius:12px; margin:20px 0;"><h3 style="color:#1e293b; margin-bottom:10px;">✅ What happens next?</h3><ul style="color:#475569; margin:0 0 0 20px;"><li>The recruiter will review your application</li><li>You'll receive an email when they update the status</li><li>You can track all applications in your dashboard</li></ul></div>
        <div style="text-align:center; margin:30px 0;"><a href="{current_app.config['BASE_URL']}/freelancer/applications" style="background:linear-gradient(135deg, #667eea, #764ba2); color:white; padding:16px 40px; text-decoration:none; border-radius:50px; font-weight:600; display:inline-block;">Track Your Application</a></div>
        <p style="font-size:16px; color:#475569; text-align:center;">Good luck! 🤞</p>
        """
        return self.send_email(to_email, subject, self._base_template(inner), user_id)

    def send_application_submitted_notification(self, application_id):
        
        """Send notification to recruiter – fetches all data from DB."""
        try:
            from database.models import JobApplication, Job, User
            app = JobApplication.get_by_id(application_id)
            if not app:
                print(f"❌ Application {application_id} not found")
                return False
            job = Job.get_by_id(app['job_id'])
            freelancer = User.find_by_id(app['freelancer_id'])
            recruiter = User.find_by_id(job['recruiter_id'])
            if not all([job, freelancer, recruiter]):
                return False

            to_email = recruiter['email']
            recruiter_name = f"{recruiter['first_name']} {recruiter['last_name']}"
            freelancer_name = f"{freelancer['first_name']} {freelancer['last_name']}"
            job_title = job['title']
            user_id = recruiter['id']

            subject = f"New Application: {freelancer_name} applied to {job_title}"
            inner = f"""
            <div style="text-align:center; margin-bottom:20px;"><div style="font-size:48px; margin-bottom:10px;">📬</div><h2 style="color:#1e293b; font-size:28px; font-weight:700;">New Application Received!</h2></div>
            <p style="font-size:16px; color:#475569; line-height:1.6; margin-bottom:20px;">Hi <strong style="color:#667eea;">{recruiter_name}</strong>,</p>
            <p style="font-size:16px; color:#475569; line-height:1.6; margin-bottom:20px;"><span style="font-size:20px; font-weight:600; color:#667eea;">{freelancer_name}</span> has just applied to your job:<br><strong>"{job_title}"</strong></p>
            <div style="background:#f0fdf4; border-left:4px solid #22c55e; padding:20px; border-radius:12px; margin:20px 0;"><div style="display:flex; align-items:center; gap:15px;"><div style="width:60px; height:60px; background:linear-gradient(135deg, #22c55e, #16a34a); border-radius:50%; display:flex; align-items:center; justify-content:center; color:white; font-size:24px;">👤</div><div><h3 style="color:#166534; margin-bottom:5px;">{freelancer_name}</h3><p style="color:#475569; margin:0;">Applied just now</p></div></div></div>
            <div style="text-align:center; margin:30px 0;"><a href="{current_app.config['BASE_URL']}/recruiter/jobs/{job['id']}/applications" style="background:linear-gradient(135deg, #22c55e, #16a34a); color:white; padding:16px 40px; text-decoration:none; border-radius:50px; font-weight:600; display:inline-block;">👁️ Review Application</a></div>
            <div style="background:#fef9c3; border-left:4px solid #eab308; padding:20px; border-radius:8px; margin:20px 0;"><p style="margin:0; color:#854d0e; font-size:14px;"><strong>⏰ Time is important!</strong> Review applications promptly to secure the best talent.</p></div>
            """
            return self.send_email(to_email, subject, self._base_template(inner), user_id)
        except Exception as e:
            traceback.print_exc()
            return False

    def send_application_status_update(self, to_email, freelancer_name, job_title, status, recruiter_notes=None, job_id=None, user_id=None):
        status_display = status.title()
        subject = f"📋 Application {status_display}: {job_title}"
        notes_html = f'<div style="background:#f8fafc; border-left:4px solid #667eea; padding:15px; margin:20px 0; border-radius:8px;"><p style="margin:0 0 5px; color:#334155; font-weight:600;">📝 Recruiter\'s Note:</p><p style="margin:0; color:#475569;">{recruiter_notes}</p></div>' if recruiter_notes else ''
        inner = f"""
        <div style="text-align:center; margin-bottom:20px;"><div style="font-size:48px; margin-bottom:10px;">📋</div><h2 style="color:#1e293b; font-size:28px; font-weight:700;">Application {status_display}</h2></div>
        <p style="font-size:16px; color:#475569; line-height:1.6; margin-bottom:20px;">Hi <strong style="color:#667eea;">{freelancer_name}</strong>,</p>
        <p style="font-size:16px; color:#475569; line-height:1.6; margin-bottom:20px;">Your application for <strong>"{job_title}"</strong> is now <strong>{status_display}</strong>.</p>
        {notes_html}
        <p style="font-size:16px; color:#475569; line-height:1.6; margin-top:20px;">Check your dashboard for more details.</p>
        <div style="text-align:center; margin:30px 0;"><a href="{current_app.config['BASE_URL']}/freelancer/applications" style="background:linear-gradient(135deg, #667eea, #764ba2); color:white; padding:16px 40px; text-decoration:none; border-radius:50px; font-weight:600; display:inline-block;">View My Applications</a></div>
        """
        return self.send_email(to_email, subject, self._base_template(inner), user_id)

    
def send_job_updated_notification(self, to_email, recruiter_name, job_title, job_id, user_id=None):
    """Notify recruiter that a job was updated."""
    subject = f"✏️ Job Updated: {job_title}"
    job_link = f"{current_app.config['BASE_URL']}/recruiter/jobs/{job_id}"
    inner = f"""
    <h2 style="color:#1e293b; margin-bottom:20px;">Job Updated Successfully</h2>
    <p style="font-size:16px; color:#475569; line-height:1.6; margin-bottom:20px;">
        Hi <strong style="color:#667eea;">{recruiter_name}</strong>,
    </p>
    <p style="font-size:16px; color:#475569; line-height:1.6; margin-bottom:20px;">
        Your job <strong>"{job_title}"</strong> has been updated.
    </p>
    <p style="font-size:16px; color:#475569; line-height:1.6; margin-bottom:20px;">
        You can view the changes in your dashboard.
    </p>
    <div style="text-align:center; margin:30px 0;">
        <a href="{job_link}" style="background:linear-gradient(135deg, #0ea5e9, #2563eb); color:white; padding:16px 40px; text-decoration:none; border-radius:50px; font-weight:600; display:inline-block;">
            View Job
        </a>
    </div>
    """
    return self.send_email(to_email, subject, self._base_template(inner), user_id)

def send_job_status_changed_notification(self, to_email, recruiter_name, job_title, job_id, is_active, user_id=None):
    """Notify recruiter when a job's active status changes."""
    status = "activated" if is_active else "deactivated"
    subject = f"🔄 Job {status.title()}: {job_title}"
    job_link = f"{current_app.config['BASE_URL']}/recruiter/jobs/{job_id}"
    inner = f"""
    <h2 style="color:#1e293b; margin-bottom:20px;">Job Status Changed</h2>
    <p style="font-size:16px; color:#475569; line-height:1.6; margin-bottom:20px;">
        Hi <strong style="color:#667eea;">{recruiter_name}</strong>,
    </p>
    <p style="font-size:16px; color:#475569; line-height:1.6; margin-bottom:20px;">
        Your job <strong>"{job_title}"</strong> has been <strong>{status}</strong>.
    </p>
    <div style="text-align:center; margin:30px 0;">
        <a href="{job_link}" style="background:linear-gradient(135deg, #0ea5e9, #2563eb); color:white; padding:16px 40px; text-decoration:none; border-radius:50px; font-weight:600; display:inline-block;">
            View Job
        </a>
    </div>
    """
    return self.send_email(to_email, subject, self._base_template(inner), user_id)


# Global placeholder – will be set in app.py
email_service = None