# from flask import Blueprint, request, jsonify
# from database.models import FreelancerProfile, Job, JobApplication, Notification
# from services.email_service import EmailService
# from utils.auth_utils import token_required, freelancer_required
# from datetime import datetime
# import traceback

# freelancer_bp = Blueprint('freelancer', __name__, url_prefix='/api/freelancer')

# @freelancer_bp.route('/jobs/<int:job_id>/apply', methods=['POST'])
# @token_required
# @freelancer_required
# def apply_for_job(job_id):
#     """Apply for a job with email notification"""
#     try:
#         data = request.get_json() or {}
        
#         # Validate required fields
#         if not data.get('cover_letter'):
#             return jsonify({
#                 'success': False,
#                 'message': 'Cover letter is required'
#             }), 400
        
#         application_id = JobApplication.create(
#             job_id=job_id,
#             freelancer_id=request.user_id,
#             application_data=data
#         )
        
#         if not application_id:
#             return jsonify({
#                 'success': False,
#                 'message': 'You have already applied for this job or job not found'
#             }), 400
        
#         # Get job details for email
#         job = Job.get_by_id(job_id)
        
#         # Send email notification to recruiter
#         EmailService.send_application_submitted_notification(application_id)
        
#         # Create in-app notification for recruiter
#         if job:
#             freelancer = User.find_by_id(request.user_id)
#             freelancer_name = f"{freelancer['first_name']} {freelancer['last_name']}"
            
#             Notification.create(
#                 user_id=job['recruiter_id'],
#                 title='New Job Application',
#                 message=f'{freelancer_name} has applied for {job["title"]}',
#                 notification_type='application',
#                 related_application_id=application_id,
#                 related_job_id=job_id
#             )
#             print(f"📧 Email and notification sent to recruiter {job['recruiter_id']}")
        
#         return jsonify({
#             'success': True,
#             'message': 'Application submitted successfully! The recruiter has been notified.',
#             'application_id': application_id
#         }), 201
        
#     except Exception as e:
#         print(f"❌ Error in apply_for_job: {str(e)}")
#         traceback.print_exc()
#         return jsonify({
#             'success': False,
#             'message': f'Application failed: {str(e)}'
#         }), 500
    


# # ============== TEST EMAIL ENDPOINTS ==============
# # Keep only this simple test (no auth required)
# @freelancer_bp.route('/test-email-simple', methods=['GET'])
# def test_email_simple():
#     """Simple test endpoint for email - no auth required"""
#     try:
#         from flask_mail import Message, Mail
#         msg = Message(
#             subject="Test Email from FreelanceHub",
#             recipients=["star36522253@gmail.com"],
#             body="This is a test email to verify SMTP configuration.",
#             sender=current_app.config.get('FROM_EMAIL')
#         )
#         mail = Mail(current_app)
#         mail.send(msg)
#         return jsonify({'success': True, 'message': 'Test email sent! Check your inbox.'})
#     except Exception as e:
#         traceback.print_exc()
#         return jsonify({'success': False, 'message': str(e)}), 500

# @freelancer_bp.route('/debug-email-status', methods=['GET'])
# def debug_email_status():
#     try:
#         status = {
#             'email_service_exists': email_service is not None,
#             'mail_configured': email_service.mail is not None if email_service else False,
#         }
#         if email_service and email_service.mail:
#             status['mail_server'] = current_app.config.get('MAIL_SERVER')
#             status['mail_username'] = current_app.config.get('MAIL_USERNAME')
#             status['mail_port'] = current_app.config.get('MAIL_PORT')
#             status['mail_use_tls'] = current_app.config.get('MAIL_USE_TLS')
#         return jsonify({'success': True, 'status': status})
#     except Exception as e:
#         return jsonify({'success': False, 'error': str(e)}), 500


from flask import Blueprint, current_app, request, jsonify
from database.models import FreelancerProfile, Job, JobApplication, Notification, User
from services.email_instance import email_service   # ✅ the global instance
from utils.auth_utils import token_required, freelancer_required
from datetime import datetime
import traceback

freelancer_bp = Blueprint('freelancer', __name__, url_prefix='/api/freelancer')

# ==================== Dashboard ====================
@freelancer_bp.route('/dashboard', methods=['GET'])
@token_required
@freelancer_required
def get_dashboard():
    try:
        # Get freelancer profile and stats
        profile = FreelancerProfile.get_by_user_id(request.user_id)
        stats = FreelancerProfile.get_stats(request.user_id)
        recent_applications = JobApplication.get_recent_by_freelancer(request.user_id, limit=5)
        recommended_jobs = Job.get_recommended_for_freelancer(request.user_id, limit=5)

        return jsonify({
            'success': True,
            'profile': profile,
            'stats': stats,
            'recent_applications': recent_applications,
            'recommended_jobs': recommended_jobs
        }), 200
    except Exception as e:
        traceback.print_exc()
        return jsonify({'success': False, 'message': str(e)}), 500

# ==================== Profile ====================
@freelancer_bp.route('/profile', methods=['GET', 'PUT'])
@token_required
@freelancer_required
def profile():
    if request.method == 'GET':
        try:
            profile = FreelancerProfile.get_by_user_id(request.user_id)
            if not profile:
                # Create empty profile if none exists
                profile = FreelancerProfile.create_empty(request.user_id)
            return jsonify({'success': True, 'profile': profile}), 200
        except Exception as e:
            return jsonify({'success': False, 'message': str(e)}), 500

    elif request.method == 'PUT':
        try:
            data = request.get_json()
            success = FreelancerProfile.update(request.user_id, data)
            if success:
                profile = FreelancerProfile.get_by_user_id(request.user_id)
                return jsonify({'success': True, 'profile': profile}), 200
            else:
                return jsonify({'success': False, 'message': 'Update failed'}), 400
        except Exception as e:
            return jsonify({'success': False, 'message': str(e)}), 500

# ==================== Job Search ====================
@freelancer_bp.route('/jobs/search', methods=['GET'])
@token_required
@freelancer_required
def search_jobs():
    try:
        filters = {
            'search': request.args.get('search', ''),
            'experience_level': request.args.get('experience_level', ''),
            'min_pay': request.args.get('min_pay', type=float),
            'max_pay': request.args.get('max_pay', type=float),
            'job_type': request.args.get('job_type', ''),
            'is_remote': request.args.get('is_remote') == 'true'
        }
        # Remove empty filters
        filters = {k: v for k, v in filters.items() if v not in (None, '', False)}
        jobs = Job.search(filters)
        return jsonify({'success': True, 'jobs': jobs}), 200
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

# ==================== Job Details ====================
@freelancer_bp.route('/jobs/<int:job_id>', methods=['GET'])
@token_required
@freelancer_required
def get_job_details(job_id):
    try:
        job = Job.get_by_id(job_id)
        if not job:
            return jsonify({'success': False, 'message': 'Job not found'}), 404
        # Check if already applied
        application = JobApplication.get_by_job_and_freelancer(job_id, request.user_id)
        job['has_applied'] = application is not None
        return jsonify({'success': True, 'job': job}), 200
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500
@freelancer_bp.route('/jobs/<int:job_id>/apply', methods=['POST'])
@token_required
@freelancer_required
def apply_for_job(job_id):
    try:
        data = request.get_json() or {}
        if not data.get('cover_letter'):
            return jsonify({'success': False, 'message': 'Cover letter is required'}), 400

        application_id = JobApplication.create(
            job_id=job_id,
            freelancer_id=request.user_id,
            application_data=data
        )

        if not application_id:
            return jsonify({
                'success': False,
                'message': 'You have already applied for this job or job not found'
            }), 400

        # Get job details for email
        job = Job.get_by_id(job_id)
        if job:
            # Retrieve email service from app config
            email_service = current_app.config.get('EMAIL_SERVICE')
            if email_service:
                email_service.send_application_submitted_notification(application_id)
            else:
                print("⚠️ Email service not available")

            # Create in-app notification for recruiter
            freelancer = User.find_by_id(request.user_id)
            freelancer_name = f"{freelancer['first_name']} {freelancer['last_name']}"
            Notification.create(
                user_id=job['recruiter_id'],
                title='New Job Application',
                message=f'{freelancer_name} has applied for {job["title"]}',
                notification_type='application',
                related_application_id=application_id,
                related_job_id=job_id
            )

        return jsonify({
            'success': True,
            'message': 'Application submitted successfully! The recruiter has been notified.',
            'application_id': application_id
        }), 201

    except Exception as e:
        traceback.print_exc()
        return jsonify({'success': False, 'message': f'Application failed: {str(e)}'}), 500

# ==================== My Applications ====================
@freelancer_bp.route('/applications', methods=['GET'])
@token_required
@freelancer_required
def get_my_applications():
    try:
        applications = JobApplication.get_by_freelancer(request.user_id)
        return jsonify({'success': True, 'applications': applications}), 200
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

# ==================== Single Application Details ====================
@freelancer_bp.route('/applications/<int:application_id>', methods=['GET'])
@token_required
@freelancer_required
def get_application_details(application_id):
    try:
        application = JobApplication.get_by_id(application_id)
        if not application or application['freelancer_id'] != request.user_id:
            return jsonify({'success': False, 'message': 'Application not found'}), 404
        return jsonify({'success': True, 'application': application}), 200
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

# ==================== Withdraw Application ====================
@freelancer_bp.route('/applications/<int:application_id>/withdraw', methods=['DELETE'])
@token_required
@freelancer_required
def withdraw_application(application_id):
    try:
        success = JobApplication.withdraw(application_id, request.user_id)
        if not success:
            return jsonify({'success': False, 'message': 'Unable to withdraw application'}), 400
        return jsonify({'success': True, 'message': 'Application withdrawn successfully'}), 200
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500