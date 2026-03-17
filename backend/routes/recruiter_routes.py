# from flask import Blueprint, request, jsonify
# from database.models import RecruiterProfile, Job, JobApplication, Notification
# from services.email_service import EmailService
# from utils.auth_utils import token_required, recruiter_required
# from datetime import datetime
# import traceback

# recruiter_bp = Blueprint('recruiter', __name__, url_prefix='/api/recruiter')

# @recruiter_bp.route('/jobs', methods=['POST'])
# @token_required
# @recruiter_required
# def create_job():
#     """Create a new job posting with email notification"""
#     try:
#         data = request.get_json()
        
#         # Validate required fields
#         required_fields = ['title', 'description', 'pay_per_hour', 'experience_level']
#         for field in required_fields:
#             if field not in data or not data[field]:
#                 return jsonify({
#                     'success': False,
#                     'message': f'{field} is required'
#                 }), 400
        
#         job_id = Job.create(request.user_id, data)
        
#         if not job_id:
#             return jsonify({
#                 'success': False,
#                 'message': 'Failed to create job'
#             }), 400
        
#         # Send email notification to recruiter
#         EmailService.send_job_posted_notification(job_id)
        
#         job = Job.get_by_id(job_id)
        
#         return jsonify({
#             'success': True,
#             'message': 'Job posted successfully! We\'ve sent you a confirmation email.',
#             'job': job
#         }), 201
        
#     except Exception as e:
#         print(f"❌ Error in create_job: {str(e)}")
#         traceback.print_exc()
#         return jsonify({
#             'success': False,
#             'message': f'Failed to create job: {str(e)}'
#         }), 500

# @recruiter_bp.route('/applications/<int:application_id>/status', methods=['PUT'])
# @token_required
# @recruiter_required
# def update_application_status(application_id):
#     """Update job application status with email notification"""
#     try:
#         data = request.get_json()
        
#         if 'status' not in data:
#             return jsonify({
#                 'success': False,
#                 'message': 'Status is required'
#             }), 400
        
#         valid_statuses = ['reviewed', 'shortlisted', 'accepted', 'rejected']
#         if data['status'] not in valid_statuses:
#             return jsonify({
#                 'success': False,
#                 'message': f'Invalid status. Must be one of: {", ".join(valid_statuses)}'
#             }), 400
        
#         application = JobApplication.update_status(
#             application_id,
#             data['status'],
#             data.get('recruiter_notes')
#         )
        
#         if not application:
#             return jsonify({
#                 'success': False,
#                 'message': 'Application not found'
#             }), 404
        
#         # Send email notification to freelancer
#         EmailService.send_application_status_update(
#             application_id,
#             data['status'],
#             data.get('recruiter_notes')
#         )
        
#         # Create in-app notification for freelancer
#         Notification.create(
#             user_id=application['freelancer_id'],
#             title=f'Application {data["status"].title()}',
#             message=f'Your application for {application["title"]} has been {data["status"]}',
#             notification_type='application',
#             related_application_id=application_id,
#             related_job_id=application['job_id']
#         )
        
#         return jsonify({
#             'success': True,
#             'message': f'Application {data["status"]} successfully. Freelancer has been notified.',
#             'application': application
#         }), 200
        
#     except Exception as e:
#         print(f"❌ Error in update_application_status: {str(e)}")
#         traceback.print_exc()   
#         return jsonify({
#             'success': False,
#             'message': f'Failed to update status: {str(e)}'
#         }), 500

from flask import Blueprint, current_app, request, jsonify
from database.models import RecruiterProfile, Job, JobApplication, Notification, User
from services.email_instance import email_service
from utils.auth_utils import token_required, recruiter_required
from datetime import datetime
import traceback

recruiter_bp = Blueprint('recruiter', __name__, url_prefix='/api/recruiter')

# ==================== Dashboard ====================
@recruiter_bp.route('/dashboard', methods=['GET'])
@token_required
@recruiter_required
def get_dashboard():
    try:
        profile = RecruiterProfile.get_by_user_id(request.user_id)
        stats = RecruiterProfile.get_stats(request.user_id)
        recent_jobs = Job.get_recent_by_recruiter(request.user_id, limit=5)
        recent_applications = JobApplication.get_recent_for_recruiter(request.user_id, limit=5)

        return jsonify({
            'success': True,
            'profile': profile,
            'stats': stats,
            'recent_jobs': recent_jobs,
            'recent_applications': recent_applications
        }), 200
    except Exception as e:
        traceback.print_exc()
        return jsonify({'success': False, 'message': str(e)}), 500

# ==================== Profile ====================
@recruiter_bp.route('/profile', methods=['GET', 'PUT'])
@token_required
@recruiter_required
def profile():
    if request.method == 'GET':
        try:
            profile = RecruiterProfile.get_by_user_id(request.user_id)
            if not profile:
                profile = RecruiterProfile.create_empty(request.user_id)
                if not profile:
                    return jsonify({'success': False, 'message': 'Failed to create profile'}), 500
            return jsonify({'success': True, 'profile': profile}), 200
        except Exception as e:
            traceback.print_exc()
            return jsonify({'success': False, 'message': str(e)}), 500

    elif request.method == 'PUT':
        try:
            data = request.get_json()
            success = RecruiterProfile.update(request.user_id, data)
            if not success:
                return jsonify({'success': False, 'message': 'Profile not found'}), 404
            profile = RecruiterProfile.get_by_user_id(request.user_id)
            return jsonify({'success': True, 'profile': profile}), 200
        except Exception as e:
            traceback.print_exc()
            return jsonify({'success': False, 'message': str(e)}), 500

# ==================== Job Management ====================
@recruiter_bp.route('/jobs', methods=['GET'])
@token_required
@recruiter_required 
def get_my_jobs():
    try:
        jobs = Job.get_by_recruiter(request.user_id)
        return jsonify({'success': True, 'jobs': jobs}), 200
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500
    
# @recruiter_bp.route('/jobs', methods=['POST'])
# @token_required
# @recruiter_required
# def create_job():
#     try:
#         data = request.get_json()
#         # ... validation ...
#         job_id = Job.create(request.user_id, data)
#         if not job_id:
#             return jsonify({'success': False, 'message': 'Failed to create job'}), 400

#         job = Job.get_by_id(job_id)
#         recruiter = User.find_by_id(request.user_id)
#         recruiter_name = f"{recruiter['first_name']} {recruiter['last_name']}"

#         # Send confirmation email
#         email_service.send_job_posted_notification(
#             to_email=recruiter['email'],
#             recruiter_name=recruiter_name,
#             job_title=job['title'],
#             job_id=job_id,
#             user_id=request.user_id
#         )

#         return jsonify({'success': True, 'message': 'Job posted successfully!', 'job': job}), 201
#     except Exception as e:
#         traceback.print_exc()
#         return jsonify({'success': False, 'message': f'Failed to create job: {str(e)}'}), 500
@recruiter_bp.route('/jobs', methods=['POST'])
@token_required
@recruiter_required
def create_job():
    try:
        data = request.get_json()
        # Validate required fields
        required_fields = ['title', 'description', 'pay_per_hour', 'experience_level']
        for field in required_fields:
            if field not in data or not data[field]:
                return jsonify({'success': False, 'message': f'{field} is required'}), 400

        job_id = Job.create(request.user_id, data)
        if not job_id:
            return jsonify({'success': False, 'message': 'Failed to create job'}), 400

        job = Job.get_by_id(job_id)
        recruiter = User.find_by_id(request.user_id)
        recruiter_name = f"{recruiter['first_name']} {recruiter['last_name']}"

        # Safely get email service from app config
        email_svc = current_app.config.get('EMAIL_SERVICE')
        if email_svc:
            try:
                email_svc.send_job_posted_notification(
                    to_email=recruiter['email'],
                    recruiter_name=recruiter_name,
                    job_title=job['title'],
                    job_id=job_id,
                    user_id=request.user_id
                )
            except Exception as email_err:
                # Log email error but don't fail the request
                print(f"⚠️ Email notification failed: {email_err}")
                traceback.print_exc()
        else:
            print("❌ EMAIL_SERVICE not available in app config")

        return jsonify({'success': True, 'message': 'Job posted successfully!', 'job': job}), 201
    except Exception as e:
        traceback.print_exc()
        return jsonify({'success': False, 'message': f'Failed to create job: {str(e)}'}), 500

@recruiter_bp.route('/jobs/<int:job_id>', methods=['GET'])
@token_required
@recruiter_required
def get_job(job_id):
    try:
        job = Job.get_by_id(job_id)
        if not job or job['recruiter_id'] != request.user_id:
            return jsonify({'success': False, 'message': 'Job not found'}), 404
        return jsonify({'success': True, 'job': job}), 200
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@recruiter_bp.route('/jobs/<int:job_id>', methods=['PUT'])
@token_required
@recruiter_required
def update_job(job_id):
    try:
        data = request.get_json()
        success = Job.update(job_id, request.user_id, data)
        if not success:
            return jsonify({'success': False, 'message': 'Unable to update job'}), 400
        job = Job.get_by_id(job_id)
        recruiter = User.find_by_id(request.user_id)
        recruiter_name = f"{recruiter['first_name']} {recruiter['last_name']}"
        if email_service:
            try:
                email_service.send_job_updated_notification(
                    to_email=recruiter['email'],
                    recruiter_name=recruiter_name,
                    job_title=job['title'],
                    job_id=job_id,
                    user_id=request.user_id
                )
            except Exception as email_err:
                print(f"⚠️ Job update email failed: {email_err}")
                traceback.print_exc()

        return jsonify({'success': True, 'job': job}), 200
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@recruiter_bp.route('/applications', methods=['GET'])
@token_required
@recruiter_required
def get_all_applications():
    try:
        jobs = Job.get_by_recruiter(request.user_id)
        job_ids = [job['id'] for job in jobs]
        if not job_ids:
            return jsonify({'success': True, 'applications': []})
        applications = JobApplication.get_by_job_ids(job_ids)
        return jsonify({'success': True, 'applications': applications})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

# @recruiter_bp.route('/jobs/<int:job_id>/toggle', methods=['POST'])
# @token_required
# @recruiter_required
# def toggle_job_status(job_id):
#     try:
#         success = Job.toggle_active(job_id, request.user_id)
#         if not success:
#             return jsonify({'success': False, 'message': 'Unable to toggle job status'}), 400
#         job = Job.get_by_id(job_id)
#         return jsonify({'success': True, 'job': job}), 200
#     except Exception as e:
#         return jsonify({'success': False, 'message': str(e)}), 500
@recruiter_bp.route('/jobs/<int:job_id>/toggle', methods=['POST'])
@token_required
@recruiter_required
def toggle_job_status(job_id):
    try:
        is_active = Job.toggle_active(job_id, request.user_id)
        if is_active is None:
            return jsonify({'success': False, 'message': 'Unable to toggle job status'}), 400
        job = Job.get_by_id(job_id)
        recruiter = User.find_by_id(request.user_id)
        recruiter_name = f"{recruiter['first_name']} {recruiter['last_name']}"

        # Send job status change notification
        if email_service:
            try:
                email_service.send_job_status_changed_notification(
                    to_email=recruiter['email'],
                    recruiter_name=recruiter_name,
                    job_title=job['title'],
                    job_id=job_id,
                    is_active=is_active,
                    user_id=request.user_id
                )
            except Exception as email_err:
                print(f"⚠️ Job status email failed: {email_err}")
                traceback.print_exc()

        return jsonify({'success': True, 'job': job}), 200
    except Exception as e:
        traceback.print_exc()
        return jsonify({'success': False, 'message': str(e)}), 500

# ==================== Applications Management ====================
@recruiter_bp.route('/jobs/<int:job_id>/applications', methods=['GET'])
@token_required
@recruiter_required
def get_job_applications(job_id):
    try:
        # Ensure job belongs to recruiter
        job = Job.get_by_id(job_id)
        if not job or job['recruiter_id'] != request.user_id:
            return jsonify({'success': False, 'message': 'Job not found'}), 404

        applications = JobApplication.get_by_job(job_id)
        return jsonify({'success': True, 'applications': applications}), 200
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@recruiter_bp.route('/applications/<int:application_id>', methods=['GET'])
@token_required
@recruiter_required
def get_application_details(application_id):
    try:
        application = JobApplication.get_by_id(application_id)
        if not application:
            return jsonify({'success': False, 'message': 'Application not found'}), 404

        # Ensure application belongs to recruiter's job
        job = Job.get_by_id(application['job_id'])
        if not job or job['recruiter_id'] != request.user_id:
            return jsonify({'success': False, 'message': 'Access denied'}), 403

        return jsonify({'success': True, 'application': application}), 200
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500
@recruiter_bp.route('/applications/<int:application_id>/status', methods=['PUT'])
@token_required
@recruiter_required
def update_application_status(application_id):
    try:
        data = request.get_json()
        if 'status' not in data:
            return jsonify({'success': False, 'message': 'Status is required'}), 400

        valid_statuses = ['reviewed', 'shortlisted', 'accepted', 'rejected']
        if data['status'] not in valid_statuses:
            return jsonify({
                'success': False,
                'message': f'Invalid status. Must be one of: {", ".join(valid_statuses)}'
            }), 400

        application = JobApplication.update_status(
            application_id,
            data['status'],
            data.get('recruiter_notes')
        )

        if not application:
            return jsonify({'success': False, 'message': 'Application not found'}), 404

        # Get job and freelancer details
        job = Job.get_by_id(application['job_id'])
        freelancer = User.find_by_id(application['freelancer_id'])
        freelancer_name = f"{freelancer['first_name']} {freelancer['last_name']}"

        # Send email to freelancer using app config
        email_service = current_app.config.get('EMAIL_SERVICE')
        if email_service:
            email_service.send_application_status_update(
                to_email=freelancer['email'],
                freelancer_name=freelancer_name,
                job_title=job['title'],
                status=data['status'],
                recruiter_notes=data.get('recruiter_notes'),
                job_id=application['job_id'],
                user_id=freelancer['id']
            )

        # In-app notification
        Notification.create(
            user_id=application['freelancer_id'],
            title=f'Application {data["status"].title()}',
            message=f'Your application for {job["title"]} has been {data["status"]}',
            notification_type='application',
            related_application_id=application_id,
            related_job_id=application['job_id']
        )

        return jsonify({
            'success': True,
            'message': f'Application {data["status"]} successfully. Freelancer has been notified.'
        }), 200

    except Exception as e:
        traceback.print_exc()
        return jsonify({'success': False, 'message': f'Failed to update status: {str(e)}'}), 500