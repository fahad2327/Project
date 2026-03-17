# # from utils.email_config import EmailConfig

# # class EmailTemplates:
# #     """Email templates for various notifications"""
    
# #     @staticmethod
# #     def get_base_template(content, title=""):
# #         """Get base HTML template"""
# #         return f"""
# #         <!DOCTYPE html>
# #         <html>
# #         <head>
# #             <meta charset="UTF-8">
# #             <meta name="viewport" content="width=device-width, initial-scale=1.0">
# #             <title>{title}</title>
# #             <style>
# #                 body {{
# #                     font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
# #                     line-height: 1.6;
# #                     color: #1f2937;
# #                     background-color: #f3f4f6;
# #                     margin: 0;
# #                     padding: 0;
# #                 }}
# #                 .container {{
# #                     max-width: 600px;
# #                     margin: 20px auto;
# #                     background-color: #ffffff;
# #                     border-radius: 16px;
# #                     box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.1);
# #                     overflow: hidden;
# #                 }}
# #                 .header {{
# #                     background: linear-gradient(135deg, #6366f1, #10b981);
# #                     padding: 30px 20px;
# #                     text-align: center;
# #                 }}
# #                 .header h1 {{
# #                     color: white;
# #                     margin: 0;
# #                     font-size: 28px;
# #                     font-weight: 700;
# #                 }}
# #                 .header p {{
# #                     color: rgba(255, 255, 255, 0.9);
# #                     margin: 10px 0 0;
# #                     font-size: 16px;
# #                 }}
# #                 .content {{
# #                     padding: 40px 30px;
# #                 }}
# #                 .button {{
# #                     display: inline-block;
# #                     padding: 14px 30px;
# #                     background: linear-gradient(135deg, #6366f1, #10b981);
# #                     color: white !important;
# #                     text-decoration: none;
# #                     border-radius: 30px;
# #                     font-weight: 600;
# #                     margin: 20px 0;
# #                     box-shadow: 0 4px 6px -1px rgba(99, 102, 241, 0.3);
# #                 }}
# #                 .button:hover {{
# #                     transform: translateY(-2px);
# #                     box-shadow: 0 10px 15px -3px rgba(99, 102, 241, 0.4);
# #                 }}
# #                 .footer {{
# #                     background-color: #f9fafb;
# #                     padding: 20px 30px;
# #                     text-align: center;
# #                     color: #6b7280;
# #                     font-size: 14px;
# #                     border-top: 1px solid #e5e7eb;
# #                 }}
# #                 .status-badge {{
# #                     display: inline-block;
# #                     padding: 8px 16px;
# #                     border-radius: 30px;
# #                     font-size: 14px;
# #                     font-weight: 600;
# #                 }}
# #                 .status-accepted {{
# #                     background: #d1fae5;
# #                     color: #065f46;
# #                 }}
# #                 .status-rejected {{
# #                     background: #fee2e2;
# #                     color: #b91c1c;
# #                 }}
# #                 .status-pending {{
# #                     background: #fef3c7;
# #                     color: #b45309;
# #                 }}
# #                 .divider {{
# #                     height: 1px;
# #                     background: linear-gradient(90deg, transparent, #6366f1, #10b981, transparent);
# #                     margin: 30px 0;
# #                 }}
# #                 .job-details {{
# #                     background: #f9fafb;
# #                     border-radius: 12px;
# #                     padding: 20px;
# #                     margin: 20px 0;
# #                     border-left: 4px solid #6366f1;
# #                 }}
# #             </style>
# #         </head>
# #         <body>
# #             <div class="container">
# #                 <div class="header">
# #                     <h1>⚡ FreelanceHub</h1>
# #                     <p>Your Gateway to Freelance Success</p>
# #                 </div>
# #                 <div class="content">
# #                     {content}
# #                 </div>
# #                 <div class="footer">
# #                     <p>© 2026 FreelanceHub. All rights reserved.</p>
# #                     <p style="margin-top: 10px; font-size: 12px;">
# #                         This email was sent to you because you're a member of FreelanceHub.<br>
# #                         If you didn't expect this email, please ignore it.
# #                     </p>
# #                 </div>
# #             </div>
# #         </body>
# #         </html>
# #         """
    
# #     @staticmethod
# #     def email_verification(user_name, verification_token):
# #         """Email verification template"""
# #         verification_link = f"{EmailConfig.BASE_URL}/verify-email/{verification_token}"
        
# #         content = f"""
# #         <h2 style="color: #1f2937; margin-bottom: 20px;">Welcome to FreelanceHub, {user_name}! 👋</h2>
        
# #         <p style="font-size: 16px; margin-bottom: 20px;">
# #             Thank you for joining our platform. Please verify your email address to get started.
# #         </p>
        
# #         <div style="text-align: center;">
# #             <a href="{verification_link}" class="button">Verify Email Address</a>
# #         </div>
        
# #         <p style="font-size: 14px; color: #6b7280; margin-top: 30px;">
# #             If the button doesn't work, copy and paste this link into your browser:<br>
# #             <span style="color: #6366f1;">{verification_link}</span>
# #         </p>
        
# #         <div class="divider"></div>
        
# #         <p style="font-size: 14px;">
# #             <strong>Why verify?</strong> Verification helps us keep the platform secure and ensures you receive important notifications about your applications and jobs.
# #         </p>
# #         """
        
# #         subject = "Verify Your Email - FreelanceHub"
# #         return EmailTemplates.get_base_template(content, subject), subject
    
# #     @staticmethod
# #     def job_posted_notification(recruiter_name, job_title, job_id):
# #         """Email to recruiter when job is posted"""
# #         job_link = f"{EmailConfig.BASE_URL}/jobs/{job_id}"
        
# #         content = f"""
# #         <h2 style="color: #1f2937; margin-bottom: 20px;">Job Posted Successfully! 🎉</h2>
        
# #         <p style="font-size: 16px; margin-bottom: 20px;">
# #             Hi {recruiter_name},
# #         </p>
        
# #         <p style="font-size: 16px; margin-bottom: 20px;">
# #             Your job "<strong>{job_title}</strong>" has been posted successfully and is now live on FreelanceHub.
# #         </p>
        
# #         <div class="job-details">
# #             <h3 style="margin: 0 0 10px; color: #1f2937;">What's Next?</h3>
# #             <ul style="margin: 0; padding-left: 20px;">
# #                 <li style="margin-bottom: 8px;">Freelancers will start applying to your job</li>
# #                 <li style="margin-bottom: 8px;">You'll receive email notifications for new applications</li>
# #                 <li style="margin-bottom: 8px;">Review applications and shortlist candidates</li>
# #             </ul>
# #         </div>
        
# #         <div style="text-align: center;">
# #             <a href="{job_link}" class="button">View Your Job</a>
# #         </div>
        
# #         <p style="font-size: 14px; margin-top: 30px;">
# #             <strong>Pro Tip:</strong> Share the job link on your social media to attract more qualified freelancers!
# #         </p>
# #         """
        
# #         subject = f"✅ Job Posted: {job_title} - FreelanceHub"
# #         return EmailTemplates.get_base_template(content, subject), subject
    
# #     @staticmethod
# #     def application_submitted_notification(recruiter_name, freelancer_name, job_title, job_id):
# #         """Email to recruiter when freelancer applies"""
# #         applications_link = f"{EmailConfig.BASE_URL}/jobs/{job_id}/applications"
        
# #         content = f"""
# #         <h2 style="color: #1f2937; margin-bottom: 20px;">New Application Received! 📬</h2>
        
# #         <p style="font-size: 16px; margin-bottom: 20px;">
# #             Hi {recruiter_name},
# #         </p>
        
# #         <p style="font-size: 16px; margin-bottom: 20px;">
# #             <strong>{freelancer_name}</strong> has applied to your job "<strong>{job_title}</strong>".
# #         </p>
        
# #         <div class="job-details">
# #             <h3 style="margin: 0 0 10px; color: #1f2937;">Application Summary:</h3>
# #             <p style="margin: 5px 0;"><strong>Freelancer:</strong> {freelancer_name}</p>
# #             <p style="margin: 5px 0;"><strong>Job:</strong> {job_title}</p>
# #             <p style="margin: 5px 0;"><strong>Status:</strong> <span class="status-badge status-pending">Pending Review</span></p>
# #         </div>
        
# #         <div style="text-align: center;">
# #             <a href="{applications_link}" class="button">Review Application</a>
# #         </div>
        
# #         <p style="font-size: 14px; margin-top: 20px;">
# #             Don't wait too long - top freelancers get multiple offers! Review and respond to applications promptly.
# #         </p>
# #         """
        
# #         subject = f"📬 New Application: {freelancer_name} applied to {job_title}"
# #         return EmailTemplates.get_base_template(content, subject), subject
    
# #     @staticmethod
# #     def application_status_update(freelancer_name, job_title, status, recruiter_notes=None):
# #         """Email to freelancer when application status changes"""
        
# #         status_colors = {
# #             'reviewed': 'status-pending',
# #             'shortlisted': 'status-pending',
# #             'accepted': 'status-accepted',
# #             'rejected': 'status-rejected'
# #         }
        
# #         status_class = status_colors.get(status, 'status-pending')
# #         status_display = status.title()
        
# #         status_messages = {
# #             'reviewed': 'Your application has been reviewed by the recruiter.',
# #             'shortlisted': 'Congratulations! You have been shortlisted for this position.',
# #             'accepted': '🎉 Excellent news! Your application has been accepted!',
# #             'rejected': 'Thank you for your interest. The recruiter has moved forward with other candidates.'
# #         }
        
# #         message = status_messages.get(status, f'Your application status has been updated to {status_display}')
        
# #         notes_html = ""
# #         if recruiter_notes:
# #             notes_html = f"""
# #             <div style="background: #f3f4f6; border-left: 4px solid #6366f1; padding: 15px; margin: 20px 0;">
# #                 <strong style="color: #1f2937;">Recruiter's Note:</strong>
# #                 <p style="margin: 10px 0 0; color: #4b5563;">{recruiter_notes}</p>
# #             </div>
# #             """
        
# #         content = f"""
# #         <h2 style="color: #1f2937; margin-bottom: 20px;">Application Status Update</h2>
        
# #         <p style="font-size: 16px; margin-bottom: 20px;">
# #             Hi {freelancer_name},
# #         </p>
        
# #         <div class="job-details">
# #             <h3 style="margin: 0 0 10px; color: #1f2937;">{job_title}</h3>
# #             <p style="margin: 10px 0;">
# #                 <strong>Status:</strong> 
# #                 <span class="status-badge {status_class}">{status_display}</span>
# #             </p>
# #             <p style="margin: 10px 0;">{message}</p>
# #         </div>
        
# #         {notes_html}
        
# #         <div style="text-align: center; margin-top: 30px;">
# #             <a href="{EmailConfig.BASE_URL}/my-applications" class="button">View My Applications</a>
# #         </div>
        
# #         <p style="font-size: 14px; margin-top: 30px;">
# #             Keep applying to other opportunities while you wait for responses. Your perfect match is out there!
# #         </p>
# #         """
        
# #         subject = f"📋 Application {status_display}: {job_title}"
# #         return EmailTemplates.get_base_template(content, subject), subject
    
# #     @staticmethod
# #     def password_reset(user_name, reset_token):
# #         """Password reset email"""
# #         reset_link = f"{EmailConfig.BASE_URL}/reset-password/{reset_token}"
        
# #         content = f"""
# #         <h2 style="color: #1f2937; margin-bottom: 20px;">Reset Your Password 🔐</h2>
        
# #         <p style="font-size: 16px; margin-bottom: 20px;">
# #             Hi {user_name},
# #         </p>
        
# #         <p style="font-size: 16px; margin-bottom: 20px;">
# #             We received a request to reset your password. Click the button below to create a new password:
# #         </p>
        
# #         <div style="text-align: center;">
# #             <a href="{reset_link}" class="button">Reset Password</a>
# #         </div>
        
# #         <p style="font-size: 14px; color: #6b7280; margin-top: 30px;">
# #             If you didn't request this, please ignore this email. Your password will remain unchanged.
# #         </p>
        
# #         <p style="font-size: 12px; color: #9ca3af; margin-top: 20px;">
# #             This link will expire in 1 hour for security reasons.
# #         </p>
# #         """
        
# #         subject = "Reset Your Password - FreelanceHub"
# #         return EmailTemplates.get_base_template(content, subject), subject
    
# #     @staticmethod
# #     def welcome_email(user_name, user_type):
# #         """Welcome email for new users"""
        
# #         type_specific = ""
# #         if user_type == 'freelancer':
# #             type_specific = """
# #             <ul style="margin: 15px 0; padding-left: 20px;">
# #                 <li style="margin-bottom: 8px;">Complete your profile to attract recruiters</li>
# #                 <li style="margin-bottom: 8px;">Browse and apply to thousands of jobs</li>
# #                 <li style="margin-bottom: 8px;">Get notified when recruiters review your applications</li>
# #             </ul>
# #             """
# #         else:
# #             type_specific = """
# #             <ul style="margin: 15px 0; padding-left: 20px;">
# #                 <li style="margin-bottom: 8px;">Post your first job and attract top talent</li>
# #                 <li style="margin-bottom: 8px;">Review applications and shortlist candidates</li>
# #                 <li style="margin-bottom: 8px;">Get notified instantly when freelancers apply</li>
# #             </ul>
# #             """
        
# #         content = f"""
# #         <h2 style="color: #1f2937; margin-bottom: 20px;">Welcome to FreelanceHub, {user_name}! 🎉</h2>
        
# #         <p style="font-size: 16px; margin-bottom: 20px;">
# #             Thank you for joining the fastest-growing freelance platform. We're excited to have you on board!
# #         </p>
        
# #         <div class="job-details">
# #             <h3 style="margin: 0 0 10px; color: #1f2937;">Getting Started:</h3>
# #             {type_specific}
# #         </div>
        
# #         <div style="text-align: center; margin: 30px 0;">
# #             <a href="{EmailConfig.BASE_URL}/dashboard" class="button">Go to Dashboard</a>
# #         </div>
        
# #         <p style="font-size: 14px;">
# #             Need help? Check out our <a href="{EmailConfig.BASE_URL}/help" style="color: #6366f1;">Help Center</a> or contact our support team.
# #         </p>
# #         """
        
# #         subject = f"Welcome to FreelanceHub, {user_name}! 🎉"
# #         return EmailTemplates.get_base_template(content, subject), subject
# # utils/email_templates.py

# from utils.email_config import EmailConfig

# class EmailTemplates:
#     """Beautiful email templates for all notifications"""
    
#     BASE_URL = EmailConfig.BASE_URL
    
#     @staticmethod
#     def get_base_template(content, title=""):
#         """Get base HTML template with premium design"""
#         return f"""
#         <!DOCTYPE html>
#         <html>
#         <head>
#             <meta charset="UTF-8">
#             <meta name="viewport" content="width=device-width, initial-scale=1.0">
#             <title>{title}</title>
#             <style>
#                 * {{
#                     margin: 0;
#                     padding: 0;
#                     box-sizing: border-box;
#                 }}
                
#                 body {{
#                     font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
#                     background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
#                     line-height: 1.6;
#                     color: #1f2937;
#                     margin: 0;
#                     padding: 40px 20px;
#                 }}
                
#                 .container {{
#                     max-width: 600px;
#                     margin: 0 auto;
#                     background-color: #ffffff;
#                     border-radius: 32px;
#                     box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25);
#                     overflow: hidden;
#                     animation: slideIn 0.5s ease-out;
#                 }}
                
#                 @keyframes slideIn {{
#                     from {{
#                         opacity: 0;
#                         transform: translateY(30px);
#                     }}
#                     to {{
#                         opacity: 1;
#                         transform: translateY(0);
#                     }}
#                 }}
                
#                 .header {{
#                     background: linear-gradient(135deg, #667eea, #764ba2);
#                     padding: 40px 30px;
#                     text-align: center;
#                     position: relative;
#                     overflow: hidden;
#                 }}
                
#                 .header::before {{
#                     content: '';
#                     position: absolute;
#                     top: -50%;
#                     right: -50%;
#                     width: 200%;
#                     height: 200%;
#                     background: radial-gradient(circle, rgba(255,255,255,0.2) 0%, transparent 70%);
#                     animation: rotate 20s linear infinite;
#                 }}
                
#                 @keyframes rotate {{
#                     from {{ transform: rotate(0deg); }}
#                     to {{ transform: rotate(360deg); }}
#                 }}
                
#                 .header h1 {{
#                     color: white;
#                     margin: 0;
#                     font-size: 36px;
#                     font-weight: 800;
#                     letter-spacing: -0.5px;
#                     position: relative;
#                     z-index: 1;
#                     text-shadow: 0 2px 4px rgba(0,0,0,0.1);
#                 }}
                
#                 .header p {{
#                     color: rgba(255, 255, 255, 0.9);
#                     margin: 10px 0 0;
#                     font-size: 18px;
#                     position: relative;
#                     z-index: 1;
#                 }}
                
#                 .content {{
#                     padding: 40px 30px;
#                     background: #ffffff;
#                 }}
                
#                 .button {{
#                     display: inline-block;
#                     padding: 16px 40px;
#                     background: linear-gradient(135deg, #667eea, #764ba2);
#                     color: white !important;
#                     text-decoration: none;
#                     border-radius: 50px;
#                     font-weight: 600;
#                     font-size: 16px;
#                     margin: 20px 0;
#                     box-shadow: 0 10px 20px -5px rgba(102, 126, 234, 0.4);
#                     transition: all 0.3s ease;
#                     border: none;
#                     cursor: pointer;
#                 }}
                
#                 .button:hover {{
#                     transform: translateY(-3px);
#                     box-shadow: 0 15px 30px -5px rgba(102, 126, 234, 0.6);
#                 }}
                
#                 .footer {{
#                     background: #f8fafc;
#                     padding: 30px;
#                     text-align: center;
#                     border-top: 1px solid #e2e8f0;
#                 }}
                
#                 .footer p {{
#                     color: #64748b;
#                     font-size: 14px;
#                     margin: 5px 0;
#                 }}
                
#                 .social-links {{
#                     margin: 20px 0;
#                 }}
                
#                 .social-link {{
#                     display: inline-block;
#                     margin: 0 10px;
#                     color: #667eea;
#                     text-decoration: none;
#                     font-size: 14px;
#                 }}
                
#                 .divider {{
#                     height: 2px;
#                     background: linear-gradient(90deg, transparent, #667eea, #764ba2, transparent);
#                     margin: 30px 0;
#                 }}
                
#                 .info-box {{
#                     background: linear-gradient(135deg, #f8fafc, #f1f5f9);
#                     border-left: 4px solid #667eea;
#                     padding: 20px;
#                     border-radius: 12px;
#                     margin: 20px 0;
#                 }}
                
#                 .badge {{
#                     display: inline-block;
#                     padding: 6px 16px;
#                     border-radius: 30px;
#                     font-size: 14px;
#                     font-weight: 600;
#                     background: linear-gradient(135deg, #667eea, #764ba2);
#                     color: white;
#                 }}
                
#                 .verification-link {{
#                     background: #f1f5f9;
#                     padding: 15px;
#                     border-radius: 12px;
#                     word-break: break-all;
#                     font-family: monospace;
#                     font-size: 14px;
#                     color: #1e293b;
#                     margin: 20px 0;
#                 }}
#             </style>
#         </head>
#         <body>
#             <div class="container">
#                 <div class="header">
#                     <h1>⚡ FreelanceHub</h1>
#                     <p>Your Gateway to Freelance Success</p>
#                 </div>
#                 <div class="content">
#                     {content}
#                 </div>
#                 <div class="footer">
#                     <div class="social-links">
#                         <a href="#" class="social-link">Twitter</a>
#                         <a href="#" class="social-link">LinkedIn</a>
#                         <a href="#" class="social-link">Facebook</a>
#                         <a href="#" class="social-link">Instagram</a>
#                     </div>
#                     <p>© 2026 FreelanceHub. All rights reserved.</p>
#                     <p style="font-size: 12px; margin-top: 15px;">
#                         This email was sent to you because you're a member of FreelanceHub.<br>
#                         If you didn't expect this email, please ignore it.
#                     </p>
#                 </div>
#             </div>
#         </body>
#         </html>
#         """
    
#     @staticmethod
#     def email_verification(user_name, verification_token):
#         """Email verification template"""
#         verification_link = f"{EmailTemplates.BASE_URL}/verify-email/{verification_token}"
        
#         content = f"""
#         <h2 style="color: #1e293b; margin-bottom: 20px; font-size: 28px; font-weight: 700;">
#             Welcome to FreelanceHub, {user_name}! 👋
#         </h2>
        
#         <p style="font-size: 16px; margin-bottom: 20px; color: #475569;">
#             Thank you for joining our community of talented freelancers and innovative companies. 
#             To get started, please verify your email address.
#         </p>
        
#         <div style="text-align: center; margin: 30px 0;">
#             <a href="{verification_link}" class="button" style="font-size: 18px;">
#                 🔐 Verify Email Address
#             </a>
#         </div>
        
#         <div class="info-box">
#             <p style="margin: 0; color: #334155;">
#                 <strong>✨ Why verify?</strong>
#             </p>
#             <ul style="margin: 15px 0 0 20px; color: #475569;">
#                 <li style="margin-bottom: 8px;">Receive instant job notifications</li>
#                 <li style="margin-bottom: 8px;">Get application updates via email</li>
#                 <li style="margin-bottom: 8px;">Connect with recruiters securely</li>
#                 <li style="margin-bottom: 8px;">Access all platform features</li>
#             </ul>
#         </div>
        
#         <p style="font-size: 14px; color: #64748b; margin: 30px 0 10px;">
#             If the button doesn't work, copy and paste this link into your browser:
#         </p>
        
#         <div class="verification-link">
#             {verification_link}
#         </div>
        
#         <div style="background: #fef3c7; border-left: 4px solid #f59e0b; padding: 15px; margin: 30px 0; border-radius: 8px;">
#             <p style="margin: 0; color: #92400e; font-size: 14px;">
#                 ⏰ This verification link will expire in <strong>24 hours</strong> for security reasons.
#             </p>
#         </div>
        
#         <p style="font-size: 14px; color: #94a3b8; margin-top: 30px;">
#             If you didn't create an account with FreelanceHub, please ignore this email.
#         </p>
#         """
        
#         subject = f"🎯 Verify Your Email - Welcome to FreelanceHub, {user_name}!"
#         return EmailTemplates.get_base_template(content, subject), subject
    
#     @staticmethod
#     def welcome_email(user_name, user_type):
#         """Welcome email after verification"""
        
#         if user_type == 'freelancer':
#             next_steps = """
#             <div style="display: flex; gap: 20px; margin: 20px 0; flex-wrap: wrap;">
#                 <div style="flex: 1; min-width: 150px; text-align: center; padding: 20px; background: #f8fafc; border-radius: 12px;">
#                     <div style="font-size: 40px; margin-bottom: 10px;">🔍</div>
#                     <h4 style="color: #1e293b; margin-bottom: 5px;">Find Work</h4>
#                     <p style="color: #64748b; font-size: 14px;">Browse thousands of jobs</p>
#                 </div>
#                 <div style="flex: 1; min-width: 150px; text-align: center; padding: 20px; background: #f8fafc; border-radius: 12px;">
#                     <div style="font-size: 40px; margin-bottom: 10px;">📝</div>
#                     <h4 style="color: #1e293b; margin-bottom: 5px;">Apply</h4>
#                     <p style="color: #64748b; font-size: 14px;">Submit your proposals</p>
#                 </div>
#                 <div style="flex: 1; min-width: 150px; text-align: center; padding: 20px; background: #f8fafc; border-radius: 12px;">
#                     <div style="font-size: 40px; margin-bottom: 10px;">💬</div>
#                     <h4 style="color: #1e293b; margin-bottom: 5px;">Connect</h4>
#                     <p style="color: #64748b; font-size: 14px;">Chat with recruiters</p>
#                 </div>
#             </div>
#             """
#         else:
#             next_steps = """
#             <div style="display: flex; gap: 20px; margin: 20px 0; flex-wrap: wrap;">
#                 <div style="flex: 1; min-width: 150px; text-align: center; padding: 20px; background: #f8fafc; border-radius: 12px;">
#                     <div style="font-size: 40px; margin-bottom: 10px;">📢</div>
#                     <h4 style="color: #1e293b; margin-bottom: 5px;">Post Jobs</h4>
#                     <p style="color: #64748b; font-size: 14px;">List your opportunities</p>
#                 </div>
#                 <div style="flex: 1; min-width: 150px; text-align: center; padding: 20px; background: #f8fafc; border-radius: 12px;">
#                     <div style="font-size: 40px; margin-bottom: 10px;">👥</div>
#                     <h4 style="color: #1e293b; margin-bottom: 5px;">Review</h4>
#                     <p style="color: #64748b; font-size: 14px;">Evaluate applications</p>
#                 </div>
#                 <div style="flex: 1; min-width: 150px; text-align: center; padding: 20px; background: #f8fafc; border-radius: 12px;">
#                     <div style="font-size: 40px; margin-bottom: 10px;">🤝</div>
#                     <h4 style="color: #1e293b; margin-bottom: 5px;">Hire</h4>
#                     <p style="color: #64748b; font-size: 14px;">Find the best talent</p>
#                 </div>
#             </div>
#             """
        
#         content = f"""
#         <div style="text-align: center; margin-bottom: 30px;">
#             <div style="font-size: 60px; margin-bottom: 20px;">🎉</div>
#             <h2 style="color: #1e293b; font-size: 32px; font-weight: 700; margin-bottom: 10px;">
#                 Email Verified Successfully!
#             </h2>
#             <p style="color: #475569; font-size: 18px;">
#                 Your account is now fully activated, {user_name}!
#             </p>
#         </div>
        
#         <div class="info-box" style="background: linear-gradient(135deg, #dbeafe, #ede9fe);">
#             <p style="margin: 0; color: #1e40af; font-size: 16px;">
#                 <strong>🚀 You're all set!</strong> You can now:
#             </p>
#             <ul style="margin: 15px 0 0 20px; color: #1e3a8a;">
#                 <li style="margin-bottom: 8px;">Receive instant email notifications</li>
#                 <li style="margin-bottom: 8px;">Apply to jobs / Review applications</li>
#                 <li style="margin-bottom: 8px;">Connect with clients/freelancers</li>
#                 <li style="margin-bottom: 8px;">Get real-time updates on your activity</li>
#             </ul>
#         </div>
        
#         {next_steps}
        
#         <div style="text-align: center; margin: 40px 0 20px;">
#             <a href="{EmailTemplates.BASE_URL}/dashboard" class="button" style="background: linear-gradient(135deg, #10b981, #059669);">
#                 🚀 Go to Dashboard
#             </a>
#             <a href="{EmailTemplates.BASE_URL}/profile" class="button" style="background: linear-gradient(135deg, #6366f1, #4f46e5); margin-left: 10px;">
#                 ✨ Complete Profile
#             </a>
#         </div>
        
#         <p style="font-size: 14px; color: #64748b; text-align: center; margin-top: 30px;">
#             We're excited to have you on board! If you need any help, check out our 
#             <a href="{EmailTemplates.BASE_URL}/help" style="color: #6366f1; text-decoration: none;">Help Center</a>.
#         </p>
#         """
        
#         subject = f"🎉 Welcome to FreelanceHub, {user_name}! Your Email is Verified"
#         return EmailTemplates.get_base_template(content, subject), subject
    
#     @staticmethod
#     def job_posted_notification(recruiter_name, job_title, job_id):
#         """Email to recruiter when job is posted"""
#         job_link = f"{EmailTemplates.BASE_URL}/jobs/{job_id}"
#         applications_link = f"{EmailTemplates.BASE_URL}/jobs/{job_id}/applications"
        
#         content = f"""
#         <h2 style="color: #1e293b; margin-bottom: 20px;">Job Posted Successfully! 🎯</h2>
        
#         <p style="font-size: 16px; margin-bottom: 20px; color: #475569;">
#             Hi <strong>{recruiter_name}</strong>,
#         </p>
        
#         <p style="font-size: 16px; margin-bottom: 30px; color: #475569;">
#             Your job "<strong>{job_title}</strong>" is now live on FreelanceHub and visible to thousands of qualified freelancers.
#         </p>
        
#         <div class="info-box" style="background: #f0f9ff; border-left-color: #0ea5e9;">
#             <h3 style="color: #0369a1; margin-bottom: 15px;">📊 Job Statistics</h3>
#             <div style="display: flex; justify-content: space-around; margin: 20px 0;">
#                 <div style="text-align: center;">
#                     <div style="font-size: 32px; font-weight: 700; color: #0ea5e9;">0</div>
#                     <div style="color: #64748b;">Applications</div>
#                 </div>
#                 <div style="text-align: center;">
#                     <div style="font-size: 32px; font-weight: 700; color: #0ea5e9;">24h</div>
#                     <div style="color: #64748b;">To First Response</div>
#                 </div>
#                 <div style="text-align: center;">
#                     <div style="font-size: 32px; font-weight: 700; color: #0ea5e9;">50+</div>
#                     <div style="color: #64748b;">Potential Matches</div>
#                 </div>
#             </div>
#         </div>
        
#         <div style="text-align: center; margin: 30px 0;">
#             <a href="{job_link}" class="button" style="background: linear-gradient(135deg, #0ea5e9, #2563eb);">
#                 👁️ View Your Job
#             </a>
#             <a href="{applications_link}" class="button" style="background: linear-gradient(135deg, #8b5cf6, #6366f1); margin-left: 10px;">
#                 📬 Track Applications
#             </a>
#         </div>
        
#         <div style="background: #f1f5f9; padding: 20px; border-radius: 12px; margin: 30px 0;">
#             <h4 style="color: #1e293b; margin-bottom: 10px;">⚡ What happens next?</h4>
#             <ul style="color: #475569; margin-left: 20px;">
#                 <li style="margin-bottom: 8px;">Freelancers will start applying to your job</li>
#                 <li style="margin-bottom: 8px;">You'll receive email notifications for each application</li>
#                 <li style="margin-bottom: 8px;">Review applications and shortlist candidates</li>
#                 <li style="margin-bottom: 8px;">Message freelancers directly to discuss details</li>
#             </ul>
#         </div>
        
#         <p style="font-size: 14px; color: #64748b; text-align: center;">
#             <strong>Pro Tip:</strong> Share the job link on LinkedIn to attract more qualified freelancers!
#         </p>
#         """
        
#         subject = f"✅ Job Posted: {job_title} - Start Receiving Applications Now!"
#         return EmailTemplates.get_base_template(content, subject), subject
    
#     @staticmethod
#     def application_submitted_notification(recruiter_name, freelancer_name, job_title, job_id, application_id):
#         """Email to recruiter when freelancer applies"""
#         application_link = f"{EmailTemplates.BASE_URL}/jobs/{job_id}/applications/{application_id}"
        
#         content = f"""
#         <div style="text-align: center; margin-bottom: 20px;">
#             <div style="font-size: 48px; margin-bottom: 10px;">📬</div>
#             <h2 style="color: #1e293b; font-size: 28px; font-weight: 700;">
#                 New Application Received!
#             </h2>
#         </div>
        
#         <p style="font-size: 16px; margin-bottom: 20px; color: #475569;">
#             Hi <strong>{recruiter_name}</strong>,
#         </p>
        
#         <p style="font-size: 16px; margin-bottom: 30px; color: #475569;">
#             <span style="font-size: 20px; font-weight: 600; color: #6366f1;">{freelancer_name}</span> has just applied to your job:<br>
#             <strong>"{job_title}"</strong>
#         </p>
        
#         <div class="info-box" style="background: #f0fdf4; border-left-color: #22c55e;">
#             <div style="display: flex; align-items: center; gap: 15px;">
#                 <div style="width: 60px; height: 60px; background: linear-gradient(135deg, #22c55e, #16a34a); border-radius: 50%; display: flex; align-items: center; justify-content: center; color: white; font-size: 24px;">
#                     👤
#                 </div>
#                 <div>
#                     <h3 style="color: #166534; margin-bottom: 5px;">{freelancer_name}</h3>
#                     <p style="color: #475569; margin: 0;">Applied just now • Ready to start</p>
#                 </div>
#             </div>
#         </div>
        
#         <div style="text-align: center; margin: 30px 0;">
#             <a href="{application_link}" class="button" style="background: linear-gradient(135deg, #22c55e, #16a34a);">
#                 👁️ Review Application
#             </a>
#         </div>
        
#         <div style="background: #fef9c3; border-left: 4px solid #eab308; padding: 20px; border-radius: 8px; margin: 20px 0;">
#             <p style="margin: 0; color: #854d0e; font-size: 14px;">
#                 <strong>⏰ Time is important!</strong> Top freelancers receive multiple offers. 
#                 Review and respond to applications promptly to secure the best talent.
#             </p>
#         </div>
        
#         <p style="font-size: 14px; color: #64748b; text-align: center; margin-top: 30px;">
#             You can view all applications in your <a href="{EmailTemplates.BASE_URL}/manage-jobs" style="color: #6366f1;">Manage Jobs</a> dashboard.
#         </p>
#         """
        
#         subject = f"📬 New Application: {freelancer_name} applied to {job_title}"
#         return EmailTemplates.get_base_template(content, subject), subject
    
#     @staticmethod
#     def application_status_update(freelancer_name, job_title, status, recruiter_notes=None, job_id=None):
#         """Email to freelancer when application status changes"""
        
#         status_colors = {
#             'reviewed': {'bg': '#fef9c3', 'text': '#854d0e', 'border': '#eab308', 'icon': '👀'},
#             'shortlisted': {'bg': '#dbeafe', 'text': '#1e40af', 'border': '#3b82f6', 'icon': '⭐'},
#             'accepted': {'bg': '#d1fae5', 'text': '#065f46', 'border': '#10b981', 'icon': '🎉'},
#             'rejected': {'bg': '#fee2e2', 'text': '#991b1b', 'border': '#ef4444', 'icon': '📋'}
#         }
        
#         colors = status_colors.get(status, {'bg': '#f1f5f9', 'text': '#475569', 'border': '#94a3b8', 'icon': '📝'})
        
#         status_messages = {
#             'reviewed': 'Your application has been reviewed by the recruiter.',
#             'shortlisted': 'Congratulations! You have been shortlisted for this position.',
#             'accepted': '🎉 Excellent news! Your application has been accepted!',
#             'rejected': 'Thank you for your interest. The recruiter has moved forward with other candidates.'
#         }
        
#         message = status_messages.get(status, f'Your application status has been updated to {status}')
        
#         notes_html = ""
#         if recruiter_notes:
#             notes_html = f"""
#             <div style="background: #f8fafc; border-left: 4px solid #6366f1; padding: 20px; margin: 20px 0; border-radius: 8px;">
#                 <p style="margin: 0 0 10px; color: #334155; font-weight: 600;">📝 Recruiter's Note:</p>
#                 <p style="margin: 0; color: #475569; font-style: italic;">"{recruiter_notes}"</p>
#             </div>
#             """
        
#         next_steps = ""
#         if status == 'accepted':
#             next_steps = """
#             <div style="background: #d1fae5; border-radius: 12px; padding: 20px; margin: 20px 0;">
#                 <h4 style="color: #065f46; margin-bottom: 10px;">✅ Next Steps:</h4>
#                 <ul style="color: #047857; margin-left: 20px;">
#                     <li style="margin-bottom: 5px;">The recruiter will contact you soon</li>
#                     <li style="margin-bottom: 5px;">Discuss project details and timeline</li>
#                     <li style="margin-bottom: 5px;">Agree on contract terms and start date</li>
#                 </ul>
#             </div>
#             """
#         elif status == 'rejected':
#             next_steps = """
#             <div style="background: #f1f5f9; border-radius: 12px; padding: 20px; margin: 20px 0;">
#                 <h4 style="color: #334155; margin-bottom: 10px;">💪 Keep Going!</h4>
#                 <p style="color: #475569;">Don't be discouraged! There are many other opportunities waiting for you:</p>
#                 <div style="text-align: center; margin-top: 15px;">
#                     <a href="{EmailTemplates.BASE_URL}/jobs" class="button" style="padding: 12px 30px; font-size: 14px; background: #6366f1;">
#                         🔍 Browse More Jobs
#                     </a>
#                 </div>
#             </div>
#             """
        
#         content = f"""
#         <div style="text-align: center; margin-bottom: 20px;">
#             <div style="font-size: 48px; margin-bottom: 10px;">{colors['icon']}</div>
#             <h2 style="color: {colors['text']}; font-size: 28px; font-weight: 700;">
#                 Application {status.title()}
#             </h2>
#         </div>
        
#         <p style="font-size: 16px; margin-bottom: 20px; color: #475569;">
#             Hi <strong>{freelancer_name}</strong>,
#         </p>
        
#         <div style="background: {colors['bg']}; border: 2px solid {colors['border']}; border-radius: 16px; padding: 20px; margin: 20px 0;">
#             <p style="margin: 0 0 10px; color: {colors['text']};">
#                 <strong>Job:</strong> {job_title}
#             </p>
#             <p style="margin: 0; color: {colors['text']};">
#                 <strong>Status:</strong> 
#                 <span style="background: {colors['border']}; color: white; padding: 4px 12px; border-radius: 30px; font-size: 14px;">
#                     {status.title()}
#                 </span>
#             </p>
#         </div>
        
#         <p style="font-size: 16px; color: #475569; margin: 20px 0;">
#             {message}
#         </p>
        
#         {notes_html}
        
#         {next_steps}
        
#         <div style="text-align: center; margin: 30px 0;">
#             <a href="{EmailTemplates.BASE_URL}/my-applications" class="button" style="background: linear-gradient(135deg, #6366f1, #4f46e5);">
#                 👁️ View My Applications
#             </a>
#         </div>
#         """
        
#         subject = f"📋 Application {status.title()}: {job_title}"
#         return EmailTemplates.get_base_template(content, subject), subject




# utils/email_templates.py
from utils.email_config import EmailConfig
# utils/email_templates.py
# utils/email_templates.py
class EmailTemplates:
    """Beautiful email templates for all notifications"""
    
    @staticmethod
    def get_base_template(content, title=""):
        """Get base HTML template with premium design"""
        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>{title}</title>
            <style>
                * {{
                    margin: 0;
                    padding: 0;
                    box-sizing: border-box;
                }}
                
                body {{
                    font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    line-height: 1.6;
                    color: #1f2937;
                    margin: 0;
                    padding: 40px 20px;
                }}
                
                .container {{
                    max-width: 600px;
                    margin: 0 auto;
                    background-color: #ffffff;
                    border-radius: 32px;
                    box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25);
                    overflow: hidden;
                    animation: slideIn 0.5s ease-out;
                }}
                
                @keyframes slideIn {{
                    from {{
                        opacity: 0;
                        transform: translateY(30px);
                    }}
                    to {{
                        opacity: 1;
                        transform: translateY(0);
                    }}
                }}
                
                .header {{
                    background: linear-gradient(135deg, #667eea, #764ba2);
                    padding: 40px 30px;
                    text-align: center;
                    position: relative;
                    overflow: hidden;
                }}
                
                .header::before {{
                    content: '';
                    position: absolute;
                    top: -50%;
                    right: -50%;
                    width: 200%;
                    height: 200%;
                    background: radial-gradient(circle, rgba(255,255,255,0.2) 0%, transparent 70%);
                    animation: rotate 20s linear infinite;
                }}
                
                @keyframes rotate {{
                    from {{ transform: rotate(0deg); }}
                    to {{ transform: rotate(360deg); }}
                }}
                
                .header h1 {{
                    color: white;
                    margin: 0;
                    font-size: 36px;
                    font-weight: 800;
                    letter-spacing: -0.5px;
                    position: relative;
                    z-index: 1;
                    text-shadow: 0 2px 4px rgba(0,0,0,0.1);
                }}
                
                .header p {{
                    color: rgba(255, 255, 255, 0.9);
                    margin: 10px 0 0;
                    font-size: 18px;
                    position: relative;
                    z-index: 1;
                }}
                
                .content {{
                    padding: 40px 30px;
                    background: #ffffff;
                }}
                
                .button {{
                    display: inline-block;
                    padding: 16px 40px;
                    background: linear-gradient(135deg, #667eea, #764ba2);
                    color: white !important;
                    text-decoration: none;
                    border-radius: 50px;
                    font-weight: 600;
                    font-size: 16px;
                    margin: 20px 0;
                    box-shadow: 0 10px 20px -5px rgba(102, 126, 234, 0.4);
                    transition: all 0.3s ease;
                    border: none;
                    cursor: pointer;
                }}
                
                .button:hover {{
                    transform: translateY(-3px);
                    box-shadow: 0 15px 30px -5px rgba(102, 126, 234, 0.6);
                }}
                
                .footer {{
                    background: #f8fafc;
                    padding: 30px;
                    text-align: center;
                    border-top: 1px solid #e2e8f0;
                }}
                
                .footer p {{
                    color: #64748b;
                    font-size: 14px;
                    margin: 5px 0;
                }}
                
                .divider {{
                    height: 2px;
                    background: linear-gradient(90deg, transparent, #667eea, #764ba2, transparent);
                    margin: 30px 0;
                }}
                
                .info-box {{
                    background: linear-gradient(135deg, #f8fafc, #f1f5f9);
                    border-left: 4px solid #667eea;
                    padding: 20px;
                    border-radius: 12px;
                    margin: 20px 0;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>⚡ FreelanceHub</h1>
                    <p>Your Gateway to Freelance Success</p>
                </div>
                <div class="content">
                    {content}
                </div>
                <div class="footer">
                    <p>© 2026 FreelanceHub. All rights reserved.</p>
                    <p style="font-size: 12px; margin-top: 15px;">
                        This email was sent to you because you're a member of FreelanceHub.<br>
                        If you didn't expect this email, please ignore it.
                    </p>
                </div>
            </div>
        </body>
        </html>
        """
    
    @staticmethod
    def application_confirmation(freelancer_name, job_title, company_name, base_url):
        """Confirmation email to freelancer after applying"""
        applications_link = f"{base_url}/freelancer/applications"
        
        content = f"""
        <div style="text-align: center; margin-bottom: 20px;">
            <div style="font-size: 48px; margin-bottom: 10px;">🎉</div>
            <h2 style="color: #1e293b; font-size: 28px; font-weight: 700;">
                Application Submitted!
            </h2>
        </div>
        
        <p style="font-size: 16px; margin-bottom: 20px; color: #475569;">
            Hi <strong>{freelancer_name}</strong>,
        </p>
        
        <p style="font-size: 16px; margin-bottom: 30px; color: #475569;">
            Your application for <strong>"{job_title}"</strong> at <strong>{company_name}</strong> has been successfully submitted!
        </p>
        
        <div class="info-box">
            <h3 style="color: #1e293b; margin-bottom: 15px;">✅ What happens next?</h3>
            <ul style="color: #475569; margin-left: 20px;">
                <li style="margin-bottom: 10px;">The recruiter will review your application</li>
                <li style="margin-bottom: 10px;">You'll receive an email when they update the status</li>
                <li style="margin-bottom: 10px;">You can track all applications in your dashboard</li>
            </ul>
        </div>
        
        <div style="text-align: center; margin: 30px 0;">
            <a href="{applications_link}" class="button">
                📋 Track Your Application
            </a>
        </div>
        
        <p style="font-size: 16px; color: #475569; text-align: center;">
            Good luck! 🤞
        </p>
        """
        
        subject = f"✅ Application Submitted: {job_title}"
        return EmailTemplates.get_base_template(content, subject), subject
    
    @staticmethod
    def application_submitted_notification(recruiter_name, freelancer_name, job_title, job_id, application_id, base_url):
        """Email to recruiter when someone applies"""
        application_link = f"{base_url}/recruiter/jobs/{job_id}/applications"
        
        content = f"""
        <div style="text-align: center; margin-bottom: 20px;">
            <div style="font-size: 48px; margin-bottom: 10px;">📬</div>
            <h2 style="color: #1e293b; font-size: 28px; font-weight: 700;">
                New Application Received!
            </h2>
        </div>
        
        <p style="font-size: 16px; margin-bottom: 20px; color: #475569;">
            Hi <strong>{recruiter_name}</strong>,
        </p>
        
        <p style="font-size: 16px; margin-bottom: 30px; color: #475569;">
            <span style="font-size: 20px; font-weight: 600; color: #6366f1;">{freelancer_name}</span> has just applied to your job:<br>
            <strong>"{job_title}"</strong>
        </p>
        
        <div class="info-box">
            <div style="display: flex; align-items: center; gap: 15px;">
                <div style="width: 60px; height: 60px; background: linear-gradient(135deg, #22c55e, #16a34a); border-radius: 50%; display: flex; align-items: center; justify-content: center; color: white; font-size: 24px;">
                    👤
                </div>
                <div>
                    <h3 style="color: #166534; margin-bottom: 5px;">{freelancer_name}</h3>
                    <p style="color: #475569; margin: 0;">Applied just now</p>
                </div>
            </div>
        </div>
        
        <div style="text-align: center; margin: 30px 0;">
            <a href="{application_link}" class="button">
                👁️ Review Application
            </a>
        </div>
        
        <div style="background: #fef9c3; border-left: 4px solid #eab308; padding: 20px; border-radius: 8px; margin: 20px 0;">
            <p style="margin: 0; color: #854d0e; font-size: 14px;">
                <strong>⏰ Time is important!</strong> Review applications promptly to secure the best talent.
            </p>
        </div>
        """
        
        subject = f"📬 New Application: {freelancer_name} applied to {job_title}"
        return EmailTemplates.get_base_template(content, subject), subject