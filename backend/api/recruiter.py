from flask import Blueprint, request, jsonify
from database.models import RecruiterProfile, Job, JobApplication, Notification
from utils.auth_utils import token_required, recruiter_required

recruiter_bp = Blueprint('recruiter', __name__, url_prefix='/api/recruiter')

@recruiter_bp.route('/profile', methods=['GET'])
@token_required
@recruiter_required
def get_profile():
    """Get recruiter profile"""
    profile = RecruiterProfile.get_by_user_id(request.user_id)
    
    if not profile:
        return jsonify({
            'success': False,
            'message': 'Profile not found'
        }), 404
    
    return jsonify({
        'success': True,
        'profile': profile
    }), 200

@recruiter_bp.route('/profile', methods=['PUT'])
@token_required
@recruiter_required
def update_profile():
    """Update recruiter profile"""
    data = request.get_json()
    
    profile = RecruiterProfile.update_profile(request.user_id, data)
    
    if not profile:
        return jsonify({
            'success': False,
            'message': 'Profile not found'
        }), 404
    
    return jsonify({
        'success': True,
        'message': 'Profile updated successfully',
        'profile': profile
    }), 200

@recruiter_bp.route('/jobs', methods=['POST'])
@token_required
@recruiter_required
def create_job():
    """Create a new job posting"""
    data = request.get_json()
    
    # Validate required fields
    required_fields = ['title', 'description', 'pay_per_hour', 'experience_level']
    for field in required_fields:
        if field not in data or not data[field]:
            return jsonify({
                'success': False,
                'message': f'{field} is required'
            }), 400
    
    job_id = Job.create(request.user_id, data)
    
    if not job_id:
        return jsonify({
            'success': False,
            'message': 'Failed to create job'
        }), 400
    
    job = Job.get_by_id(job_id)
    
    return jsonify({
        'success': True,
        'message': 'Job posted successfully',
        'job': job
    }), 201

@recruiter_bp.route('/jobs', methods=['GET'])
@token_required
@recruiter_required
def get_my_jobs():
    """Get all jobs posted by recruiter"""
    jobs = Job.get_by_recruiter(request.user_id)
    
    return jsonify({
        'success': True,
        'count': len(jobs),
        'jobs': jobs
    }), 200

@recruiter_bp.route('/jobs/<int:job_id>/applications', methods=['GET'])
@token_required
@recruiter_required
def get_job_applications(job_id):
    """Get all applications for a specific job"""
    # Verify job belongs to recruiter
    job = Job.get_by_id(job_id)
    if not job or job['recruiter_id'] != request.user_id:
        return jsonify({
            'success': False,
            'message': 'Job not found or unauthorized'
        }), 404
    
    applications = JobApplication.get_by_job(job_id)
    
    return jsonify({
        'success': True,
        'count': len(applications),
        'applications': applications
    }), 200

@recruiter_bp.route('/applications/<int:application_id>/status', methods=['PUT'])
@token_required
@recruiter_required
def update_application_status(application_id):
    """Update job application status"""
    data = request.get_json()
    
    if 'status' not in data:
        return jsonify({
            'success': False,
            'message': 'Status is required'
        }), 400
    
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
        return jsonify({
            'success': False,
            'message': 'Application not found'
        }), 404
    
    # Create notification for freelancer
    Notification.create(
        user_id=application['freelancer_id'],
        title=f'Application {data["status"].title()}',
        message=f'Your application for {application["title"]} has been {data["status"]}',
        notification_type='application',
        related_application_id=application_id,
        related_job_id=application['job_id']
    )
    
    return jsonify({
        'success': True,
        'message': f'Application {data["status"]} successfully',
        'application': application
    }), 200

@recruiter_bp.route('/dashboard', methods=['GET'])
@token_required
@recruiter_required
def get_dashboard():
    """Get recruiter dashboard data"""
    jobs = Job.get_by_recruiter(request.user_id)
    profile = RecruiterProfile.get_by_user_id(request.user_id)
    
    # Get all applications for all jobs
    all_applications = []
    for job in jobs:
        applications = JobApplication.get_by_job(job['id'])
        all_applications.extend(applications)
    
    stats = {
        'total_jobs': len(jobs),
        'active_jobs': sum(1 for j in jobs if j['is_active']),
        'total_applications': len(all_applications),
        'pending_applications': sum(1 for a in all_applications if a['status'] == 'applied'),
        'shortlisted_applications': sum(1 for a in all_applications if a['status'] == 'shortlisted'),
        'accepted_applications': sum(1 for a in all_applications if a['status'] == 'accepted')
    }
    
    return jsonify({
        'success': True,
        'profile': profile,
        'recent_jobs': jobs[:5],
        'recent_applications': all_applications[:10],
        'stats': stats
    }), 200