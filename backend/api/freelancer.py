from flask import Blueprint, request, jsonify
from database.models import FreelancerProfile, Job, JobApplication, Notification
from utils.auth_utils import token_required, freelancer_required
from datetime import datetime
import traceback

freelancer_bp = Blueprint('freelancer', __name__, url_prefix='/api/freelancer')

@freelancer_bp.route('/profile', methods=['GET'])
@token_required
@freelancer_required
def get_profile():
    """Get freelancer profile"""
    try:
        profile = FreelancerProfile.get_by_user_id(request.user_id)
        
        if not profile:
            return jsonify({
                'success': False,
                'message': 'Profile not found'
            }), 404
        
        return jsonify({
            'success': True,
            'profile': profile
        }), 200
    except Exception as e:
        print(f"Error in get_profile: {str(e)}")
        traceback.print_exc()
        return jsonify({
            'success': False,
            'message': f'Server error: {str(e)}'
        }), 500

@freelancer_bp.route('/profile', methods=['PUT'])
@token_required
@freelancer_required
def update_profile():
    """Update freelancer profile"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                'success': False,
                'message': 'No data provided'
            }), 400
        
        profile = FreelancerProfile.update_profile(request.user_id, data)
        
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
    except Exception as e:
        print(f"Error in update_profile: {str(e)}")
        traceback.print_exc()
        return jsonify({
            'success': False,
            'message': f'Server error: {str(e)}'
        }), 500

@freelancer_bp.route('/jobs/search', methods=['GET'])
@token_required
@freelancer_required
def search_jobs():
    """Search for jobs with improved filtering"""
    try:
        # Get filter parameters
        search = request.args.get('search', '')
        experience_level = request.args.get('experience_level', '')
        min_pay = request.args.get('min_pay', '')
        max_pay = request.args.get('max_pay', '')
        job_type = request.args.get('job_type', '')
        is_remote = request.args.get('is_remote', '')
        
        # Build filters dictionary (only include non-empty values)
        filters = {}
        if search and search.strip():
            filters['search'] = search.strip()
        if experience_level and experience_level.strip():
            filters['experience_level'] = experience_level.strip()
        if min_pay and min_pay.strip():
            try:
                filters['min_pay'] = float(min_pay)
            except ValueError:
                pass
        if max_pay and max_pay.strip():
            try:
                filters['max_pay'] = float(max_pay)
            except ValueError:
                pass
        if job_type and job_type.strip() and job_type != 'All Types':
            filters['job_type'] = job_type.strip()
        if is_remote and is_remote.lower() == 'true':
            filters['is_remote'] = True
        
        print(f"🔍 Search filters: {filters}")  # Debug log
        
        jobs = Job.search_jobs(filters)
        
        print(f"✅ Found {len(jobs)} jobs")  # Debug log
        
        return jsonify({
            'success': True,
            'count': len(jobs),
            'jobs': jobs
        }), 200
        
    except Exception as e:
        print(f"❌ Error in search_jobs: {str(e)}")
        traceback.print_exc()
        return jsonify({
            'success': False,
            'message': f'Search failed: {str(e)}',
            'jobs': []
        }), 500

@freelancer_bp.route('/jobs/<int:job_id>', methods=['GET'])
@token_required
@freelancer_required
def get_job_details(job_id):
    """Get job details by ID"""
    try:
        print(f"🔍 Fetching job details for ID: {job_id}")
        job = Job.get_by_id(job_id)
        
        if not job:
            return jsonify({
                'success': False,
                'message': 'Job not found'
            }), 404
        
        return jsonify({
            'success': True,
            'job': job
        }), 200
    except Exception as e:
        print(f"❌ Error in get_job_details: {str(e)}")
        traceback.print_exc()
        return jsonify({
            'success': False,
            'message': f'Server error: {str(e)}'
        }), 500

@freelancer_bp.route('/jobs/<int:job_id>/apply', methods=['POST'])
@token_required
@freelancer_required
def apply_for_job(job_id):
    """Apply for a job"""
    try:
        data = request.get_json() or {}
        
        # Validate required fields
        if not data.get('cover_letter'):
            return jsonify({
                'success': False,
                'message': 'Cover letter is required'
            }), 400
        
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
        
        # Create notification for recruiter
        job = Job.get_by_id(job_id)
        if job:
            Notification.create(
                user_id=job['recruiter_id'],
                title='New Job Application',
                message=f'A freelancer has applied for {job["title"]}',
                notification_type='application',
                related_application_id=application_id,
                related_job_id=job_id
            )
            print(f"📧 Notification created for recruiter {job['recruiter_id']}")
        
        return jsonify({
            'success': True,
            'message': 'Application submitted successfully',
            'application_id': application_id
        }), 201
        
    except Exception as e:
        print(f"❌ Error in apply_for_job: {str(e)}")
        traceback.print_exc()
        return jsonify({
            'success': False,
            'message': f'Application failed: {str(e)}'
        }), 500

@freelancer_bp.route('/applications', methods=['GET'])
@token_required
@freelancer_required
def get_applications():
    """Get all applications by freelancer"""
    try:
        applications = JobApplication.get_by_freelancer(request.user_id)
        
        return jsonify({
            'success': True,
            'count': len(applications),
            'applications': applications
        }), 200
    except Exception as e:
        print(f"❌ Error in get_applications: {str(e)}")
        traceback.print_exc()
        return jsonify({
            'success': False,
            'message': f'Server error: {str(e)}'
        }), 500

@freelancer_bp.route('/dashboard', methods=['GET'])
@token_required
@freelancer_required
def get_dashboard():
    """Get freelancer dashboard data"""
    try:
        profile = FreelancerProfile.get_by_user_id(request.user_id)
        applications = JobApplication.get_by_freelancer(request.user_id)
        
        # Get recommended jobs based on skills
        recommended_jobs = []
        if profile and profile.get('skills'):
            skill_names = [s['name'] for s in profile['skills']]
            print(f"🎯 Freelancer skills: {skill_names}")
            
            if skill_names:
                # Search for jobs with matching skills
                for skill in skill_names[:3]:  # Use top 3 skills
                    jobs = Job.search_jobs({'search': skill})
                    if jobs:
                        print(f"Found {len(jobs)} jobs for skill: {skill}")
                        recommended_jobs.extend(jobs[:2])  # Take top 2 per skill
        
        # Remove duplicates
        seen = set()
        unique_jobs = []
        for job in recommended_jobs:
            if job['id'] not in seen:
                seen.add(job['id'])
                unique_jobs.append(job)
        
        print(f"📊 Recommended {len(unique_jobs)} unique jobs")
        
        # Calculate profile completion percentage
        profile_completion = 0
        if profile:
            fields = ['bio', 'hourly_rate', 'education', 'experience', 
                     'github_url', 'linkedin_url', 'portfolio_url']
            completed = sum(1 for field in fields if profile.get(field))
            if profile.get('skills') and len(profile['skills']) > 0:
                completed += 1
            if profile.get('tech_stacks') and len(profile['tech_stacks']) > 0:
                completed += 1
            total_fields = len(fields) + 2
            profile_completion = int((completed / total_fields) * 100)
        
        stats = {
            'total_applications': len(applications),
            'pending_applications': sum(1 for a in applications if a['status'] == 'applied'),
            'accepted_applications': sum(1 for a in applications if a['status'] == 'accepted'),
            'rejected_applications': sum(1 for a in applications if a['status'] == 'rejected'),
            'profile_completion': profile_completion
        }
        
        return jsonify({
            'success': True,
            'profile': profile,
            'recent_applications': applications[:5],
            'recommended_jobs': unique_jobs[:6],
            'stats': stats
        }), 200
        
    except Exception as e:
        print(f"❌ Error in get_dashboard: {str(e)}")
        traceback.print_exc()
        return jsonify({
            'success': False,
            'message': f'Server error: {str(e)}'
        }), 500