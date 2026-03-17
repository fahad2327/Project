# # # # # # # # from flask import Blueprint, request, jsonify
# # # # # # # # from database.models import FreelancerProfile, Job, JobApplication, Notification
# # # # # # # # from utils.auth_utils import token_required, freelancer_required
# # # # # # # # from datetime import datetime
# # # # # # # # import traceback

# # # # # # # # freelancer_bp = Blueprint('freelancer', __name__, url_prefix='/api/freelancer')

# # # # # # # # @freelancer_bp.route('/profile', methods=['GET'])
# # # # # # # # @token_required
# # # # # # # # @freelancer_required
# # # # # # # # def get_profile():
# # # # # # # #     """Get freelancer profile"""
# # # # # # # #     try:
# # # # # # # #         profile = FreelancerProfile.get_by_user_id(request.user_id)
        
# # # # # # # #         if not profile:
# # # # # # # #             return jsonify({
# # # # # # # #                 'success': False,
# # # # # # # #                 'message': 'Profile not found'
# # # # # # # #             }), 404
        
# # # # # # # #         return jsonify({
# # # # # # # #             'success': True,
# # # # # # # #             'profile': profile
# # # # # # # #         }), 200
# # # # # # # #     except Exception as e:
# # # # # # # #         print(f"Error in get_profile: {str(e)}")
# # # # # # # #         traceback.print_exc()
# # # # # # # #         return jsonify({
# # # # # # # #             'success': False,
# # # # # # # #             'message': f'Server error: {str(e)}'
# # # # # # # #         }), 500

# # # # # # # # @freelancer_bp.route('/profile', methods=['PUT'])
# # # # # # # # @token_required
# # # # # # # # @freelancer_required
# # # # # # # # def update_profile():
# # # # # # # #     """Update freelancer profile"""
# # # # # # # #     try:
# # # # # # # #         data = request.get_json()
        
# # # # # # # #         if not data:
# # # # # # # #             return jsonify({
# # # # # # # #                 'success': False,
# # # # # # # #                 'message': 'No data provided'
# # # # # # # #             }), 400
        
# # # # # # # #         profile = FreelancerProfile.update_profile(request.user_id, data)
        
# # # # # # # #         if not profile:
# # # # # # # #             return jsonify({
# # # # # # # #                 'success': False,
# # # # # # # #                 'message': 'Profile not found'
# # # # # # # #             }), 404
        
# # # # # # # #         return jsonify({
# # # # # # # #             'success': True,
# # # # # # # #             'message': 'Profile updated successfully',
# # # # # # # #             'profile': profile
# # # # # # # #         }), 200
# # # # # # # #     except Exception as e:
# # # # # # # #         print(f"Error in update_profile: {str(e)}")
# # # # # # # #         traceback.print_exc()
# # # # # # # #         return jsonify({
# # # # # # # #             'success': False,
# # # # # # # #             'message': f'Server error: {str(e)}'
# # # # # # # #         }), 500

# # # # # # # # @freelancer_bp.route('/jobs/search', methods=['GET'])
# # # # # # # # @token_required
# # # # # # # # @freelancer_required
# # # # # # # # def search_jobs():
# # # # # # # #     """Search for jobs with improved filtering"""
# # # # # # # #     try:
# # # # # # # #         # Get filter parameters
# # # # # # # #         search = request.args.get('search', '')
# # # # # # # #         experience_level = request.args.get('experience_level', '')
# # # # # # # #         min_pay = request.args.get('min_pay', '')
# # # # # # # #         max_pay = request.args.get('max_pay', '')
# # # # # # # #         job_type = request.args.get('job_type', '')
# # # # # # # #         is_remote = request.args.get('is_remote', '')
        
# # # # # # # #         # Build filters dictionary (only include non-empty values)
# # # # # # # #         filters = {}
# # # # # # # #         if search and search.strip():
# # # # # # # #             filters['search'] = search.strip()
# # # # # # # #         if experience_level and experience_level.strip():
# # # # # # # #             filters['experience_level'] = experience_level.strip()
# # # # # # # #         if min_pay and min_pay.strip():
# # # # # # # #             try:
# # # # # # # #                 filters['min_pay'] = float(min_pay)
# # # # # # # #             except ValueError:
# # # # # # # #                 pass
# # # # # # # #         if max_pay and max_pay.strip():
# # # # # # # #             try:
# # # # # # # #                 filters['max_pay'] = float(max_pay)
# # # # # # # #             except ValueError:
# # # # # # # #                 pass
# # # # # # # #         if job_type and job_type.strip() and job_type != 'All Types':
# # # # # # # #             filters['job_type'] = job_type.strip()
# # # # # # # #         if is_remote and is_remote.lower() == 'true':
# # # # # # # #             filters['is_remote'] = True
        
# # # # # # # #         print(f"🔍 Search filters: {filters}")  # Debug log
        
# # # # # # # #         jobs = Job.search_jobs(filters)
        
# # # # # # # #         print(f"✅ Found {len(jobs)} jobs")  # Debug log
        
# # # # # # # #         return jsonify({
# # # # # # # #             'success': True,
# # # # # # # #             'count': len(jobs),
# # # # # # # #             'jobs': jobs
# # # # # # # #         }), 200
        
# # # # # # # #     except Exception as e:
# # # # # # # #         print(f"❌ Error in search_jobs: {str(e)}")
# # # # # # # #         traceback.print_exc()
# # # # # # # #         return jsonify({
# # # # # # # #             'success': False,
# # # # # # # #             'message': f'Search failed: {str(e)}',
# # # # # # # #             'jobs': []
# # # # # # # #         }), 500

# # # # # # # # @freelancer_bp.route('/jobs/<int:job_id>', methods=['GET'])
# # # # # # # # @token_required
# # # # # # # # @freelancer_required
# # # # # # # # def get_job_details(job_id):
# # # # # # # #     """Get job details by ID"""
# # # # # # # #     try:
# # # # # # # #         print(f"🔍 Fetching job details for ID: {job_id}")
# # # # # # # #         job = Job.get_by_id(job_id)
        
# # # # # # # #         if not job:
# # # # # # # #             return jsonify({
# # # # # # # #                 'success': False,
# # # # # # # #                 'message': 'Job not found'
# # # # # # # #             }), 404
        
# # # # # # # #         return jsonify({
# # # # # # # #             'success': True,
# # # # # # # #             'job': job
# # # # # # # #         }), 200
# # # # # # # #     except Exception as e:
# # # # # # # #         print(f"❌ Error in get_job_details: {str(e)}")
# # # # # # # #         traceback.print_exc()
# # # # # # # #         return jsonify({
# # # # # # # #             'success': False,
# # # # # # # #             'message': f'Server error: {str(e)}'
# # # # # # # #         }), 500

# # # # # # # # @freelancer_bp.route('/jobs/<int:job_id>/apply', methods=['POST'])
# # # # # # # # @token_required
# # # # # # # # @freelancer_required
# # # # # # # # def apply_for_job(job_id):
# # # # # # # #     """Apply for a job"""
# # # # # # # #     try:
# # # # # # # #         data = request.get_json() or {}
        
# # # # # # # #         # Validate required fields
# # # # # # # #         if not data.get('cover_letter'):
# # # # # # # #             return jsonify({
# # # # # # # #                 'success': False,
# # # # # # # #                 'message': 'Cover letter is required'
# # # # # # # #             }), 400
        
# # # # # # # #         application_id = JobApplication.create(
# # # # # # # #             job_id=job_id,
# # # # # # # #             freelancer_id=request.user_id,
# # # # # # # #             application_data=data
# # # # # # # #         )
        
# # # # # # # #         if not application_id:
# # # # # # # #             return jsonify({
# # # # # # # #                 'success': False,
# # # # # # # #                 'message': 'You have already applied for this job or job not found'
# # # # # # # #             }), 400
        
# # # # # # # #         # Create notification for recruiter
# # # # # # # #         job = Job.get_by_id(job_id)
# # # # # # # #         if job:
# # # # # # # #             Notification.create(
# # # # # # # #                 user_id=job['recruiter_id'],
# # # # # # # #                 title='New Job Application',
# # # # # # # #                 message=f'A freelancer has applied for {job["title"]}',
# # # # # # # #                 notification_type='application',
# # # # # # # #                 related_application_id=application_id,
# # # # # # # #                 related_job_id=job_id
# # # # # # # #             )
# # # # # # # #             print(f"📧 Notification created for recruiter {job['recruiter_id']}")
        
# # # # # # # #         return jsonify({
# # # # # # # #             'success': True,
# # # # # # # #             'message': 'Application submitted successfully',
# # # # # # # #             'application_id': application_id
# # # # # # # #         }), 201
        
# # # # # # # #     except Exception as e:
# # # # # # # #         print(f"❌ Error in apply_for_job: {str(e)}")
# # # # # # # #         traceback.print_exc()
# # # # # # # #         return jsonify({
# # # # # # # #             'success': False,
# # # # # # # #             'message': f'Application failed: {str(e)}'
# # # # # # # #         }), 500

# # # # # # # # @freelancer_bp.route('/applications', methods=['GET'])
# # # # # # # # @token_required
# # # # # # # # @freelancer_required
# # # # # # # # def get_applications():
# # # # # # # #     """Get all applications by freelancer"""
# # # # # # # #     try:
# # # # # # # #         applications = JobApplication.get_by_freelancer(request.user_id)
        
# # # # # # # #         return jsonify({
# # # # # # # #             'success': True,
# # # # # # # #             'count': len(applications),
# # # # # # # #             'applications': applications
# # # # # # # #         }), 200
# # # # # # # #     except Exception as e:
# # # # # # # #         print(f"❌ Error in get_applications: {str(e)}")
# # # # # # # #         traceback.print_exc()
# # # # # # # #         return jsonify({
# # # # # # # #             'success': False,
# # # # # # # #             'message': f'Server error: {str(e)}'
# # # # # # # #         }), 500

# # # # # # # # @freelancer_bp.route('/dashboard', methods=['GET'])
# # # # # # # # @token_required
# # # # # # # # @freelancer_required
# # # # # # # # def get_dashboard():
# # # # # # # #     """Get freelancer dashboard data"""
# # # # # # # #     try:
# # # # # # # #         profile = FreelancerProfile.get_by_user_id(request.user_id)
# # # # # # # #         applications = JobApplication.get_by_freelancer(request.user_id)
        
# # # # # # # #         # Get recommended jobs based on skills
# # # # # # # #         recommended_jobs = []
# # # # # # # #         if profile and profile.get('skills'):
# # # # # # # #             skill_names = [s['name'] for s in profile['skills']]
# # # # # # # #             print(f"🎯 Freelancer skills: {skill_names}")
            
# # # # # # # #             if skill_names:
# # # # # # # #                 # Search for jobs with matching skills
# # # # # # # #                 for skill in skill_names[:3]:  # Use top 3 skills
# # # # # # # #                     jobs = Job.search_jobs({'search': skill})
# # # # # # # #                     if jobs:
# # # # # # # #                         print(f"Found {len(jobs)} jobs for skill: {skill}")
# # # # # # # #                         recommended_jobs.extend(jobs[:2])  # Take top 2 per skill
        
# # # # # # # #         # Remove duplicates
# # # # # # # #         seen = set()
# # # # # # # #         unique_jobs = []
# # # # # # # #         for job in recommended_jobs:
# # # # # # # #             if job['id'] not in seen:
# # # # # # # #                 seen.add(job['id'])
# # # # # # # #                 unique_jobs.append(job)
        
# # # # # # # #         print(f"📊 Recommended {len(unique_jobs)} unique jobs")
        
# # # # # # # #         # Calculate profile completion percentage
# # # # # # # #         profile_completion = 0
# # # # # # # #         if profile:
# # # # # # # #             fields = ['bio', 'hourly_rate', 'education', 'experience', 
# # # # # # # #                      'github_url', 'linkedin_url', 'portfolio_url']
# # # # # # # #             completed = sum(1 for field in fields if profile.get(field))
# # # # # # # #             if profile.get('skills') and len(profile['skills']) > 0:
# # # # # # # #                 completed += 1
# # # # # # # #             if profile.get('tech_stacks') and len(profile['tech_stacks']) > 0:
# # # # # # # #                 completed += 1
# # # # # # # #             total_fields = len(fields) + 2
# # # # # # # #             profile_completion = int((completed / total_fields) * 100)
        
# # # # # # # #         stats = {
# # # # # # # #             'total_applications': len(applications),
# # # # # # # #             'pending_applications': sum(1 for a in applications if a['status'] == 'applied'),
# # # # # # # #             'accepted_applications': sum(1 for a in applications if a['status'] == 'accepted'),
# # # # # # # #             'rejected_applications': sum(1 for a in applications if a['status'] == 'rejected'),
# # # # # # # #             'profile_completion': profile_completion
# # # # # # # #         }
        
# # # # # # # #         return jsonify({
# # # # # # # #             'success': True,
# # # # # # # #             'profile': profile,
# # # # # # # #             'recent_applications': applications[:5],
# # # # # # # #             'recommended_jobs': unique_jobs[:6],
# # # # # # # #             'stats': stats
# # # # # # # #         }), 200
        
# # # # # # # #     except Exception as e:
# # # # # # # #         print(f"❌ Error in get_dashboard: {str(e)}")
# # # # # # # #         traceback.print_exc()
# # # # # # # #         return jsonify({
# # # # # # # #             'success': False,
# # # # # # # #             'message': f'Server error: {str(e)}'
# # # # # # # #         }), 500

# # # # # # # from flask import Blueprint, request, jsonify, current_app
# # # # # # # from database.models import FreelancerProfile, Job, JobApplication, Notification, User
# # # # # # # from utils.auth_utils import token_required, freelancer_required
# # # # # # # from services.email_service import email_service
# # # # # # # from datetime import datetime
# # # # # # # import traceback

# # # # # # # freelancer_bp = Blueprint('freelancer', __name__, url_prefix='/api/freelancer')

# # # # # # # @freelancer_bp.route('/profile', methods=['GET'])
# # # # # # # @token_required
# # # # # # # @freelancer_required
# # # # # # # def get_profile():
# # # # # # #     """Get freelancer profile"""
# # # # # # #     try:
# # # # # # #         profile = FreelancerProfile.get_by_user_id(request.user_id)
        
# # # # # # #         if not profile:
# # # # # # #             return jsonify({
# # # # # # #                 'success': False,
# # # # # # #                 'message': 'Profile not found'
# # # # # # #             }), 404
        
# # # # # # #         return jsonify({
# # # # # # #             'success': True,
# # # # # # #             'profile': profile
# # # # # # #         }), 200
# # # # # # #     except Exception as e:
# # # # # # #         print(f"❌ Error in get_profile: {str(e)}")
# # # # # # #         traceback.print_exc()
# # # # # # #         return jsonify({
# # # # # # #             'success': False,
# # # # # # #             'message': f'Server error: {str(e)}'
# # # # # # #         }), 500

# # # # # # # @freelancer_bp.route('/profile', methods=['PUT'])
# # # # # # # @token_required
# # # # # # # @freelancer_required
# # # # # # # def update_profile():
# # # # # # #     """Update freelancer profile"""
# # # # # # #     try:
# # # # # # #         data = request.get_json()
        
# # # # # # #         if not data:
# # # # # # #             return jsonify({
# # # # # # #                 'success': False,
# # # # # # #                 'message': 'No data provided'
# # # # # # #             }), 400
        
# # # # # # #         profile = FreelancerProfile.update_profile(request.user_id, data)
        
# # # # # # #         if not profile:
# # # # # # #             return jsonify({
# # # # # # #                 'success': False,
# # # # # # #                 'message': 'Profile not found'
# # # # # # #             }), 404
        
# # # # # # #         return jsonify({
# # # # # # #             'success': True,
# # # # # # #             'message': 'Profile updated successfully',
# # # # # # #             'profile': profile
# # # # # # #         }), 200
# # # # # # #     except Exception as e:
# # # # # # #         print(f"❌ Error in update_profile: {str(e)}")
# # # # # # #         traceback.print_exc()
# # # # # # #         return jsonify({
# # # # # # #             'success': False,
# # # # # # #             'message': f'Server error: {str(e)}'
# # # # # # #         }), 500

# # # # # # # @freelancer_bp.route('/jobs/search', methods=['GET'])
# # # # # # # @token_required
# # # # # # # @freelancer_required
# # # # # # # def search_jobs():
# # # # # # #     """Search for jobs with improved filtering"""
# # # # # # #     try:
# # # # # # #         # Get filter parameters
# # # # # # #         search = request.args.get('search', '')
# # # # # # #         experience_level = request.args.get('experience_level', '')
# # # # # # #         min_pay = request.args.get('min_pay', '')
# # # # # # #         max_pay = request.args.get('max_pay', '')
# # # # # # #         job_type = request.args.get('job_type', '')
# # # # # # #         is_remote = request.args.get('is_remote', '')
        
# # # # # # #         # Build filters dictionary (only include non-empty values)
# # # # # # #         filters = {}
# # # # # # #         if search and search.strip():
# # # # # # #             filters['search'] = search.strip()
# # # # # # #         if experience_level and experience_level.strip():
# # # # # # #             filters['experience_level'] = experience_level.strip()
# # # # # # #         if min_pay and min_pay.strip():
# # # # # # #             try:
# # # # # # #                 filters['min_pay'] = float(min_pay)
# # # # # # #             except ValueError:
# # # # # # #                 pass
# # # # # # #         if max_pay and max_pay.strip():
# # # # # # #             try:
# # # # # # #                 filters['max_pay'] = float(max_pay)
# # # # # # #             except ValueError:
# # # # # # #                 pass
# # # # # # #         if job_type and job_type.strip() and job_type != 'All Types':
# # # # # # #             filters['job_type'] = job_type.strip()
# # # # # # #         if is_remote and is_remote.lower() == 'true':
# # # # # # #             filters['is_remote'] = True
        
# # # # # # #         print(f"🔍 Search filters: {filters}")
        
# # # # # # #         jobs = Job.search_jobs(filters)
        
# # # # # # #         print(f"✅ Found {len(jobs)} jobs")
        
# # # # # # #         return jsonify({
# # # # # # #             'success': True,
# # # # # # #             'count': len(jobs),
# # # # # # #             'jobs': jobs
# # # # # # #         }), 200
        
# # # # # # #     except Exception as e:
# # # # # # #         print(f"❌ Error in search_jobs: {str(e)}")
# # # # # # #         traceback.print_exc()
# # # # # # #         return jsonify({
# # # # # # #             'success': False,
# # # # # # #             'message': f'Search failed: {str(e)}',
# # # # # # #             'jobs': []
# # # # # # #         }), 500

# # # # # # # @freelancer_bp.route('/jobs/<int:job_id>', methods=['GET'])
# # # # # # # @token_required
# # # # # # # @freelancer_required
# # # # # # # def get_job_details(job_id):
# # # # # # #     """Get job details by ID"""
# # # # # # #     try:
# # # # # # #         print(f"🔍 Fetching job details for ID: {job_id}")
# # # # # # #         job = Job.get_by_id(job_id)
        
# # # # # # #         if not job:
# # # # # # #             return jsonify({
# # # # # # #                 'success': False,
# # # # # # #                 'message': 'Job not found'
# # # # # # #             }), 404
        
# # # # # # #         return jsonify({
# # # # # # #             'success': True,
# # # # # # #             'job': job
# # # # # # #         }), 200
# # # # # # #     except Exception as e:
# # # # # # #         print(f"❌ Error in get_job_details: {str(e)}")
# # # # # # #         traceback.print_exc()
# # # # # # #         return jsonify({
# # # # # # #             'success': False,
# # # # # # #             'message': f'Server error: {str(e)}'
# # # # # # #         }), 500

# # # # # # # @freelancer_bp.route('/jobs/<int:job_id>/apply', methods=['POST'])
# # # # # # # @token_required
# # # # # # # @freelancer_required
# # # # # # # def apply_for_job(job_id):
# # # # # # #     """Apply for a job with email notification"""
# # # # # # #     try:
# # # # # # #         data = request.get_json() or {}
        
# # # # # # #         print(f"📝 Freelancer {request.user_id} applying for job {job_id}")
        
# # # # # # #         # Validate required fields
# # # # # # #         if not data.get('cover_letter'):
# # # # # # #             return jsonify({
# # # # # # #                 'success': False,
# # # # # # #                 'message': 'Cover letter is required'
# # # # # # #             }), 400
        
# # # # # # #         # Create application
# # # # # # #         application_id = JobApplication.create(
# # # # # # #             job_id=job_id,
# # # # # # #             freelancer_id=request.user_id,
# # # # # # #             application_data=data
# # # # # # #         )
        
# # # # # # #         if not application_id:
# # # # # # #             return jsonify({
# # # # # # #                 'success': False,
# # # # # # #                 'message': 'You have already applied for this job or job not found'
# # # # # # #             }), 400
        
# # # # # # #         # Get job details for notification
# # # # # # #         job = Job.get_by_id(job_id)
# # # # # # #         freelancer = User.find_by_id(request.user_id)
# # # # # # #         recruiter = User.find_by_id(job['recruiter_id'])
        
# # # # # # #         if job and freelancer and recruiter:
# # # # # # #             freelancer_name = f"{freelancer['first_name']} {freelancer['last_name']}"
# # # # # # #             recruiter_name = f"{recruiter['first_name']} {recruiter['last_name']}"
            
# # # # # # #             # 1. Create in-app notification for recruiter
# # # # # # #             Notification.create(
# # # # # # #                 user_id=job['recruiter_id'],
# # # # # # #                 title='New Job Application',
# # # # # # #                 message=f'{freelancer_name} has applied for {job["title"]}',
# # # # # # #                 notification_type='application',
# # # # # # #                 related_application_id=application_id,
# # # # # # #                 related_job_id=job_id
# # # # # # #             )
# # # # # # #             print(f"✅ In-app notification created for recruiter {job['recruiter_id']}")
            
# # # # # # #             # 2. Send email notification to recruiter
# # # # # # #             try:
# # # # # # #                 if email_service:
# # # # # # #                     email_service.send_application_submitted_notification(
# # # # # # #                         to_email=recruiter['email'],
# # # # # # #                         recruiter_name=recruiter_name,
# # # # # # #                         freelancer_name=freelancer_name,
# # # # # # #                         job_title=job['title'],
# # # # # # #                         job_id=job_id,
# # # # # # #                         application_id=application_id
# # # # # # #                     )
# # # # # # #                     print(f"✅ Email notification sent to recruiter")
# # # # # # #             except Exception as e:
# # # # # # #                 print(f"⚠️ Failed to send email notification: {e}")
# # # # # # #                 traceback.print_exc()
        
# # # # # # #         return jsonify({
# # # # # # #             'success': True,
# # # # # # #             'message': 'Application submitted successfully! The recruiter has been notified.',
# # # # # # #             'application_id': application_id
# # # # # # #         }), 201
        
# # # # # # #     except Exception as e:
# # # # # # #         print(f"❌ Error in apply_for_job: {str(e)}")
# # # # # # #         traceback.print_exc()
# # # # # # #         return jsonify({
# # # # # # #             'success': False,
# # # # # # #             'message': f'Application failed: {str(e)}'
# # # # # # #         }), 500

# # # # # # # @freelancer_bp.route('/applications', methods=['GET'])
# # # # # # # @token_required
# # # # # # # @freelancer_required
# # # # # # # def get_applications():
# # # # # # #     """Get all applications by freelancer"""
# # # # # # #     try:
# # # # # # #         applications = JobApplication.get_by_freelancer(request.user_id)
        
# # # # # # #         return jsonify({
# # # # # # #             'success': True,
# # # # # # #             'count': len(applications),
# # # # # # #             'applications': applications
# # # # # # #         }), 200
# # # # # # #     except Exception as e:
# # # # # # #         print(f"❌ Error in get_applications: {str(e)}")
# # # # # # #         traceback.print_exc()
# # # # # # #         return jsonify({
# # # # # # #             'success': False,
# # # # # # #             'message': f'Server error: {str(e)}'
# # # # # # #         }), 500

# # # # # # # @freelancer_bp.route('/dashboard', methods=['GET'])
# # # # # # # @token_required
# # # # # # # @freelancer_required
# # # # # # # def get_dashboard():
# # # # # # #     """Get freelancer dashboard data"""
# # # # # # #     try:
# # # # # # #         profile = FreelancerProfile.get_by_user_id(request.user_id)
# # # # # # #         applications = JobApplication.get_by_freelancer(request.user_id)
        
# # # # # # #         # Get recommended jobs based on skills
# # # # # # #         recommended_jobs = []
# # # # # # #         if profile and profile.get('skills'):
# # # # # # #             skill_names = [s['name'] for s in profile['skills']]
# # # # # # #             print(f"🎯 Freelancer skills: {skill_names}")
            
# # # # # # #             if skill_names:
# # # # # # #                 # Search for jobs with matching skills
# # # # # # #                 for skill in skill_names[:3]:
# # # # # # #                     jobs = Job.search_jobs({'search': skill})
# # # # # # #                     if jobs:
# # # # # # #                         print(f"Found {len(jobs)} jobs for skill: {skill}")
# # # # # # #                         recommended_jobs.extend(jobs[:2])
        
# # # # # # #         # Remove duplicates
# # # # # # #         seen = set()
# # # # # # #         unique_jobs = []
# # # # # # #         for job in recommended_jobs:
# # # # # # #             if job['id'] not in seen:
# # # # # # #                 seen.add(job['id'])
# # # # # # #                 unique_jobs.append(job)
        
# # # # # # #         print(f"📊 Recommended {len(unique_jobs)} unique jobs")
        
# # # # # # #         # Calculate profile completion percentage
# # # # # # #         profile_completion = 0
# # # # # # #         if profile:
# # # # # # #             fields = ['bio', 'hourly_rate', 'education', 'experience', 
# # # # # # #                      'github_url', 'linkedin_url', 'portfolio_url']
# # # # # # #             completed = sum(1 for field in fields if profile.get(field))
# # # # # # #             if profile.get('skills') and len(profile['skills']) > 0:
# # # # # # #                 completed += 1
# # # # # # #             if profile.get('tech_stacks') and len(profile['tech_stacks']) > 0:
# # # # # # #                 completed += 1
# # # # # # #             total_fields = len(fields) + 2
# # # # # # #             profile_completion = int((completed / total_fields) * 100)
        
# # # # # # #         stats = {
# # # # # # #             'total_applications': len(applications),
# # # # # # #             'pending_applications': sum(1 for a in applications if a['status'] == 'applied'),
# # # # # # #             'accepted_applications': sum(1 for a in applications if a['status'] == 'accepted'),
# # # # # # #             'rejected_applications': sum(1 for a in applications if a['status'] == 'rejected'),
# # # # # # #             'profile_completion': profile_completion
# # # # # # #         }
        
# # # # # # #         return jsonify({
# # # # # # #             'success': True,
# # # # # # #             'profile': profile,
# # # # # # #             'recent_applications': applications[:5],
# # # # # # #             'recommended_jobs': unique_jobs[:6],
# # # # # # #             'stats': stats
# # # # # # #         }), 200
        
# # # # # # #     except Exception as e:
# # # # # # #         print(f"❌ Error in get_dashboard: {str(e)}")
# # # # # # #         traceback.print_exc()
# # # # # # #         return jsonify({
# # # # # # #             'success': False,
# # # # # # #             'message': f'Server error: {str(e)}'
# # # # # # #         }), 500




# # # # # # from flask import Blueprint, request, jsonify, current_app
# # # # # # from database.models import FreelancerProfile, Job, JobApplication, Notification, User
# # # # # # from utils.auth_utils import token_required, freelancer_required
# # # # # # from services.email_service import email_service
# # # # # # from datetime import datetime
# # # # # # import traceback

# # # # # # freelancer_bp = Blueprint('freelancer', __name__, url_prefix='/api/freelancer')

# # # # # # @freelancer_bp.route('/profile', methods=['GET'])
# # # # # # @token_required
# # # # # # @freelancer_required
# # # # # # def get_profile():
# # # # # #     """Get freelancer profile"""
# # # # # #     try:
# # # # # #         profile = FreelancerProfile.get_by_user_id(request.user_id)
        
# # # # # #         if not profile:
# # # # # #             return jsonify({
# # # # # #                 'success': False,
# # # # # #                 'message': 'Profile not found'
# # # # # #             }), 404
        
# # # # # #         return jsonify({
# # # # # #             'success': True,
# # # # # #             'profile': profile
# # # # # #         }), 200
# # # # # #     except Exception as e:
# # # # # #         print(f"❌ Error in get_profile: {str(e)}")
# # # # # #         traceback.print_exc()
# # # # # #         return jsonify({
# # # # # #             'success': False,
# # # # # #             'message': f'Server error: {str(e)}'
# # # # # #         }), 500

# # # # # # @freelancer_bp.route('/profile', methods=['PUT'])
# # # # # # @token_required
# # # # # # @freelancer_required
# # # # # # def update_profile():
# # # # # #     """Update freelancer profile"""
# # # # # #     try:
# # # # # #         data = request.get_json()
        
# # # # # #         if not data:
# # # # # #             return jsonify({
# # # # # #                 'success': False,
# # # # # #                 'message': 'No data provided'
# # # # # #             }), 400
        
# # # # # #         profile = FreelancerProfile.update_profile(request.user_id, data)
        
# # # # # #         if not profile:
# # # # # #             return jsonify({
# # # # # #                 'success': False,
# # # # # #                 'message': 'Profile not found'
# # # # # #             }), 404
        
# # # # # #         return jsonify({
# # # # # #             'success': True,
# # # # # #             'message': 'Profile updated successfully',
# # # # # #             'profile': profile
# # # # # #         }), 200
# # # # # #     except Exception as e:
# # # # # #         print(f"❌ Error in update_profile: {str(e)}")
# # # # # #         traceback.print_exc()
# # # # # #         return jsonify({
# # # # # #             'success': False,
# # # # # #             'message': f'Server error: {str(e)}'
# # # # # #         }), 500

# # # # # # @freelancer_bp.route('/jobs/search', methods=['GET'])
# # # # # # @token_required
# # # # # # @freelancer_required
# # # # # # def search_jobs():
# # # # # #     """Search for jobs with improved filtering"""
# # # # # #     try:
# # # # # #         # Get filter parameters
# # # # # #         search = request.args.get('search', '')
# # # # # #         experience_level = request.args.get('experience_level', '')
# # # # # #         min_pay = request.args.get('min_pay', '')
# # # # # #         max_pay = request.args.get('max_pay', '')
# # # # # #         job_type = request.args.get('job_type', '')
# # # # # #         is_remote = request.args.get('is_remote', '')
        
# # # # # #         # Build filters dictionary (only include non-empty values)
# # # # # #         filters = {}
# # # # # #         if search and search.strip():
# # # # # #             filters['search'] = search.strip()
# # # # # #         if experience_level and experience_level.strip():
# # # # # #             filters['experience_level'] = experience_level.strip()
# # # # # #         if min_pay and min_pay.strip():
# # # # # #             try:
# # # # # #                 filters['min_pay'] = float(min_pay)
# # # # # #             except ValueError:
# # # # # #                 pass
# # # # # #         if max_pay and max_pay.strip():
# # # # # #             try:
# # # # # #                 filters['max_pay'] = float(max_pay)
# # # # # #             except ValueError:
# # # # # #                 pass
# # # # # #         if job_type and job_type.strip() and job_type != 'All Types':
# # # # # #             filters['job_type'] = job_type.strip()
# # # # # #         if is_remote and is_remote.lower() == 'true':
# # # # # #             filters['is_remote'] = True
        
# # # # # #         print(f"🔍 Search filters: {filters}")
        
# # # # # #         jobs = Job.search_jobs(filters)
        
# # # # # #         print(f"✅ Found {len(jobs)} jobs")
        
# # # # # #         return jsonify({
# # # # # #             'success': True,
# # # # # #             'count': len(jobs),
# # # # # #             'jobs': jobs
# # # # # #         }), 200
        
# # # # # #     except Exception as e:
# # # # # #         print(f"❌ Error in search_jobs: {str(e)}")
# # # # # #         traceback.print_exc()
# # # # # #         return jsonify({
# # # # # #             'success': False,
# # # # # #             'message': f'Search failed: {str(e)}',
# # # # # #             'jobs': []
# # # # # #         }), 500

# # # # # # @freelancer_bp.route('/jobs/<int:job_id>', methods=['GET'])
# # # # # # @token_required
# # # # # # @freelancer_required
# # # # # # def get_job_details(job_id):
# # # # # #     """Get job details by ID"""
# # # # # #     try:
# # # # # #         print(f"🔍 Fetching job details for ID: {job_id}")
# # # # # #         job = Job.get_by_id(job_id)
        
# # # # # #         if not job:
# # # # # #             return jsonify({
# # # # # #                 'success': False,
# # # # # #                 'message': 'Job not found'
# # # # # #             }), 404
        
# # # # # #         return jsonify({
# # # # # #             'success': True,
# # # # # #             'job': job
# # # # # #         }), 200
# # # # # #     except Exception as e:
# # # # # #         print(f"❌ Error in get_job_details: {str(e)}")
# # # # # #         traceback.print_exc()
# # # # # #         return jsonify({
# # # # # #             'success': False,
# # # # # #             'message': f'Server error: {str(e)}'
# # # # # #         }), 500

# # # # # # @freelancer_bp.route('/jobs/<int:job_id>/apply', methods=['POST'])
# # # # # # @token_required
# # # # # # @freelancer_required
# # # # # # def apply_for_job(job_id):
# # # # # #     """Apply for a job with email notification"""
# # # # # #     try:
# # # # # #         data = request.get_json() or {}
        
# # # # # #         print(f"📝 Freelancer {request.user_id} applying for job {job_id}")
# # # # # #         print(f"📦 Application data: {data}")
        
# # # # # #         # Validate required fields
# # # # # #         if not data.get('cover_letter'):
# # # # # #             return jsonify({
# # # # # #                 'success': False,
# # # # # #                 'message': 'Cover letter is required'
# # # # # #             }), 400
        
# # # # # #         # First check if job exists
# # # # # #         job = Job.get_by_id(job_id)
# # # # # #         if not job:
# # # # # #             print(f"❌ Job {job_id} not found")
# # # # # #             return jsonify({
# # # # # #                 'success': False,
# # # # # #                 'message': 'Job not found'
# # # # # #             }), 404
            
# # # # # #         print(f"✅ Job found: {job['title']}")
        
# # # # # #         # Create application
# # # # # #         application_id = JobApplication.create(
# # # # # #             job_id=job_id,
# # # # # #             freelancer_id=request.user_id,
# # # # # #             application_data=data
# # # # # #         )
        
# # # # # #         if not application_id:
# # # # # #             # Check if it's because of duplicate application
# # # # # #             connection = get_db_connection()
# # # # # #             cursor = connection.cursor()
# # # # # #             cursor.execute("""
# # # # # #                 SELECT id, status FROM job_applications 
# # # # # #                 WHERE job_id = %s AND freelancer_id = %s
# # # # # #             """, (job_id, request.user_id))
# # # # # #             existing = cursor.fetchone()
# # # # # #             cursor.close()
# # # # # #             connection.close()
            
# # # # # #             if existing:
# # # # # #                 return jsonify({
# # # # # #                     'success': False,
# # # # # #                     'message': f'You have already applied for this job (Status: {existing["status"]})'
# # # # # #                 }), 400
# # # # # #             else:
# # # # # #                 return jsonify({
# # # # # #                     'success': False,
# # # # # #                     'message': 'Failed to create application. Please try again.'
# # # # # #                 }), 400
        
# # # # # #         # Get freelancer and recruiter info for notifications
# # # # # #         freelancer = User.find_by_id(request.user_id)
# # # # # #         recruiter = User.find_by_id(job['recruiter_id'])
        
# # # # # #         if freelancer and recruiter:
# # # # # #             freelancer_name = f"{freelancer['first_name']} {freelancer['last_name']}"
# # # # # #             recruiter_name = f"{recruiter['first_name']} {recruiter['last_name']}"
            
# # # # # #             # Create in-app notification for recruiter
# # # # # #             Notification.create(
# # # # # #                 user_id=job['recruiter_id'],
# # # # # #                 title='New Job Application',
# # # # # #                 message=f'{freelancer_name} has applied for {job["title"]}',
# # # # # #                 notification_type='application',
# # # # # #                 related_application_id=application_id,
# # # # # #                 related_job_id=job_id
# # # # # #             )
# # # # # #             print(f"✅ In-app notification created for recruiter {job['recruiter_id']}")
            
# # # # # #             # Send email notification to recruiter
# # # # # #             try:
# # # # # #                 if email_service:
# # # # # #                     email_service.send_application_submitted_notification(
# # # # # #                         to_email=recruiter['email'],
# # # # # #                         recruiter_name=recruiter_name,
# # # # # #                         freelancer_name=freelancer_name,
# # # # # #                         job_title=job['title'],
# # # # # #                         job_id=job_id,
# # # # # #                         application_id=application_id
# # # # # #                     )
# # # # # #                     print(f"✅ Email notification sent to recruiter")
# # # # # #             except Exception as e:
# # # # # #                 print(f"⚠️ Failed to send email notification: {e}")
# # # # # #                 traceback.print_exc()
        
# # # # # #         return jsonify({
# # # # # #             'success': True,
# # # # # #             'message': 'Application submitted successfully! The recruiter has been notified.',
# # # # # #             'application_id': application_id
# # # # # #         }), 201
        
# # # # # #     except Exception as e:
# # # # # #         print(f"❌ Error in apply_for_job: {str(e)}")
# # # # # #         traceback.print_exc()
# # # # # #         return jsonify({
# # # # # #             'success': False,
# # # # # #             'message': f'Application failed: {str(e)}'
# # # # # #         }), 500

# # # # # # @freelancer_bp.route('/applications', methods=['GET'])
# # # # # # @token_required
# # # # # # @freelancer_required
# # # # # # def get_applications():
# # # # # #     """Get all applications by freelancer"""
# # # # # #     try:
# # # # # #         applications = JobApplication.get_by_freelancer(request.user_id)
        
# # # # # #         return jsonify({
# # # # # #             'success': True,
# # # # # #             'count': len(applications),
# # # # # #             'applications': applications
# # # # # #         }), 200
# # # # # #     except Exception as e:
# # # # # #         print(f"❌ Error in get_applications: {str(e)}")
# # # # # #         traceback.print_exc()
# # # # # #         return jsonify({
# # # # # #             'success': False,
# # # # # #             'message': f'Server error: {str(e)}'
# # # # # #         }), 500

# # # # # # @freelancer_bp.route('/dashboard', methods=['GET'])
# # # # # # @token_required
# # # # # # @freelancer_required
# # # # # # def get_dashboard():
# # # # # #     """Get freelancer dashboard data"""
# # # # # #     try:
# # # # # #         profile = FreelancerProfile.get_by_user_id(request.user_id)
# # # # # #         applications = JobApplication.get_by_freelancer(request.user_id)
        
# # # # # #         # Get recommended jobs based on skills
# # # # # #         recommended_jobs = []
# # # # # #         if profile and profile.get('skills'):
# # # # # #             skill_names = [s['name'] for s in profile['skills']]
# # # # # #             print(f"🎯 Freelancer skills: {skill_names}")
            
# # # # # #             if skill_names:
# # # # # #                 # Search for jobs with matching skills
# # # # # #                 for skill in skill_names[:3]:
# # # # # #                     jobs = Job.search_jobs({'search': skill})
# # # # # #                     if jobs:
# # # # # #                         print(f"Found {len(jobs)} jobs for skill: {skill}")
# # # # # #                         recommended_jobs.extend(jobs[:2])
        
# # # # # #         # Remove duplicates
# # # # # #         seen = set()
# # # # # #         unique_jobs = []
# # # # # #         for job in recommended_jobs:
# # # # # #             if job['id'] not in seen:
# # # # # #                 seen.add(job['id'])
# # # # # #                 unique_jobs.append(job)
        
# # # # # #         print(f"📊 Recommended {len(unique_jobs)} unique jobs")
        
# # # # # #         # Calculate profile completion percentage
# # # # # #         profile_completion = 0
# # # # # #         if profile:
# # # # # #             fields = ['bio', 'hourly_rate', 'education', 'experience', 
# # # # # #                      'github_url', 'linkedin_url', 'portfolio_url']
# # # # # #             completed = sum(1 for field in fields if profile.get(field))
# # # # # #             if profile.get('skills') and len(profile['skills']) > 0:
# # # # # #                 completed += 1
# # # # # #             if profile.get('tech_stacks') and len(profile['tech_stacks']) > 0:
# # # # # #                 completed += 1
# # # # # #             total_fields = len(fields) + 2
# # # # # #             profile_completion = int((completed / total_fields) * 100)
        
# # # # # #         stats = {
# # # # # #             'total_applications': len(applications),
# # # # # #             'pending_applications': sum(1 for a in applications if a['status'] == 'applied'),
# # # # # #             'accepted_applications': sum(1 for a in applications if a['status'] == 'accepted'),
# # # # # #             'rejected_applications': sum(1 for a in applications if a['status'] == 'rejected'),
# # # # # #             'profile_completion': profile_completion
# # # # # #         }
        
# # # # # #         return jsonify({
# # # # # #             'success': True,
# # # # # #             'profile': profile,
# # # # # #             'recent_applications': applications[:5],
# # # # # #             'recommended_jobs': unique_jobs[:6],
# # # # # #             'stats': stats
# # # # # #         }), 200
        
# # # # # #     except Exception as e:
# # # # # #         print(f"❌ Error in get_dashboard: {str(e)}")
# # # # # #         traceback.print_exc()
# # # # # #         return jsonify({
# # # # # #             'success': False,
# # # # # #             'message': f'Server error: {str(e)}'
# # # # # #         }), 500
# # # # # from flask import Blueprint, request, jsonify, current_app
# # # # # from database.models import FreelancerProfile, Job, JobApplication, Notification, User
# # # # # from utils.auth_utils import token_required, freelancer_required
# # # # # from services.email_service import email_service
# # # # # from datetime import datetime
# # # # # import traceback

# # # # # freelancer_bp = Blueprint('freelancer', __name__, url_prefix='/api/freelancer')

# # # # # @freelancer_bp.route('/profile', methods=['GET'])
# # # # # @token_required
# # # # # @freelancer_required
# # # # # def get_profile():
# # # # #     """Get freelancer profile"""
# # # # #     try:
# # # # #         profile = FreelancerProfile.get_by_user_id(request.user_id)
        
# # # # #         if not profile:
# # # # #             return jsonify({
# # # # #                 'success': False,
# # # # #                 'message': 'Profile not found'
# # # # #             }), 404
        
# # # # #         return jsonify({
# # # # #             'success': True,
# # # # #             'profile': profile
# # # # #         }), 200
# # # # #     except Exception as e:
# # # # #         print(f"❌ Error in get_profile: {str(e)}")
# # # # #         traceback.print_exc()
# # # # #         return jsonify({
# # # # #             'success': False,
# # # # #             'message': f'Server error: {str(e)}'
# # # # #         }), 500

# # # # # @freelancer_bp.route('/profile', methods=['PUT'])
# # # # # @token_required
# # # # # @freelancer_required
# # # # # def update_profile():
# # # # #     """Update freelancer profile"""
# # # # #     try:
# # # # #         data = request.get_json()
        
# # # # #         if not data:
# # # # #             return jsonify({
# # # # #                 'success': False,
# # # # #                 'message': 'No data provided'
# # # # #             }), 400
        
# # # # #         profile = FreelancerProfile.update_profile(request.user_id, data)
        
# # # # #         if not profile:
# # # # #             return jsonify({
# # # # #                 'success': False,
# # # # #                 'message': 'Profile not found'
# # # # #             }), 404
        
# # # # #         return jsonify({
# # # # #             'success': True,
# # # # #             'message': 'Profile updated successfully',
# # # # #             'profile': profile
# # # # #         }), 200
# # # # #     except Exception as e:
# # # # #         print(f"❌ Error in update_profile: {str(e)}")
# # # # #         traceback.print_exc()
# # # # #         return jsonify({
# # # # #             'success': False,
# # # # #             'message': f'Server error: {str(e)}'
# # # # #         }), 500

# # # # # @freelancer_bp.route('/jobs/search', methods=['GET'])
# # # # # @token_required
# # # # # @freelancer_required
# # # # # def search_jobs():
# # # # #     """Search for jobs with improved filtering"""
# # # # #     try:
# # # # #         # Get filter parameters
# # # # #         search = request.args.get('search', '')
# # # # #         experience_level = request.args.get('experience_level', '')
# # # # #         min_pay = request.args.get('min_pay', '')
# # # # #         max_pay = request.args.get('max_pay', '')
# # # # #         job_type = request.args.get('job_type', '')
# # # # #         is_remote = request.args.get('is_remote', '')
        
# # # # #         # Build filters dictionary (only include non-empty values)
# # # # #         filters = {}
# # # # #         if search and search.strip():
# # # # #             filters['search'] = search.strip()
# # # # #         if experience_level and experience_level.strip():
# # # # #             filters['experience_level'] = experience_level.strip()
# # # # #         if min_pay and min_pay.strip():
# # # # #             try:
# # # # #                 filters['min_pay'] = float(min_pay)
# # # # #             except ValueError:
# # # # #                 pass
# # # # #         if max_pay and max_pay.strip():
# # # # #             try:
# # # # #                 filters['max_pay'] = float(max_pay)
# # # # #             except ValueError:
# # # # #                 pass
# # # # #         if job_type and job_type.strip() and job_type != 'All Types':
# # # # #             filters['job_type'] = job_type.strip()
# # # # #         if is_remote and is_remote.lower() == 'true':
# # # # #             filters['is_remote'] = True
        
# # # # #         print(f"🔍 Search filters: {filters}")
        
# # # # #         jobs = Job.search_jobs(filters)
        
# # # # #         print(f"✅ Found {len(jobs)} jobs")
        
# # # # #         return jsonify({
# # # # #             'success': True,
# # # # #             'count': len(jobs),
# # # # #             'jobs': jobs
# # # # #         }), 200
        
# # # # #     except Exception as e:
# # # # #         print(f"❌ Error in search_jobs: {str(e)}")
# # # # #         traceback.print_exc()
# # # # #         return jsonify({
# # # # #             'success': False,
# # # # #             'message': f'Search failed: {str(e)}',
# # # # #             'jobs': []
# # # # #         }), 500

# # # # # @freelancer_bp.route('/jobs/<int:job_id>', methods=['GET'])
# # # # # @token_required
# # # # # @freelancer_required
# # # # # def get_job_details(job_id):
# # # # #     """Get job details by ID"""
# # # # #     try:
# # # # #         print(f"🔍 Fetching job details for ID: {job_id}")
# # # # #         job = Job.get_by_id(job_id)
        
# # # # #         if not job:
# # # # #             return jsonify({
# # # # #                 'success': False,
# # # # #                 'message': 'Job not found'
# # # # #             }), 404
        
# # # # #         return jsonify({
# # # # #             'success': True,
# # # # #             'job': job
# # # # #         }), 200
# # # # #     except Exception as e:
# # # # #         print(f"❌ Error in get_job_details: {str(e)}")
# # # # #         traceback.print_exc()
# # # # #         return jsonify({
# # # # #             'success': False,
# # # # #             'message': f'Server error: {str(e)}'
# # # # #         }), 500

# # # # # @freelancer_bp.route('/jobs/<int:job_id>/apply', methods=['POST'])
# # # # # @token_required
# # # # # @freelancer_required
# # # # # def apply_for_job(job_id):
# # # # #     """Apply for a job with email notification"""
# # # # #     try:
# # # # #         data = request.get_json() or {}
        
# # # # #         print(f"📝 Freelancer {request.user_id} applying for job {job_id}")
# # # # #         print(f"📦 Application data: {data}")
        
# # # # #         # Validate required fields
# # # # #         if not data.get('cover_letter'):
# # # # #             return jsonify({
# # # # #                 'success': False,
# # # # #                 'message': 'Cover letter is required'
# # # # #             }), 400
        
# # # # #         # First check if job exists
# # # # #         job = Job.get_by_id(job_id)
# # # # #         if not job:
# # # # #             print(f"❌ Job {job_id} not found")
# # # # #             return jsonify({
# # # # #                 'success': False,
# # # # #                 'message': 'Job not found'
# # # # #             }), 404
            
# # # # #         print(f"✅ Job found: {job['title']}")
        
# # # # #         # Check if freelancer profile exists
# # # # #         profile = FreelancerProfile.get_by_user_id(request.user_id)
# # # # #         if not profile:
# # # # #             print(f"⚠️ Freelancer profile not found for user {request.user_id}, will be created automatically")
        
# # # # #         # Create application
# # # # #         application_id = JobApplication.create(
# # # # #             job_id=job_id,
# # # # #             freelancer_id=request.user_id,
# # # # #             application_data=data
# # # # #         )
        
# # # # #         if not application_id:
# # # # #             # Check if it's because of duplicate application
# # # # #             connection = get_db_connection()
# # # # #             cursor = connection.cursor()
# # # # #             cursor.execute("""
# # # # #                 SELECT id, status FROM job_applications 
# # # # #                 WHERE job_id = %s AND freelancer_id = %s
# # # # #             """, (job_id, request.user_id))
# # # # #             existing = cursor.fetchone()
# # # # #             cursor.close()
# # # # #             connection.close()
            
# # # # #             if existing:
# # # # #                 return jsonify({
# # # # #                     'success': False,
# # # # #                     'message': f'You have already applied for this job (Status: {existing["status"]})'
# # # # #                 }), 400
# # # # #             else:
# # # # #                 return jsonify({
# # # # #                     'success': False,
# # # # #                     'message': 'Failed to create application. Please try again.'
# # # # #                 }), 400
        
# # # # #         # Get freelancer and recruiter info for notifications
# # # # #         freelancer = User.find_by_id(request.user_id)
# # # # #         recruiter = User.find_by_id(job['recruiter_id'])
        
# # # # #         if freelancer and recruiter:
# # # # #             freelancer_name = f"{freelancer['first_name']} {freelancer['last_name']}"
# # # # #             recruiter_name = f"{recruiter['first_name']} {recruiter['last_name']}"
            
# # # # #             # 1. Create in-app notification for recruiter
# # # # #             Notification.create(
# # # # #                 user_id=job['recruiter_id'],
# # # # #                 title='New Job Application',
# # # # #                 message=f'{freelancer_name} has applied for {job["title"]}',
# # # # #                 notification_type='application',
# # # # #                 related_application_id=application_id,
# # # # #                 related_job_id=job_id
# # # # #             )
# # # # #             print(f"✅ In-app notification created for recruiter {job['recruiter_id']}")
            
# # # # #             # 2. Send email notification to recruiter
# # # # #             try:
# # # # #                 if email_service:
# # # # #                     email_service.send_application_submitted_notification(
# # # # #                         to_email=recruiter['email'],
# # # # #                         recruiter_name=recruiter_name,
# # # # #                         freelancer_name=freelancer_name,
# # # # #                         job_title=job['title'],
# # # # #                         job_id=job_id,
# # # # #                         application_id=application_id
# # # # #                     )
# # # # #                     print(f"✅ Email notification sent to recruiter")
# # # # #             except Exception as e:
# # # # #                 print(f"⚠️ Failed to send email notification: {e}")
# # # # #                 traceback.print_exc()
            
# # # # #             # 3. Send confirmation email to freelancer
# # # # #             try:
# # # # #                 if email_service:
# # # # #                     email_service.send_application_confirmation(
# # # # #                         to_email=freelancer['email'],
# # # # #                         freelancer_name=freelancer_name,
# # # # #                         job_title=job['title'],
# # # # #                         company_name=job.get('company_name', 'Company')
# # # # #                     )
# # # # #                     print(f"✅ Confirmation email sent to freelancer")
# # # # #             except Exception as e:
# # # # #                 print(f"⚠️ Failed to send confirmation email: {e}")
# # # # #                 traceback.print_exc()
        
# # # # #         return jsonify({
# # # # #             'success': True,
# # # # #             'message': 'Application submitted successfully! The recruiter has been notified.',
# # # # #             'application_id': application_id
# # # # #         }), 201
        
# # # # #     except Exception as e:
# # # # #         print(f"❌ Error in apply_for_job: {str(e)}")
# # # # #         traceback.print_exc()
# # # # #         return jsonify({
# # # # #             'success': False,
# # # # #             'message': f'Application failed: {str(e)}'
# # # # #         }), 500

# # # # # @freelancer_bp.route('/applications', methods=['GET'])
# # # # # @token_required
# # # # # @freelancer_required
# # # # # def get_applications():
# # # # #     """Get all applications by freelancer"""
# # # # #     try:
# # # # #         applications = JobApplication.get_by_freelancer(request.user_id)
        
# # # # #         return jsonify({
# # # # #             'success': True,
# # # # #             'count': len(applications),
# # # # #             'applications': applications
# # # # #         }), 200
# # # # #     except Exception as e:
# # # # #         print(f"❌ Error in get_applications: {str(e)}")
# # # # #         traceback.print_exc()
# # # # #         return jsonify({
# # # # #             'success': False,
# # # # #             'message': f'Server error: {str(e)}'
# # # # #         }), 500

# # # # # @freelancer_bp.route('/dashboard', methods=['GET'])
# # # # # @token_required
# # # # # @freelancer_required
# # # # # def get_dashboard():
# # # # #     """Get freelancer dashboard data"""
# # # # #     try:
# # # # #         profile = FreelancerProfile.get_by_user_id(request.user_id)
# # # # #         applications = JobApplication.get_by_freelancer(request.user_id)
        
# # # # #         # Get recommended jobs based on skills
# # # # #         recommended_jobs = []
# # # # #         if profile and profile.get('skills'):
# # # # #             skill_names = [s['name'] for s in profile['skills']]
# # # # #             print(f"🎯 Freelancer skills: {skill_names}")
            
# # # # #             if skill_names:
# # # # #                 # Search for jobs with matching skills
# # # # #                 for skill in skill_names[:3]:
# # # # #                     jobs = Job.search_jobs({'search': skill})
# # # # #                     if jobs:
# # # # #                         print(f"Found {len(jobs)} jobs for skill: {skill}")
# # # # #                         recommended_jobs.extend(jobs[:2])
        
# # # # #         # Remove duplicates
# # # # #         seen = set()
# # # # #         unique_jobs = []
# # # # #         for job in recommended_jobs:
# # # # #             if job['id'] not in seen:
# # # # #                 seen.add(job['id'])
# # # # #                 unique_jobs.append(job)
        
# # # # #         print(f"📊 Recommended {len(unique_jobs)} unique jobs")
        
# # # # #         # Calculate profile completion percentage
# # # # #         profile_completion = 0
# # # # #         if profile:
# # # # #             fields = ['bio', 'hourly_rate', 'education', 'experience', 
# # # # #                      'github_url', 'linkedin_url', 'portfolio_url']
# # # # #             completed = sum(1 for field in fields if profile.get(field))
# # # # #             if profile.get('skills') and len(profile['skills']) > 0:
# # # # #                 completed += 1
# # # # #             if profile.get('tech_stacks') and len(profile['tech_stacks']) > 0:
# # # # #                 completed += 1
# # # # #             total_fields = len(fields) + 2
# # # # #             profile_completion = int((completed / total_fields) * 100)
        
# # # # #         stats = {
# # # # #             'total_applications': len(applications),
# # # # #             'pending_applications': sum(1 for a in applications if a['status'] == 'applied'),
# # # # #             'accepted_applications': sum(1 for a in applications if a['status'] == 'accepted'),
# # # # #             'rejected_applications': sum(1 for a in applications if a['status'] == 'rejected'),
# # # # #             'profile_completion': profile_completion
# # # # #         }
        
# # # # #         return jsonify({
# # # # #             'success': True,
# # # # #             'profile': profile,
# # # # #             'recent_applications': applications[:5],
# # # # #             'recommended_jobs': unique_jobs[:6],
# # # # #             'stats': stats
# # # # #         }), 200
        
# # # # #     except Exception as e:
# # # # #         print(f"❌ Error in get_dashboard: {str(e)}")
# # # # #         traceback.print_exc()
# # # # #         return jsonify({
# # # # #             'success': False,
# # # # #             'message': f'Server error: {str(e)}'
# # # # #         }), 500

        

# # # # from flask import Blueprint, request, jsonify, current_app
# # # # from database.models import FreelancerProfile, Job, JobApplication, Notification, User
# # # # from utils.auth_utils import token_required, freelancer_required
# # # # from services.email_service import email_service
# # # # from datetime import datetime
# # # # import traceback

# # # # freelancer_bp = Blueprint('freelancer', __name__, url_prefix='/api/freelancer')

# # # # @freelancer_bp.route('/profile', methods=['GET'])
# # # # @token_required
# # # # @freelancer_required
# # # # def get_profile():
# # # #     """Get freelancer profile"""
# # # #     try:
# # # #         profile = FreelancerProfile.get_by_user_id(request.user_id)
        
# # # #         if not profile:
# # # #             return jsonify({
# # # #                 'success': False,
# # # #                 'message': 'Profile not found'
# # # #             }), 404
        
# # # #         return jsonify({
# # # #             'success': True,
# # # #             'profile': profile
# # # #         }), 200
# # # #     except Exception as e:
# # # #         print(f"❌ Error in get_profile: {str(e)}")
# # # #         traceback.print_exc()
# # # #         return jsonify({
# # # #             'success': False,
# # # #             'message': f'Server error: {str(e)}'
# # # #         }), 500

# # # # @freelancer_bp.route('/profile', methods=['PUT'])
# # # # @token_required
# # # # @freelancer_required
# # # # def update_profile():
# # # #     """Update freelancer profile"""
# # # #     try:
# # # #         data = request.get_json()
        
# # # #         if not data:
# # # #             return jsonify({
# # # #                 'success': False,
# # # #                 'message': 'No data provided'
# # # #             }), 400
        
# # # #         profile = FreelancerProfile.update_profile(request.user_id, data)
        
# # # #         if not profile:
# # # #             return jsonify({
# # # #                 'success': False,
# # # #                 'message': 'Profile not found'
# # # #             }), 404
        
# # # #         return jsonify({
# # # #             'success': True,
# # # #             'message': 'Profile updated successfully',
# # # #             'profile': profile
# # # #         }), 200
# # # #     except Exception as e:
# # # #         print(f"❌ Error in update_profile: {str(e)}")
# # # #         traceback.print_exc()
# # # #         return jsonify({
# # # #             'success': False,
# # # #             'message': f'Server error: {str(e)}'
# # # #         }), 500

# # # # @freelancer_bp.route('/jobs/search', methods=['GET'])
# # # # @token_required
# # # # @freelancer_required
# # # # def search_jobs():
# # # #     """Search for jobs with improved filtering"""
# # # #     try:
# # # #         # Get filter parameters
# # # #         search = request.args.get('search', '')
# # # #         experience_level = request.args.get('experience_level', '')
# # # #         min_pay = request.args.get('min_pay', '')
# # # #         max_pay = request.args.get('max_pay', '')
# # # #         job_type = request.args.get('job_type', '')
# # # #         is_remote = request.args.get('is_remote', '')
        
# # # #         # Build filters dictionary (only include non-empty values)
# # # #         filters = {}
# # # #         if search and search.strip():
# # # #             filters['search'] = search.strip()
# # # #         if experience_level and experience_level.strip():
# # # #             filters['experience_level'] = experience_level.strip()
# # # #         if min_pay and min_pay.strip():
# # # #             try:
# # # #                 filters['min_pay'] = float(min_pay)
# # # #             except ValueError:
# # # #                 pass
# # # #         if max_pay and max_pay.strip():
# # # #             try:
# # # #                 filters['max_pay'] = float(max_pay)
# # # #             except ValueError:
# # # #                 pass
# # # #         if job_type and job_type.strip() and job_type != 'All Types':
# # # #             filters['job_type'] = job_type.strip()
# # # #         if is_remote and is_remote.lower() == 'true':
# # # #             filters['is_remote'] = True
        
# # # #         print(f"🔍 Search filters: {filters}")
        
# # # #         jobs = Job.search_jobs(filters)
        
# # # #         print(f"✅ Found {len(jobs)} jobs")
        
# # # #         return jsonify({
# # # #             'success': True,
# # # #             'count': len(jobs),
# # # #             'jobs': jobs
# # # #         }), 200
        
# # # #     except Exception as e:
# # # #         print(f"❌ Error in search_jobs: {str(e)}")
# # # #         traceback.print_exc()
# # # #         return jsonify({
# # # #             'success': False,
# # # #             'message': f'Search failed: {str(e)}',
# # # #             'jobs': []
# # # #         }), 500

# # # # @freelancer_bp.route('/jobs/<int:job_id>', methods=['GET'])
# # # # @token_required
# # # # @freelancer_required
# # # # def get_job_details(job_id):
# # # #     """Get job details by ID"""
# # # #     try:
# # # #         print(f"🔍 Fetching job details for ID: {job_id}")
# # # #         job = Job.get_by_id(job_id)
        
# # # #         if not job:
# # # #             return jsonify({
# # # #                 'success': False,
# # # #                 'message': 'Job not found'
# # # #             }), 404
        
# # # #         return jsonify({
# # # #             'success': True,
# # # #             'job': job
# # # #         }), 200
# # # #     except Exception as e:
# # # #         print(f"❌ Error in get_job_details: {str(e)}")
# # # #         traceback.print_exc()
# # # #         return jsonify({
# # # #             'success': False,
# # # #             'message': f'Server error: {str(e)}'
# # # #         }), 500

# # # # @freelancer_bp.route('/jobs/<int:job_id>/apply', methods=['POST'])
# # # # @token_required
# # # # @freelancer_required
# # # # def apply_for_job(job_id):
# # # #     """Apply for a job with email notification"""
# # # #     try:
# # # #         data = request.get_json() or {}
        
# # # #         print(f"📝 Freelancer {request.user_id} applying for job {job_id}")
# # # #         print(f"📦 Application data: {data}")
        
# # # #         # Validate required fields
# # # #         if not data.get('cover_letter'):
# # # #             return jsonify({
# # # #                 'success': False,
# # # #                 'message': 'Cover letter is required'
# # # #             }), 400
        
# # # #         # First check if job exists
# # # #         job = Job.get_by_id(job_id)
# # # #         if not job:
# # # #             print(f"❌ Job {job_id} not found")
# # # #             return jsonify({
# # # #                 'success': False,
# # # #                 'message': 'Job not found'
# # # #             }), 404
            
# # # #         print(f"✅ Job found: {job['title']}")
# # # #         print(f"📧 Job details - Recruiter ID: {job['recruiter_id']}, Recruiter Email: {job.get('recruiter_email', 'N/A')}")
        
# # # #         # Create application
# # # #         application_id = JobApplication.create(
# # # #             job_id=job_id,
# # # #             freelancer_id=request.user_id,
# # # #             application_data=data
# # # #         )
        
# # # #         if not application_id:
# # # #             # Check if it's because of duplicate application
# # # #             connection = get_db_connection()
# # # #             cursor = connection.cursor()
# # # #             cursor.execute("""
# # # #                 SELECT id, status FROM job_applications 
# # # #                 WHERE job_id = %s AND freelancer_id = %s
# # # #             """, (job_id, request.user_id))
# # # #             existing = cursor.fetchone()
# # # #             cursor.close()
# # # #             connection.close()
            
# # # #             if existing:
# # # #                 return jsonify({
# # # #                     'success': False,
# # # #                     'message': f'You have already applied for this job (Status: {existing["status"]})'
# # # #                 }), 400
# # # #             else:
# # # #                 return jsonify({
# # # #                     'success': False,
# # # #                     'message': 'Failed to create application. Please try again.'
# # # #                 }), 400
        
# # # #         print(f"✅ Application created with ID: {application_id}")
        
# # # #         # Get freelancer and recruiter info for notifications
# # # #         freelancer = User.find_by_id(request.user_id)
# # # #         recruiter = User.find_by_id(job['recruiter_id'])
        
# # # #         print(f"👤 Freelancer: {freelancer['email'] if freelancer else 'Not found'}")
# # # #         print(f"👤 Recruiter: {recruiter['email'] if recruiter else 'Not found'}")
        
# # # #         if freelancer and recruiter:
# # # #             freelancer_name = f"{freelancer['first_name']} {freelancer['last_name']}"
# # # #             recruiter_name = f"{recruiter['first_name']} {recruiter['last_name']}"
            
# # # #             # 1. Create in-app notification for recruiter
# # # #             Notification.create(
# # # #                 user_id=job['recruiter_id'],
# # # #                 title='New Job Application',
# # # #                 message=f'{freelancer_name} has applied for {job["title"]}',
# # # #                 notification_type='application',
# # # #                 related_application_id=application_id,
# # # #                 related_job_id=job_id
# # # #             )
# # # #             print(f"✅ In-app notification created for recruiter {job['recruiter_id']}")
            
# # # #             # 2. Send email notification to recruiter
# # # #             try:
# # # #                 if email_service:
# # # #                     print(f"📧 Email service exists, preparing to send to recruiter: {recruiter['email']}")
# # # #                     company_name = job.get('company_name', 'Company')
# # # #                     result = email_service.send_application_submitted_notification(
# # # #                         to_email=recruiter['email'],
# # # #                         recruiter_name=recruiter_name,
# # # #                         freelancer_name=freelancer_name,
# # # #                         job_title=job['title'],
# # # #                         job_id=job_id,
# # # #                         application_id=application_id,
# # # #                         user_id=recruiter['id']
# # # #                     )
# # # #                     print(f"📧 Email send result to recruiter: {result}")
# # # #                 else:
# # # #                     print(f"❌ Email service is None!")
# # # #             except Exception as e:
# # # #                 print(f"⚠️ Failed to send email notification to recruiter: {e}")
# # # #                 traceback.print_exc()
            
# # # #             # 3. Send confirmation email to freelancer
# # # #             try:
# # # #                 if email_service:
# # # #                     print(f"📧 Preparing to send confirmation to freelancer: {freelancer['email']}")
# # # #                     company_name = job.get('company_name', 'Company')
# # # #                     result = email_service.send_application_confirmation(
# # # #                         to_email=freelancer['email'],
# # # #                         freelancer_name=freelancer_name,
# # # #                         job_title=job['title'],
# # # #                         company_name=company_name,
# # # #                         user_id=freelancer['id']
# # # #                     )
# # # #                     print(f"📧 Email send result to freelancer: {result}")
# # # #                 else:
# # # #                     print(f"❌ Email service is None!")
# # # #             except Exception as e:
# # # #                 print(f"⚠️ Failed to send confirmation email: {e}")
# # # #                 traceback.print_exc()
# # # #         else:
# # # #             print(f"❌ Could not get freelancer or recruiter info")
        
# # # #         return jsonify({
# # # #             'success': True,
# # # #             'message': 'Application submitted successfully! The recruiter has been notified.',
# # # #             'application_id': application_id
# # # #         }), 201
        
# # # #     except Exception as e:
# # # #         print(f"❌ Error in apply_for_job: {str(e)}")
# # # #         traceback.print_exc()
# # # #         return jsonify({
# # # #             'success': False,
# # # #             'message': f'Application failed: {str(e)}'
# # # #         }), 500
    
# # # # @freelancer_bp.route('/applications', methods=['GET'])
# # # # @token_required
# # # # @freelancer_required
# # # # def get_applications():
# # # #     """Get all applications by freelancer"""
# # # #     try:
# # # #         applications = JobApplication.get_by_freelancer(request.user_id)
        
# # # #         return jsonify({
# # # #             'success': True,
# # # #             'count': len(applications),
# # # #             'applications': applications
# # # #         }), 200
# # # #     except Exception as e:
# # # #         print(f"❌ Error in get_applications: {str(e)}")
# # # #         traceback.print_exc()
# # # #         return jsonify({
# # # #             'success': False,
# # # #             'message': f'Server error: {str(e)}'
# # # #         }), 500

# # # # @freelancer_bp.route('/dashboard', methods=['GET'])
# # # # @token_required
# # # # @freelancer_required
# # # # def get_dashboard():
# # # #     """Get freelancer dashboard data"""
# # # #     try:
# # # #         profile = FreelancerProfile.get_by_user_id(request.user_id)
# # # #         applications = JobApplication.get_by_freelancer(request.user_id)
        
# # # #         # Get recommended jobs based on skills
# # # #         recommended_jobs = []
# # # #         if profile and profile.get('skills'):
# # # #             skill_names = [s['name'] for s in profile['skills']]
# # # #             print(f"🎯 Freelancer skills: {skill_names}")
            
# # # #             if skill_names:
# # # #                 # Search for jobs with matching skills
# # # #                 for skill in skill_names[:3]:
# # # #                     jobs = Job.search_jobs({'search': skill})
# # # #                     if jobs:
# # # #                         print(f"Found {len(jobs)} jobs for skill: {skill}")
# # # #                         recommended_jobs.extend(jobs[:2])
        
# # # #         # Remove duplicates
# # # #         seen = set()
# # # #         unique_jobs = []
# # # #         for job in recommended_jobs:
# # # #             if job['id'] not in seen:
# # # #                 seen.add(job['id'])
# # # #                 unique_jobs.append(job)
        
# # # #         print(f"📊 Recommended {len(unique_jobs)} unique jobs")
        
# # # #         # Calculate profile completion percentage
# # # #         profile_completion = 0
# # # #         if profile:
# # # #             fields = ['bio', 'hourly_rate', 'education', 'experience', 
# # # #                      'github_url', 'linkedin_url', 'portfolio_url']
# # # #             completed = sum(1 for field in fields if profile.get(field))
# # # #             if profile.get('skills') and len(profile['skills']) > 0:
# # # #                 completed += 1
# # # #             if profile.get('tech_stacks') and len(profile['tech_stacks']) > 0:
# # # #                 completed += 1
# # # #             total_fields = len(fields) + 2
# # # #             profile_completion = int((completed / total_fields) * 100)
        
# # # #         stats = {
# # # #             'total_applications': len(applications),
# # # #             'pending_applications': sum(1 for a in applications if a['status'] == 'applied'),
# # # #             'accepted_applications': sum(1 for a in applications if a['status'] == 'accepted'),
# # # #             'rejected_applications': sum(1 for a in applications if a['status'] == 'rejected'),
# # # #             'profile_completion': profile_completion
# # # #         }
        
# # # #         return jsonify({
# # # #             'success': True,
# # # #             'profile': profile,
# # # #             'recent_applications': applications[:5],
# # # #             'recommended_jobs': unique_jobs[:6],
# # # #             'stats': stats
# # # #         }), 200
        
# # # #     except Exception as e:
# # # #         print(f"❌ Error in get_dashboard: {str(e)}")
# # # #         traceback.print_exc()
# # # #         return jsonify({
# # # #             'success': False,
# # # #             'message': f'Server error: {str(e)}'
# # # #         }), 500


# # # # @freelancer_bp.route('/test-email', methods=['GET'])
# # # # @token_required
# # # # def test_email():
# # # #     """Test email sending"""
# # # #     try:
# # # #         user = User.find_by_id(request.user_id)
# # # #         if not user:
# # # #             return jsonify({'success': False, 'message': 'User not found'})
        
# # # #         if email_service:
# # # #             freelancer_name = f"{user['first_name']} {user['last_name']}"
# # # #             email_service.send_application_confirmation(
# # # #                 to_email=user['email'],
# # # #                 freelancer_name=freelancer_name,
# # # #                 job_title="Test Job",
# # # #                 company_name="Test Company",
# # # #                 user_id=user['id']
# # # #             )
# # # #             return jsonify({'success': True, 'message': 'Test email sent! Check your inbox.'})
# # # #         else:
# # # #             return jsonify({'success': False, 'message': 'Email service not initialized'})
# # # #     except Exception as e:
# # # #         return jsonify({'success': False, 'message': str(e)}), 500
    


# # # # @freelancer_bp.route('/test-email-simple', methods=['GET', 'OPTIONS'])
# # # # def test_email_simple():
# # # #     """Simple test endpoint for email - no auth required"""
# # # #     # Handle OPTIONS request for CORS
# # # #     if request.method == 'OPTIONS':
# # # #         response = jsonify({'success': True})
# # # #         response.headers.add('Access-Control-Allow-Origin', 'http://localhost:3000')
# # # #         response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
# # # #         response.headers.add('Access-Control-Allow-Methods', 'GET,OPTIONS')
# # # #         response.headers.add('Access-Control-Allow-Credentials', 'true')
# # # #         return response
        
# # # #     try:
# # # #         print("=" * 50)
# # # #         print("TEST EMAIL SIMPLE ENDPOINT CALLED")
# # # #         print("=" * 50)
        
# # # #         # Import here to avoid circular imports
# # # #         from flask_mail import Message
        
# # # #         # Get mail instance from current_app
# # # #         from flask import current_app
        
# # # #         # Create a simple test message
# # # #         msg = Message(
# # # #             subject="Test Email from FreelanceHub",
# # # #             recipients=["star36522253@gmail.com"],
# # # #             body="This is a test email to verify SMTP configuration. If you received this, email is working!",
# # # #             sender=current_app.config.get('FROM_EMAIL', 'noreply@freelancehub.com')
# # # #         )
        
# # # #         # Try to send
# # # #         print(f"📧 Attempting to send test email to star36522253@gmail.com...")
# # # #         print(f"📧 Mail server: {current_app.config.get('MAIL_SERVER')}")
# # # #         print(f"📧 Mail username: {current_app.config.get('MAIL_USERNAME')}")
        
# # # #         from flask_mail import Mail
# # # #         mail = Mail(current_app)
# # # #         mail.send(msg)
# # # #         print(f"✅ Test email sent successfully!")
        
# # # #         response = jsonify({'success': True, 'message': 'Test email sent! Check your inbox.'})
# # # #         response.headers.add('Access-Control-Allow-Origin', 'http://localhost:3000')
# # # #         return response
# # # #     except Exception as e:
# # # #         print(f"❌ Test email failed: {str(e)}")
# # # #         traceback.print_exc()
# # # #         response = jsonify({'success': False, 'message': str(e)})
# # # #         response.headers.add('Access-Control-Allow-Origin', 'http://localhost:3000')
# # # #         return response, 500

# # # # @freelancer_bp.route('/test-email', methods=['GET', 'OPTIONS'])
# # # # @token_required
# # # # def test_email():
# # # #     """Test email sending with auth"""
# # # #     # Handle OPTIONS request for CORS
# # # #     if request.method == 'OPTIONS':
# # # #         response = jsonify({'success': True})
# # # #         response.headers.add('Access-Control-Allow-Origin', 'http://localhost:3000')
# # # #         response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
# # # #         response.headers.add('Access-Control-Allow-Methods', 'GET,OPTIONS')
# # # #         response.headers.add('Access-Control-Allow-Credentials', 'true')
# # # #         return response
        
# # # #     try:
# # # #         print("=" * 50)
# # # #         print("TEST EMAIL AUTH ENDPOINT CALLED")
# # # #         print("=" * 50)
        
# # # #         user = User.find_by_id(request.user_id)
# # # #         if not user:
# # # #             return jsonify({'success': False, 'message': 'User not found'}), 404
        
# # # #         print(f"👤 User found: {user['email']}")
        
# # # #         if email_service:
# # # #             freelancer_name = f"{user['first_name']} {user['last_name']}"
# # # #             print(f"📧 Calling email_service.send_application_confirmation...")
            
# # # #             result = email_service.send_application_confirmation(
# # # #                 to_email=user['email'],
# # # #                 freelancer_name=freelancer_name,
# # # #                 job_title="Test Job",
# # # #                 company_name="Test Company",
# # # #                 user_id=user['id']
# # # #             )
            
# # # #             print(f"📧 Email service returned: {result}")
            
# # # #             response = jsonify({'success': True, 'message': 'Test email sent! Check your inbox.'})
# # # #             response.headers.add('Access-Control-Allow-Origin', 'http://localhost:3000')
# # # #             return response
# # # #         else:
# # # #             print(f"❌ Email service is None!")
# # # #             response = jsonify({'success': False, 'message': 'Email service not initialized'})
# # # #             response.headers.add('Access-Control-Allow-Origin', 'http://localhost:3000')
# # # #             return response, 500
# # # #     except Exception as e:
# # # #         print(f"❌ Test email failed: {str(e)}")
# # # #         traceback.print_exc()
# # # #         response = jsonify({'success': False, 'message': str(e)})
# # # #         response.headers.add('Access-Control-Allow-Origin', 'http://localhost:3000')
# # # #         return response, 500
# # # from flask import Blueprint, request, jsonify, current_app
# # # from database.models import FreelancerProfile, Job, JobApplication, Notification, User
# # # from utils.auth_utils import token_required, freelancer_required
# # # from services.email_service import email_service
# # # from database.db_config import get_db_connection
# # # from datetime import datetime
# # # import traceback

# # # freelancer_bp = Blueprint('freelancer', __name__, url_prefix='/api/freelancer')

# # # # ============== PROFILE ENDPOINTS ==============

# # # @freelancer_bp.route('/profile', methods=['GET'])
# # # @token_required
# # # @freelancer_required
# # # def get_profile():
# # #     """Get freelancer profile"""
# # #     try:
# # #         profile = FreelancerProfile.get_by_user_id(request.user_id)
        
# # #         if not profile:
# # #             return jsonify({
# # #                 'success': False,
# # #                 'message': 'Profile not found'
# # #             }), 404
        
# # #         return jsonify({
# # #             'success': True,
# # #             'profile': profile
# # #         }), 200
# # #     except Exception as e:
# # #         print(f"❌ Error in get_profile: {str(e)}")
# # #         traceback.print_exc()
# # #         return jsonify({
# # #             'success': False,
# # #             'message': f'Server error: {str(e)}'
# # #         }), 500

# # # @freelancer_bp.route('/profile', methods=['PUT'])
# # # @token_required
# # # @freelancer_required
# # # def update_profile():
# # #     """Update freelancer profile"""
# # #     try:
# # #         data = request.get_json()
        
# # #         if not data:
# # #             return jsonify({
# # #                 'success': False,
# # #                 'message': 'No data provided'
# # #             }), 400
        
# # #         profile = FreelancerProfile.update_profile(request.user_id, data)
        
# # #         if not profile:
# # #             return jsonify({
# # #                 'success': False,
# # #                 'message': 'Profile not found'
# # #             }), 404
        
# # #         return jsonify({
# # #             'success': True,
# # #             'message': 'Profile updated successfully',
# # #             'profile': profile
# # #         }), 200
# # #     except Exception as e:
# # #         print(f"❌ Error in update_profile: {str(e)}")
# # #         traceback.print_exc()
# # #         return jsonify({
# # #             'success': False,
# # #             'message': f'Server error: {str(e)}'
# # #         }), 500

# # # # ============== JOB SEARCH ENDPOINTS ==============

# # # @freelancer_bp.route('/jobs/search', methods=['GET'])
# # # @token_required
# # # @freelancer_required
# # # def search_jobs():
# # #     """Search for jobs with improved filtering"""
# # #     try:
# # #         # Get filter parameters
# # #         search = request.args.get('search', '')
# # #         experience_level = request.args.get('experience_level', '')
# # #         min_pay = request.args.get('min_pay', '')
# # #         max_pay = request.args.get('max_pay', '')
# # #         job_type = request.args.get('job_type', '')
# # #         is_remote = request.args.get('is_remote', '')
        
# # #         # Build filters dictionary (only include non-empty values)
# # #         filters = {}
# # #         if search and search.strip():
# # #             filters['search'] = search.strip()
# # #         if experience_level and experience_level.strip():
# # #             filters['experience_level'] = experience_level.strip()
# # #         if min_pay and min_pay.strip():
# # #             try:
# # #                 filters['min_pay'] = float(min_pay)
# # #             except ValueError:
# # #                 pass
# # #         if max_pay and max_pay.strip():
# # #             try:
# # #                 filters['max_pay'] = float(max_pay)
# # #             except ValueError:
# # #                 pass
# # #         if job_type and job_type.strip() and job_type != 'All Types':
# # #             filters['job_type'] = job_type.strip()
# # #         if is_remote and is_remote.lower() == 'true':
# # #             filters['is_remote'] = True
        
# # #         print(f"🔍 Search filters: {filters}")
        
# # #         jobs = Job.search_jobs(filters)
        
# # #         print(f"✅ Found {len(jobs)} jobs")
        
# # #         return jsonify({
# # #             'success': True,
# # #             'count': len(jobs),
# # #             'jobs': jobs
# # #         }), 200
        
# # #     except Exception as e:
# # #         print(f"❌ Error in search_jobs: {str(e)}")
# # #         traceback.print_exc()
# # #         return jsonify({
# # #             'success': False,
# # #             'message': f'Search failed: {str(e)}',
# # #             'jobs': []
# # #         }), 500

# # # @freelancer_bp.route('/jobs/<int:job_id>', methods=['GET'])
# # # @token_required
# # # @freelancer_required
# # # def get_job_details(job_id):
# # #     """Get job details by ID"""
# # #     try:
# # #         print(f"🔍 Fetching job details for ID: {job_id}")
# # #         job = Job.get_by_id(job_id)
        
# # #         if not job:
# # #             return jsonify({
# # #                 'success': False,
# # #                 'message': 'Job not found'
# # #             }), 404
        
# # #         return jsonify({
# # #             'success': True,
# # #             'job': job
# # #         }), 200
# # #     except Exception as e:
# # #         print(f"❌ Error in get_job_details: {str(e)}")
# # #         traceback.print_exc()
# # #         return jsonify({
# # #             'success': False,
# # #             'message': f'Server error: {str(e)}'
# # #         }), 500

# # # # ============== APPLICATION ENDPOINTS ==============

# # # @freelancer_bp.route('/jobs/<int:job_id>/apply', methods=['POST'])
# # # @token_required
# # # @freelancer_required
# # # def apply_for_job(job_id):
# # #     """Apply for a job with email notification"""
# # #     try:
# # #         data = request.get_json() or {}
        
# # #         print(f"📝 Freelancer {request.user_id} applying for job {job_id}")
# # #         print(f"📦 Application data: {data}")
        
# # #         # Validate required fields
# # #         if not data.get('cover_letter'):
# # #             return jsonify({
# # #                 'success': False,
# # #                 'message': 'Cover letter is required'
# # #             }), 400
        
# # #         # First check if job exists
# # #         job = Job.get_by_id(job_id)
# # #         if not job:
# # #             print(f"❌ Job {job_id} not found")
# # #             return jsonify({
# # #                 'success': False,
# # #                 'message': 'Job not found'
# # #             }), 404
            
# # #         print(f"✅ Job found: {job['title']}")
# # #         print(f"📧 Job details - Recruiter ID: {job['recruiter_id']}, Recruiter Email: {job.get('recruiter_email', 'N/A')}")
        
# # #         # Create application
# # #         application_id = JobApplication.create(
# # #             job_id=job_id,
# # #             freelancer_id=request.user_id,
# # #             application_data=data
# # #         )
        
# # #         if not application_id:
# # #             # Check if it's because of duplicate application
# # #             connection = get_db_connection()
# # #             cursor = connection.cursor()
# # #             cursor.execute("""
# # #                 SELECT id, status FROM job_applications 
# # #                 WHERE job_id = %s AND freelancer_id = %s
# # #             """, (job_id, request.user_id))
# # #             existing = cursor.fetchone()
# # #             cursor.close()
# # #             connection.close()
            
# # #             if existing:
# # #                 return jsonify({
# # #                     'success': False,
# # #                     'message': f'You have already applied for this job (Status: {existing["status"]})'
# # #                 }), 400
# # #             else:
# # #                 return jsonify({
# # #                     'success': False,
# # #                     'message': 'Failed to create application. Please try again.'
# # #                 }), 400
        
# # #         print(f"✅ Application created with ID: {application_id}")
        
# # #         # Get freelancer and recruiter info for notifications
# # #         freelancer = User.find_by_id(request.user_id)
# # #         recruiter = User.find_by_id(job['recruiter_id'])
        
# # #         print(f"👤 Freelancer: {freelancer['email'] if freelancer else 'Not found'}")
# # #         print(f"👤 Recruiter: {recruiter['email'] if recruiter else 'Not found'}")
        
# # #         if freelancer and recruiter:
# # #             freelancer_name = f"{freelancer['first_name']} {freelancer['last_name']}"
# # #             recruiter_name = f"{recruiter['first_name']} {recruiter['last_name']}"
            
# # #             # 1. Create in-app notification for recruiter
# # #             Notification.create(
# # #                 user_id=job['recruiter_id'],
# # #                 title='New Job Application',
# # #                 message=f'{freelancer_name} has applied for {job["title"]}',
# # #                 notification_type='application',
# # #                 related_application_id=application_id,
# # #                 related_job_id=job_id
# # #             )
# # #             print(f"✅ In-app notification created for recruiter {job['recruiter_id']}")
            
# # #             # 2. Send email notification to recruiter
# # #             try:
# # #                 if email_service:
# # #                     print(f"📧 Email service exists, preparing to send to recruiter: {recruiter['email']}")
# # #                     company_name = job.get('company_name', 'Company')
# # #                     result = email_service.send_application_submitted_notification(
# # #                         to_email=recruiter['email'],
# # #                         recruiter_name=recruiter_name,
# # #                         freelancer_name=freelancer_name,
# # #                         job_title=job['title'],
# # #                         job_id=job_id,
# # #                         application_id=application_id,
# # #                         user_id=recruiter['id']
# # #                     )
# # #                     print(f"📧 Email send result to recruiter: {result}")
# # #                 else:
# # #                     print(f"❌ Email service is None!")
# # #             except Exception as e:
# # #                 print(f"⚠️ Failed to send email notification to recruiter: {e}")
# # #                 traceback.print_exc()
            
# # #             # 3. Send confirmation email to freelancer
# # #             try:
# # #                 if email_service:
# # #                     print(f"📧 Preparing to send confirmation to freelancer: {freelancer['email']}")
# # #                     company_name = job.get('company_name', 'Company')
# # #                     result = email_service.send_application_confirmation(
# # #                         to_email=freelancer['email'],
# # #                         freelancer_name=freelancer_name,
# # #                         job_title=job['title'],
# # #                         company_name=company_name,
# # #                         user_id=freelancer['id']
# # #                     )
# # #                     print(f"📧 Email send result to freelancer: {result}")
# # #                 else:
# # #                     print(f"❌ Email service is None!")
# # #             except Exception as e:
# # #                 print(f"⚠️ Failed to send confirmation email: {e}")
# # #                 traceback.print_exc()
# # #         else:
# # #             print(f"❌ Could not get freelancer or recruiter info")
        
# # #         return jsonify({
# # #             'success': True,
# # #             'message': 'Application submitted successfully! The recruiter has been notified.',
# # #             'application_id': application_id
# # #         }), 201
        
# # #     except Exception as e:
# # #         print(f"❌ Error in apply_for_job: {str(e)}")
# # #         traceback.print_exc()
# # #         return jsonify({
# # #             'success': False,
# # #             'message': f'Application failed: {str(e)}'
# # #         }), 500

# # # @freelancer_bp.route('/applications', methods=['GET'])
# # # @token_required
# # # @freelancer_required
# # # def get_applications():
# # #     """Get all applications by freelancer"""
# # #     try:
# # #         applications = JobApplication.get_by_freelancer(request.user_id)
        
# # #         return jsonify({
# # #             'success': True,
# # #             'count': len(applications),
# # #             'applications': applications
# # #         }), 200
# # #     except Exception as e:
# # #         print(f"❌ Error in get_applications: {str(e)}")
# # #         traceback.print_exc()
# # #         return jsonify({
# # #             'success': False,
# # #             'message': f'Server error: {str(e)}'
# # #         }), 500

# # # # ============== DASHBOARD ENDPOINT ==============

# # # @freelancer_bp.route('/dashboard', methods=['GET'])
# # # @token_required
# # # @freelancer_required
# # # def get_dashboard():
# # #     """Get freelancer dashboard data"""
# # #     try:
# # #         profile = FreelancerProfile.get_by_user_id(request.user_id)
# # #         applications = JobApplication.get_by_freelancer(request.user_id)
        
# # #         # Get recommended jobs based on skills
# # #         recommended_jobs = []
# # #         if profile and profile.get('skills'):
# # #             skill_names = [s['name'] for s in profile['skills']]
# # #             print(f"🎯 Freelancer skills: {skill_names}")
            
# # #             if skill_names:
# # #                 # Search for jobs with matching skills
# # #                 for skill in skill_names[:3]:
# # #                     jobs = Job.search_jobs({'search': skill})
# # #                     if jobs:
# # #                         print(f"Found {len(jobs)} jobs for skill: {skill}")
# # #                         recommended_jobs.extend(jobs[:2])
        
# # #         # Remove duplicates
# # #         seen = set()
# # #         unique_jobs = []
# # #         for job in recommended_jobs:
# # #             if job['id'] not in seen:
# # #                 seen.add(job['id'])
# # #                 unique_jobs.append(job)
        
# # #         print(f"📊 Recommended {len(unique_jobs)} unique jobs")
        
# # #         # Calculate profile completion percentage
# # #         profile_completion = 0
# # #         if profile:
# # #             fields = ['bio', 'hourly_rate', 'education', 'experience', 
# # #                      'github_url', 'linkedin_url', 'portfolio_url']
# # #             completed = sum(1 for field in fields if profile.get(field))
# # #             if profile.get('skills') and len(profile['skills']) > 0:
# # #                 completed += 1
# # #             if profile.get('tech_stacks') and len(profile['tech_stacks']) > 0:
# # #                 completed += 1
# # #             total_fields = len(fields) + 2
# # #             profile_completion = int((completed / total_fields) * 100)
        
# # #         stats = {
# # #             'total_applications': len(applications),
# # #             'pending_applications': sum(1 for a in applications if a['status'] == 'applied'),
# # #             'accepted_applications': sum(1 for a in applications if a['status'] == 'accepted'),
# # #             'rejected_applications': sum(1 for a in applications if a['status'] == 'rejected'),
# # #             'profile_completion': profile_completion
# # #         }
        
# # #         return jsonify({
# # #             'success': True,
# # #             'profile': profile,
# # #             'recent_applications': applications[:5],
# # #             'recommended_jobs': unique_jobs[:6],
# # #             'stats': stats
# # #         }), 200
        
# # #     except Exception as e:
# # #         print(f"❌ Error in get_dashboard: {str(e)}")
# # #         traceback.print_exc()
# # #         return jsonify({
# # #             'success': False,
# # #             'message': f'Server error: {str(e)}'
# # #         }), 500

# # # # ============== TEST EMAIL ENDPOINTS ==============

# # # @freelancer_bp.route('/test-email-simple', methods=['GET', 'OPTIONS'])
# # # def test_email_simple():
# # #     """Simple test endpoint for email - no auth required"""
# # #     # Handle OPTIONS request for CORS
# # #     if request.method == 'OPTIONS':
# # #         response = jsonify({'success': True})
# # #         response.headers.add('Access-Control-Allow-Origin', 'http://localhost:3000')
# # #         response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
# # #         response.headers.add('Access-Control-Allow-Methods', 'GET,OPTIONS')
# # #         response.headers.add('Access-Control-Allow-Credentials', 'true')
# # #         return response
        
# # #     try:
# # #         print("=" * 50)
# # #         print("TEST EMAIL SIMPLE ENDPOINT CALLED")
# # #         print("=" * 50)
        
# # #         # Import here to avoid circular imports
# # #         from flask_mail import Message
        
# # #         # Get mail instance from current_app
# # #         from flask import current_app
        
# # #         # Create a simple test message
# # #         msg = Message(
# # #             subject="Test Email from FreelanceHub",
# # #             recipients=["star36522253@gmail.com"],
# # #             body="This is a test email to verify SMTP configuration. If you received this, email is working!",
# # #             sender=current_app.config.get('FROM_EMAIL', 'noreply@freelancehub.com')
# # #         )
        
# # #         # Try to send
# # #         print(f"📧 Attempting to send test email to star36522253@gmail.com...")
# # #         print(f"📧 Mail server: {current_app.config.get('MAIL_SERVER')}")
# # #         print(f"📧 Mail username: {current_app.config.get('MAIL_USERNAME')}")
        
# # #         from flask_mail import Mail
# # #         mail = Mail(current_app)
# # #         mail.send(msg)
# # #         print(f"✅ Test email sent successfully!")
        
# # #         response = jsonify({'success': True, 'message': 'Test email sent! Check your inbox.'})
# # #         response.headers.add('Access-Control-Allow-Origin', 'http://localhost:3000')
# # #         return response
# # #     except Exception as e:
# # #         print(f"❌ Test email failed: {str(e)}")
# # #         traceback.print_exc()
# # #         response = jsonify({'success': False, 'message': str(e)})
# # #         response.headers.add('Access-Control-Allow-Origin', 'http://localhost:3000')
# # #         return response, 500

# # # @freelancer_bp.route('/test-email-auth', methods=['GET', 'OPTIONS'])
# # # @token_required
# # # def test_email_auth():
# # #     """Test email sending with auth"""
# # #     # Handle OPTIONS request for CORS
# # #     if request.method == 'OPTIONS':
# # #         response = jsonify({'success': True})
# # #         response.headers.add('Access-Control-Allow-Origin', 'http://localhost:3000')
# # #         response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
# # #         response.headers.add('Access-Control-Allow-Methods', 'GET,OPTIONS')
# # #         response.headers.add('Access-Control-Allow-Credentials', 'true')
# # #         return response
        
# # #     try:
# # #         print("=" * 50)
# # #         print("TEST EMAIL AUTH ENDPOINT CALLED")
# # #         print("=" * 50)
        
# # #         user = User.find_by_id(request.user_id)
# # #         if not user:
# # #             return jsonify({'success': False, 'message': 'User not found'}), 404
        
# # #         print(f"👤 User found: {user['email']}")
        
# # #         if email_service:
# # #             freelancer_name = f"{user['first_name']} {user['last_name']}"
# # #             print(f"📧 Calling email_service.send_application_confirmation...")
            
# # #             result = email_service.send_application_confirmation(
# # #                 to_email=user['email'],
# # #                 freelancer_name=freelancer_name,
# # #                 job_title="Test Job",
# # #                 company_name="Test Company",
# # #                 user_id=user['id']
# # #             )
            
# # #             print(f"📧 Email service returned: {result}")
            
# # #             response = jsonify({'success': True, 'message': 'Test email sent! Check your inbox.'})
# # #             response.headers.add('Access-Control-Allow-Origin', 'http://localhost:3000')
# # #             return response
# # #         else:
# # #             print(f"❌ Email service is None!")
# # #             response = jsonify({'success': False, 'message': 'Email service not initialized'})
# # #             response.headers.add('Access-Control-Allow-Origin', 'http://localhost:3000')
# # #             return response, 500
# # #     except Exception as e:
# # #         print(f"❌ Test email failed: {str(e)}")
# # #         traceback.print_exc()
# # #         response = jsonify({'success': False, 'message': str(e)})
# # #         response.headers.add('Access-Control-Allow-Origin', 'http://localhost:3000')
# # #         return response, 500
# # from flask import Blueprint, request, jsonify, current_app
# # from database.models import FreelancerProfile, Job, JobApplication, Notification, User
# # from utils.auth_utils import token_required, freelancer_required
# # from database.db_config import get_db_connection
# # from datetime import datetime
# # import traceback

# # from services.email_service import email_service as global_email_service
# # from flask import current_app

# # # Then in your functions, use it like this:
# # email_service = global_email_service  # This is the global instance
# # # OR better yet, get it from app config:
# # # email_service = current_app.config.get('EMAIL_SERVICE')

# # freelancer_bp = Blueprint('freelancer', __name__, url_prefix='/api/freelancer')

# # # ============== PROFILE ENDPOINTS ==============

# # @freelancer_bp.route('/profile', methods=['GET'])
# # @token_required
# # @freelancer_required
# # def get_profile():
# #     """Get freelancer profile"""
# #     try:
# #         profile = FreelancerProfile.get_by_user_id(request.user_id)
        
# #         if not profile:
# #             return jsonify({
# #                 'success': False,
# #                 'message': 'Profile not found'
# #             }), 404
        
# #         return jsonify({
# #             'success': True,
# #             'profile': profile
# #         }), 200
# #     except Exception as e:
# #         print(f"❌ Error in get_profile: {str(e)}")
# #         traceback.print_exc()
# #         return jsonify({
# #             'success': False,
# #             'message': f'Server error: {str(e)}'
# #         }), 500

# # @freelancer_bp.route('/profile', methods=['PUT'])
# # @token_required
# # @freelancer_required
# # def update_profile():
# #     """Update freelancer profile"""
# #     try:
# #         data = request.get_json()
        
# #         if not data:
# #             return jsonify({
# #                 'success': False,
# #                 'message': 'No data provided'
# #             }), 400
        
# #         profile = FreelancerProfile.update_profile(request.user_id, data)
        
# #         if not profile:
# #             return jsonify({
# #                 'success': False,
# #                 'message': 'Profile not found'
# #             }), 404
        
# #         return jsonify({
# #             'success': True,
# #             'message': 'Profile updated successfully',
# #             'profile': profile
# #         }), 200
# #     except Exception as e:
# #         print(f"❌ Error in update_profile: {str(e)}")
# #         traceback.print_exc()
# #         return jsonify({
# #             'success': False,
# #             'message': f'Server error: {str(e)}'
# #         }), 500

# # # ============== JOB SEARCH ENDPOINTS ==============

# # @freelancer_bp.route('/jobs/search', methods=['GET'])
# # @token_required
# # @freelancer_required
# # def search_jobs():
# #     """Search for jobs with improved filtering"""
# #     try:
# #         # Get filter parameters
# #         search = request.args.get('search', '')
# #         experience_level = request.args.get('experience_level', '')
# #         min_pay = request.args.get('min_pay', '')
# #         max_pay = request.args.get('max_pay', '')
# #         job_type = request.args.get('job_type', '')
# #         is_remote = request.args.get('is_remote', '')
        
# #         # Build filters dictionary (only include non-empty values)
# #         filters = {}
# #         if search and search.strip():
# #             filters['search'] = search.strip()
# #         if experience_level and experience_level.strip():
# #             filters['experience_level'] = experience_level.strip()
# #         if min_pay and min_pay.strip():
# #             try:
# #                 filters['min_pay'] = float(min_pay)
# #             except ValueError:
# #                 pass
# #         if max_pay and max_pay.strip():
# #             try:
# #                 filters['max_pay'] = float(max_pay)
# #             except ValueError:
# #                 pass
# #         if job_type and job_type.strip() and job_type != 'All Types':
# #             filters['job_type'] = job_type.strip()
# #         if is_remote and is_remote.lower() == 'true':
# #             filters['is_remote'] = True
        
# #         print(f"🔍 Search filters: {filters}")
        
# #         jobs = Job.search_jobs(filters)
        
# #         print(f"✅ Found {len(jobs)} jobs")
        
# #         return jsonify({
# #             'success': True,
# #             'count': len(jobs),
# #             'jobs': jobs
# #         }), 200
        
# #     except Exception as e:
# #         print(f"❌ Error in search_jobs: {str(e)}")
# #         traceback.print_exc()
# #         return jsonify({
# #             'success': False,
# #             'message': f'Search failed: {str(e)}',
# #             'jobs': []
# #         }), 500

# # @freelancer_bp.route('/jobs/<int:job_id>', methods=['GET'])
# # @token_required
# # @freelancer_required
# # def get_job_details(job_id):
# #     """Get job details by ID"""
# #     try:
# #         print(f"🔍 Fetching job details for ID: {job_id}")
# #         job = Job.get_by_id(job_id)
        
# #         if not job:
# #             return jsonify({
# #                 'success': False,
# #                 'message': 'Job not found'
# #             }), 404
        
# #         return jsonify({
# #             'success': True,
# #             'job': job
# #         }), 200
# #     except Exception as e:
# #         print(f"❌ Error in get_job_details: {str(e)}")
# #         traceback.print_exc()
# #         return jsonify({
# #             'success': False,
# #             'message': f'Server error: {str(e)}'
# #         }), 500
# # @freelancer_bp.route('/debug-email-status', methods=['GET'])
# # def debug_email_status():
# #     """Debug endpoint to check email service status"""
# #     try:
# #         from services.email_service import email_service as global_email_service
        
# #         status = {
# #             'email_service_exists': global_email_service is not None,
# #             'mail_configured': global_email_service.mail is not None if global_email_service else False,
# #             'has_mail_attribute': hasattr(global_email_service, 'mail') if global_email_service else False,
# #         }
        
# #         if global_email_service and global_email_service.mail:
# #             # Try to get mail config
# #             try:
# #                 status['mail_server'] = current_app.config.get('MAIL_SERVER')
# #                 status['mail_username'] = current_app.config.get('MAIL_USERNAME')
# #                 status['mail_port'] = current_app.config.get('MAIL_PORT')
# #                 status['mail_use_tls'] = current_app.config.get('MAIL_USE_TLS')
# #             except:
# #                 pass
        
# #         return jsonify({'success': True, 'status': status})
# #     except Exception as e:
# #         return jsonify({'success': False, 'error': str(e)}), 500
# # # ============== APPLICATION ENDPOINTS ==============
# # @freelancer_bp.route('/jobs/<int:job_id>/apply', methods=['POST'])
# # @token_required
# # @freelancer_required
# # def apply_for_job(job_id):
# #     """Apply for a job with email notification"""
# #     try:
# #         data = request.get_json() or {}
        
# #         print(f"📝 Freelancer {request.user_id} applying for job {job_id}")
# #         print(f"📦 Application data: {data}")
        
# #         # Validate required fields
# #         if not data.get('cover_letter'):
# #             return jsonify({
# #                 'success': False,
# #                 'message': 'Cover letter is required'
# #             }), 400
        
# #         # First check if job exists
# #         job = Job.get_by_id(job_id)
# #         if not job:
# #             print(f"❌ Job {job_id} not found")
# #             return jsonify({
# #                 'success': False,
# #                 'message': 'Job not found'
# #             }), 404
            
# #         print(f"✅ Job found: {job['title']}")
# #         print(f"📧 Job details - Recruiter ID: {job['recruiter_id']}, Recruiter Email: {job.get('recruiter_email', 'N/A')}")
        
# #         # Create application
# #         application_id = JobApplication.create(
# #             job_id=job_id,
# #             freelancer_id=request.user_id,
# #             application_data=data
# #         )
        
# #         if not application_id:
# #             # Check if it's because of duplicate application
# #             connection = get_db_connection()
# #             cursor = connection.cursor()
# #             cursor.execute("""
# #                 SELECT id, status FROM job_applications 
# #                 WHERE job_id = %s AND freelancer_id = %s
# #             """, (job_id, request.user_id))
# #             existing = cursor.fetchone()
# #             cursor.close()
# #             connection.close()
            
# #             if existing:
# #                 return jsonify({
# #                     'success': False,
# #                     'message': f'You have already applied for this job (Status: {existing["status"]})'
# #                 }), 400
# #             else:
# #                 return jsonify({
# #                     'success': False,
# #                     'message': 'Failed to create application. Please try again.'
# #                 }), 400
        
# #         print(f"✅ Application created with ID: {application_id}")
        
# #         # Get freelancer and recruiter info for notifications
# #         freelancer = User.find_by_id(request.user_id)
# #         recruiter = User.find_by_id(job['recruiter_id'])
        
# #         print(f"👤 Freelancer: {freelancer['email'] if freelancer else 'Not found'}")
# #         print(f"👤 Recruiter: {recruiter['email'] if recruiter else 'Not found'}")
        
# #         if freelancer and recruiter:
# #             freelancer_name = f"{freelancer['first_name']} {freelancer['last_name']}"
# #             recruiter_name = f"{recruiter['first_name']} {recruiter['last_name']}"
            
# #             # 1. Create in-app notification for recruiter
# #             Notification.create(
# #                 user_id=job['recruiter_id'],
# #                 title='New Job Application',
# #                 message=f'{freelancer_name} has applied for {job["title"]}',
# #                 notification_type='application',
# #                 related_application_id=application_id,
# #                 related_job_id=job_id
# #             )
# #             print(f"✅ In-app notification created for recruiter {job['recruiter_id']}")
            
# #             # 2. Send email notification to recruiter
# #             try:
# #                 # Import here to avoid circular imports
# #                 from services.email_service import email_service as global_email_service
                
# #                 if global_email_service and global_email_service.mail:
# #                     print(f"📧 Email service exists, preparing to send to recruiter: {recruiter['email']}")
# #                     print(f"📧 Email service mail object: {global_email_service.mail is not None}")
                    
# #                     company_name = job.get('company_name', 'Company')
# #                     result = global_email_service.send_application_submitted_notification(
# #                         to_email=recruiter['email'],
# #                         recruiter_name=recruiter_name,
# #                         freelancer_name=freelancer_name,
# #                         job_title=job['title'],
# #                         job_id=job_id,
# #                         application_id=application_id,
# #                         user_id=recruiter['id']
# #                     )
# #                     print(f"📧 Email send result to recruiter: {result}")
# #                 else:
# #                     print(f"❌ Email service is None or mail not configured!")
# #                     print(f"   global_email_service: {global_email_service}")
# #                     if global_email_service:
# #                         print(f"   mail attribute: {global_email_service.mail is not None}")
# #             except Exception as e:
# #                 print(f"⚠️ Failed to send email notification to recruiter: {e}")
# #                 traceback.print_exc()
            
# #             # 3. Send confirmation email to freelancer
# #             try:
# #                 from services.email_service import email_service as global_email_service
                
# #                 if global_email_service and global_email_service.mail:
# #                     print(f"📧 Preparing to send confirmation to freelancer: {freelancer['email']}")
# #                     company_name = job.get('company_name', 'Company')
# #                     result = global_email_service.send_application_confirmation(
# #                         to_email=freelancer['email'],
# #                         freelancer_name=freelancer_name,
# #                         job_title=job['title'],
# #                         company_name=company_name,
# #                         user_id=freelancer['id']
# #                     )
# #                     print(f"📧 Email send result to freelancer: {result}")
# #                 else:
# #                     print(f"❌ Email service is None for freelancer confirmation!")
# #             except Exception as e:
# #                 print(f"⚠️ Failed to send confirmation email: {e}")
# #                 traceback.print_exc()
# #         else:
# #             print(f"❌ Could not get freelancer or recruiter info")
        
# #         return jsonify({
# #             'success': True,
# #             'message': 'Application submitted successfully! The recruiter has been notified.',
# #             'application_id': application_id
# #         }), 201
        
# #     except Exception as e:
# #         print(f"❌ Error in apply_for_job: {str(e)}")
# #         traceback.print_exc()
# #         return jsonify({
# #             'success': False,
# #             'message': f'Application failed: {str(e)}'
# #         }), 500
    

# # @freelancer_bp.route('/applications', methods=['GET'])
# # @token_required
# # @freelancer_required
# # def get_applications():
# #     """Get all applications by freelancer"""
# #     try:
# #         applications = JobApplication.get_by_freelancer(request.user_id)
        
# #         return jsonify({
# #             'success': True,
# #             'count': len(applications),
# #             'applications': applications
# #         }), 200
# #     except Exception as e:
# #         print(f"❌ Error in get_applications: {str(e)}")
# #         traceback.print_exc()
# #         return jsonify({
# #             'success': False,
# #             'message': f'Server error: {str(e)}'
# #         }), 500

# # # ============== DASHBOARD ENDPOINT ==============

# # @freelancer_bp.route('/dashboard', methods=['GET'])
# # @token_required
# # @freelancer_required
# # def get_dashboard():
# #     """Get freelancer dashboard data"""
# #     try:
# #         profile = FreelancerProfile.get_by_user_id(request.user_id)
# #         applications = JobApplication.get_by_freelancer(request.user_id)
        
# #         # Get recommended jobs based on skills
# #         recommended_jobs = []
# #         if profile and profile.get('skills'):
# #             skill_names = [s['name'] for s in profile['skills']]
# #             print(f"🎯 Freelancer skills: {skill_names}")
            
# #             if skill_names:
# #                 # Search for jobs with matching skills
# #                 for skill in skill_names[:3]:
# #                     jobs = Job.search_jobs({'search': skill})
# #                     if jobs:
# #                         print(f"Found {len(jobs)} jobs for skill: {skill}")
# #                         recommended_jobs.extend(jobs[:2])
        
# #         # Remove duplicates
# #         seen = set()
# #         unique_jobs = []
# #         for job in recommended_jobs:
# #             if job['id'] not in seen:
# #                 seen.add(job['id'])
# #                 unique_jobs.append(job)
        
# #         print(f"📊 Recommended {len(unique_jobs)} unique jobs")
        
# #         # Calculate profile completion percentage
# #         profile_completion = 0
# #         if profile:
# #             fields = ['bio', 'hourly_rate', 'education', 'experience', 
# #                      'github_url', 'linkedin_url', 'portfolio_url']
# #             completed = sum(1 for field in fields if profile.get(field))
# #             if profile.get('skills') and len(profile['skills']) > 0:
# #                 completed += 1
# #             if profile.get('tech_stacks') and len(profile['tech_stacks']) > 0:
# #                 completed += 1
# #             total_fields = len(fields) + 2
# #             profile_completion = int((completed / total_fields) * 100)
        
# #         stats = {
# #             'total_applications': len(applications),
# #             'pending_applications': sum(1 for a in applications if a['status'] == 'applied'),
# #             'accepted_applications': sum(1 for a in applications if a['status'] == 'accepted'),
# #             'rejected_applications': sum(1 for a in applications if a['status'] == 'rejected'),
# #             'profile_completion': profile_completion
# #         }
        
# #         return jsonify({
# #             'success': True,
# #             'profile': profile,
# #             'recent_applications': applications[:5],
# #             'recommended_jobs': unique_jobs[:6],
# #             'stats': stats
# #         }), 200
        
# #     except Exception as e:
# #         print(f"❌ Error in get_dashboard: {str(e)}")
# #         traceback.print_exc()
# #         return jsonify({
# #             'success': False,
# #             'message': f'Server error: {str(e)}'
# #         }), 500

# # # ============== TEST EMAIL ENDPOINTS ==============

# # @freelancer_bp.route('/test-email-simple', methods=['GET', 'OPTIONS'])
# # def test_email_simple():
# #     """Simple test endpoint for email - no auth required"""
# #     # Handle OPTIONS request for CORS
# #     if request.method == 'OPTIONS':
# #         response = jsonify({'success': True})
# #         response.headers.add('Access-Control-Allow-Origin', 'http://localhost:3000')
# #         response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
# #         response.headers.add('Access-Control-Allow-Methods', 'GET,OPTIONS')
# #         response.headers.add('Access-Control-Allow-Credentials', 'true')
# #         return response
        
# #     try:
# #         print("=" * 50)
# #         print("TEST EMAIL SIMPLE ENDPOINT CALLED")
# #         print("=" * 50)
        
# #         # Import here to avoid circular imports
# #         from flask_mail import Message
        
# #         # Get mail instance from current_app
# #         from flask import current_app
        
# #         # Create a simple test message
# #         msg = Message(
# #             subject="Test Email from FreelanceHub",
# #             recipients=["star36522253@gmail.com"],
# #             body="This is a test email to verify SMTP configuration. If you received this, email is working!",
# #             sender=current_app.config.get('FROM_EMAIL', 'noreply@freelancehub.com')
# #         )
        
# #         # Try to send
# #         print(f"📧 Attempting to send test email to star36522253@gmail.com...")
# #         print(f"📧 Mail server: {current_app.config.get('MAIL_SERVER')}")
# #         print(f"📧 Mail username: {current_app.config.get('MAIL_USERNAME')}")
        
# #         from flask_mail import Mail
# #         mail = Mail(current_app)
# #         mail.send(msg)
# #         print(f"✅ Test email sent successfully!")
        
# #         response = jsonify({'success': True, 'message': 'Test email sent! Check your inbox.'})
# #         response.headers.add('Access-Control-Allow-Origin', 'http://localhost:3000')
# #         return response
# #     except Exception as e:
# #         print(f"❌ Test email failed: {str(e)}")
# #         traceback.print_exc()
# #         response = jsonify({'success': False, 'message': str(e)})
# #         response.headers.add('Access-Control-Allow-Origin', 'http://localhost:3000')
# #         return response, 500


# # @freelancer_bp.route('/test-email-auth', methods=['GET', 'OPTIONS'])
# # @token_required
# # def test_email_auth():
# #     """Test email sending with auth"""
# #     # Handle OPTIONS request for CORS
# #     if request.method == 'OPTIONS':
# #         response = jsonify({'success': True})
# #         response.headers.add('Access-Control-Allow-Origin', 'http://localhost:3000')
# #         response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
# #         response.headers.add('Access-Control-Allow-Methods', 'GET,OPTIONS')
# #         response.headers.add('Access-Control-Allow-Credentials', 'true')
# #         return response
        
# #     try:
# #         print("=" * 50)
# #         print("TEST EMAIL AUTH ENDPOINT CALLED")
# #         print("=" * 50)
        
# #         user = User.find_by_id(request.user_id)
# #         if not user:
# #             return jsonify({'success': False, 'message': 'User not found'}), 404
        
# #         print(f"👤 User found: {user['email']}")
        
# #         if email_service:
# #             freelancer_name = f"{user['first_name']} {user['last_name']}"
# #             print(f"📧 Calling email_service.send_application_confirmation...")
            
# #             result = email_service.send_application_confirmation(
# #                 to_email=user['email'],
# #                 freelancer_name=freelancer_name,
# #                 job_title="Test Job",
# #                 company_name="Test Company",
# #                 user_id=user['id']
# #             )
            
# #             print(f"📧 Email service returned: {result}")
            
# #             response = jsonify({'success': True, 'message': 'Test email sent! Check your inbox.'})
# #             response.headers.add('Access-Control-Allow-Origin', 'http://localhost:3000')
# #             return response
# #         else:
# #             print(f"❌ Email service is None!")
# #             response = jsonify({'success': False, 'message': 'Email service not initialized'})
# #             response.headers.add('Access-Control-Allow-Origin', 'http://localhost:3000')
# #             return response, 500
# #     except Exception as e:
# #         print(f"❌ Test email failed: {str(e)}")
# #         traceback.print_exc()
# #         response = jsonify({'success': False, 'message': str(e)})
# #         response.headers.add('Access-Control-Allow-Origin', 'http://localhost:3000')
# #         return response, 500
    





# # # 2. Send email notification to recruiter
# # try:
# #     if email_service:
# #         print(f"📧 Email service object: {email_service}")
# #         print(f"📧 Email service mail attribute: {email_service.mail is not None}")
# #         print(f"📧 Preparing to send to recruiter: {recruiter['email']}")
        
# #         company_name = job.get('company_name', 'Company')
# #         result = email_service.send_application_submitted_notification(
# #             to_email=recruiter['email'],
# #             recruiter_name=recruiter_name,
# #             freelancer_name=freelancer_name,
# #             job_title=job['title'],
# #             job_id=job_id,
# #             application_id=application_id,
# #             user_id=recruiter['id']
# #         )
# #         print(f"📧 Email send result to recruiter: {result}")
        
# #         # Log manually if email_service doesn't log
# #         try:
# #             connection = get_db_connection()
# #             cursor = connection.cursor()
# #             cursor.execute("""
# #                 INSERT INTO email_logs 
# #                 (user_id, recipient_email, email_type, subject, status, sent_at)
# #                 VALUES (%s, %s, %s, %s, %s, NOW())
# #             """, (recruiter['id'], recruiter['email'], 'application_received', 
# #                   f"New Application: {freelancer_name} applied to {job['title']}", 'sent'))
# #             connection.commit()
# #             cursor.close()
# #             connection.close()
# #             print(f"📝 Manually logged email for recruiter")
# #         except Exception as log_error:
# #             print(f"⚠️ Manual log failed: {log_error}")
            
# #     else:
# #         print(f"❌ Email service is None!")
# # except Exception as e:
# #     print(f"⚠️ Failed to send email notification to recruiter: {e}")
# #     traceback.print_exc()




# # @freelancer_bp.route('/test-email-flask', methods=['GET'])
# # def test_email_flask():
# #     """Test email using Flask-Mail directly"""
# #     try:
# #         from flask_mail import Message
# #         from flask import current_app
        
# #         print("=" * 50)
# #         print("TEST EMAIL FLASK - DIRECT MAIL")
# #         print("=" * 50)
        
# #         # Get mail instance
# #         from flask_mail import Mail
# #         mail = Mail(current_app)
        
# #         # Create message
# #         msg = Message(
# #             subject="Flask-Mail Test from FreelanceHub",
# #             recipients=["star36522253@gmail.com"],
# #             body="If you received this, Flask-Mail is working correctly!",
# #             sender=current_app.config.get('FROM_EMAIL')
# #         )
        
# #         # Send email
# #         print(f"📧 Sending via Flask-Mail...")
# #         mail.send(msg)
# #         print(f"✅ Email sent successfully!")
        
# #         return jsonify({'success': True, 'message': 'Flask-Mail test email sent!'})
# #     except Exception as e:
# #         print(f"❌ Error: {str(e)}")
# #         traceback.print_exc()
# #         return jsonify({'success': False, 'message': str(e)}), 500

# # @freelancer_bp.route('/debug-email-status', methods=['GET'])
# # def debug_email_status():
# #     """Debug endpoint to check email service status"""
# #     try:
# #         from services.email_service import email_service as global_email_service
        
# #         status = {
# #             'email_service_exists': global_email_service is not None,
# #             'mail_configured': global_email_service.mail is not None if global_email_service else False,
# #             'has_mail_attribute': hasattr(global_email_service, 'mail') if global_email_service else False,
# #         }
        
# #         if global_email_service and global_email_service.mail:
# #             # Try to get mail config
# #             try:
# #                 status['mail_server'] = current_app.config.get('MAIL_SERVER')
# #                 status['mail_username'] = current_app.config.get('MAIL_USERNAME')
# #                 status['mail_port'] = current_app.config.get('MAIL_PORT')
# #                 status['mail_use_tls'] = current_app.config.get('MAIL_USE_TLS')
# #             except:
# #                 pass
        
# #         return jsonify({'success': True, 'status': status})
# #     except Exception as e:
# #         return jsonify({'success': False, 'error': str(e)}), 500




# from flask import Blueprint, request, jsonify, current_app
# from database.models import FreelancerProfile, Job, JobApplication, Notification, User
# from utils.auth_utils import token_required, freelancer_required
# from database.db_config import get_db_connection
# from datetime import datetime
# from services.email_instance import email_service
# import traceback

# freelancer_bp = Blueprint('freelancer', __name__, url_prefix='/api/freelancer')

# # ============== PROFILE ENDPOINTS ==============

# @freelancer_bp.route('/profile', methods=['GET'])
# @token_required
# @freelancer_required
# def get_profile():
#     """Get freelancer profile"""
#     try:
#         profile = FreelancerProfile.get_by_user_id(request.user_id)
        
#         if not profile:
#             return jsonify({
#                 'success': False,
#                 'message': 'Profile not found'
#             }), 404
        
#         return jsonify({
#             'success': True,
#             'profile': profile
#         }), 200
#     except Exception as e:
#         print(f"❌ Error in get_profile: {str(e)}")
#         traceback.print_exc()
#         return jsonify({
#             'success': False,
#             'message': f'Server error: {str(e)}'
#         }), 500

# @freelancer_bp.route('/profile', methods=['PUT'])
# @token_required
# @freelancer_required
# def update_profile():
#     """Update freelancer profile"""
#     try:
#         data = request.get_json()
        
#         if not data:
#             return jsonify({
#                 'success': False,
#                 'message': 'No data provided'
#             }), 400
        
#         profile = FreelancerProfile.update_profile(request.user_id, data)
        
#         if not profile:
#             return jsonify({
#                 'success': False,
#                 'message': 'Profile not found'
#             }), 404
        
#         return jsonify({
#             'success': True,
#             'message': 'Profile updated successfully',
#             'profile': profile
#         }), 200
#     except Exception as e:
#         print(f"❌ Error in update_profile: {str(e)}")
#         traceback.print_exc()
#         return jsonify({
#             'success': False,
#             'message': f'Server error: {str(e)}'
#         }), 500

# # ============== JOB SEARCH ENDPOINTS ==============

# @freelancer_bp.route('/jobs/search', methods=['GET'])
# @token_required
# @freelancer_required
# def search_jobs():
#     """Search for jobs with improved filtering"""
#     try:
#         # Get filter parameters
#         search = request.args.get('search', '')
#         experience_level = request.args.get('experience_level', '')
#         min_pay = request.args.get('min_pay', '')
#         max_pay = request.args.get('max_pay', '')
#         job_type = request.args.get('job_type', '')
#         is_remote = request.args.get('is_remote', '')
        
#         # Build filters dictionary (only include non-empty values)
#         filters = {}
#         if search and search.strip():
#             filters['search'] = search.strip()
#         if experience_level and experience_level.strip():
#             filters['experience_level'] = experience_level.strip()
#         if min_pay and min_pay.strip():
#             try:
#                 filters['min_pay'] = float(min_pay)
#             except ValueError:
#                 pass
#         if max_pay and max_pay.strip():
#             try:
#                 filters['max_pay'] = float(max_pay)
#             except ValueError:
#                 pass
#         if job_type and job_type.strip() and job_type != 'All Types':
#             filters['job_type'] = job_type.strip()
#         if is_remote and is_remote.lower() == 'true':
#             filters['is_remote'] = True
        
#         print(f"🔍 Search filters: {filters}")
        
#         jobs = Job.search_jobs(filters)
        
#         print(f"✅ Found {len(jobs)} jobs")
        
#         return jsonify({
#             'success': True,
#             'count': len(jobs),
#             'jobs': jobs
#         }), 200
        
#     except Exception as e:
#         print(f"❌ Error in search_jobs: {str(e)}")
#         traceback.print_exc()
#         return jsonify({
#             'success': False,
#             'message': f'Search failed: {str(e)}',
#             'jobs': []
#         }), 500

# @freelancer_bp.route('/jobs/<int:job_id>', methods=['GET'])
# @token_required
# @freelancer_required
# def get_job_details(job_id):
#     """Get job details by ID"""
#     try:
#         print(f"🔍 Fetching job details for ID: {job_id}")
#         job = Job.get_by_id(job_id)
        
#         if not job:
#             return jsonify({
#                 'success': False,
#                 'message': 'Job not found'
#             }), 404
        
#         return jsonify({
#             'success': True,
#             'job': job
#         }), 200
#     except Exception as e:
#         print(f"❌ Error in get_job_details: {str(e)}")
#         traceback.print_exc()
#         return jsonify({
#             'success': False,
#             'message': f'Server error: {str(e)}'
#         }), 500

# # ============== APPLICATION ENDPOINTS ==============

# @freelancer_bp.route('/jobs/<int:job_id>/apply', methods=['POST'])
# @token_required
# @freelancer_required
# def apply_for_job(job_id):
#     """Apply for a job with email notification"""
#     try:
#         data = request.get_json() or {}
        
#         print(f"📝 Freelancer {request.user_id} applying for job {job_id}")
#         print(f"📦 Application data: {data}")
        
#         # Validate required fields
#         if not data.get('cover_letter'):
#             return jsonify({
#                 'success': False,
#                 'message': 'Cover letter is required'
#             }), 400
        
#         # First check if job exists
#         job = Job.get_by_id(job_id)
#         if not job:
#             print(f"❌ Job {job_id} not found")
#             return jsonify({
#                 'success': False,
#                 'message': 'Job not found'
#             }), 404
            
#         print(f"✅ Job found: {job['title']}")
#         print(f"📧 Job details - Recruiter ID: {job['recruiter_id']}, Recruiter Email: {job.get('recruiter_email', 'N/A')}")
        
#         # Create application
#         application_id = JobApplication.create(
#             job_id=job_id,
#             freelancer_id=request.user_id,
#             application_data=data
#         )
        
#         if not application_id:
#             # Check if it's because of duplicate application
#             connection = get_db_connection()
#             cursor = connection.cursor()
#             cursor.execute("""
#                 SELECT id, status FROM job_applications 
#                 WHERE job_id = %s AND freelancer_id = %s
#             """, (job_id, request.user_id))
#             existing = cursor.fetchone()
#             cursor.close()
#             connection.close()
            
#             if existing:
#                 return jsonify({
#                     'success': False,
#                     'message': f'You have already applied for this job (Status: {existing["status"]})'
#                 }), 400
#             else:
#                 return jsonify({
#                     'success': False,
#                     'message': 'Failed to create application. Please try again.'
#                 }), 400
        
#         print(f"✅ Application created with ID: {application_id}")
        
#         # Get freelancer and recruiter info for notifications
#         freelancer = User.find_by_id(request.user_id)
#         recruiter = User.find_by_id(job['recruiter_id'])
        
#         print(f"👤 Freelancer: {freelancer['email'] if freelancer else 'Not found'}")
#         print(f"👤 Recruiter: {recruiter['email'] if recruiter else 'Not found'}")
        
#         if freelancer and recruiter:
#             freelancer_name = f"{freelancer['first_name']} {freelancer['last_name']}"
#             recruiter_name = f"{recruiter['first_name']} {recruiter['last_name']}"
            
#             # 1. Create in-app notification for recruiter
#             Notification.create(
#                 user_id=job['recruiter_id'],
#                 title='New Job Application',
#                 message=f'{freelancer_name} has applied for {job["title"]}',
#                 notification_type='application',
#                 related_application_id=application_id,
#                 related_job_id=job_id
#             )
#             print(f"✅ In-app notification created for recruiter {job['recruiter_id']}")
            
#             # 2. Send email notification to recruiter
#             try:
#                 if email_service and email_service.mail:
#                     print(f"📧 Email service exists, preparing to send to recruiter: {recruiter['email']}")
#                     print(f"📧 Email service mail object: {email_service.mail is not None}")
                    
#                     company_name = job.get('company_name', 'Company')
#                     result = email_service.send_application_submitted_notification(
#                         to_email=recruiter['email'],
#                         recruiter_name=recruiter_name,
#                         freelancer_name=freelancer_name,
#                         job_title=job['title'],
#                         job_id=job_id,
#                         application_id=application_id,
#                         user_id=recruiter['id']
#                     )
#                     print(f"📧 Email send result to recruiter: {result}")
                    
#                     # Manual log as backup
#                     try:
#                         connection = get_db_connection()
#                         cursor = connection.cursor()
#                         cursor.execute("""
#                             INSERT INTO email_logs 
#                             (user_id, recipient_email, email_type, subject, status, sent_at)
#                             VALUES (%s, %s, %s, %s, %s, NOW())
#                         """, (recruiter['id'], recruiter['email'], 'application_received', 
#                               f"New Application: {freelancer_name} applied to {job['title']}", 'sent'))
#                         connection.commit()
#                         cursor.close()
#                         connection.close()
#                         print(f"📝 Manually logged email for recruiter")
#                     except Exception as log_error:
#                         print(f"⚠️ Manual log failed: {log_error}")
#                 else:
#                     print(f"❌ Email service is None or mail not configured!")
#                     print(f"   email_service: {email_service}")
#                     if email_service:
#                         print(f"   mail attribute: {email_service.mail is not None}")
#             except Exception as e:
#                 print(f"⚠️ Failed to send email notification to recruiter: {e}")
#                 traceback.print_exc()
            
#             # 3. Send confirmation email to freelancer
#             try:
#                 if email_service and email_service.mail:
#                     print(f"📧 Preparing to send confirmation to freelancer: {freelancer['email']}")
#                     company_name = job.get('company_name', 'Company')
#                     result = email_service.send_application_confirmation(
#                         to_email=freelancer['email'],
#                         freelancer_name=freelancer_name,
#                         job_title=job['title'],
#                         company_name=company_name,
#                         user_id=freelancer['id']
#                     )
#                     print(f"📧 Email send result to freelancer: {result}")
#                 else:
#                     print(f"❌ Email service is None for freelancer confirmation!")
#             except Exception as e:
#                 print(f"⚠️ Failed to send confirmation email: {e}")
#                 traceback.print_exc()
#         else:
#             print(f"❌ Could not get freelancer or recruiter info")
        
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

# @freelancer_bp.route('/applications', methods=['GET'])
# @token_required
# @freelancer_required
# def get_applications():
#     """Get all applications by freelancer"""
#     try:
#         applications = JobApplication.get_by_freelancer(request.user_id)
        
#         return jsonify({
#             'success': True,
#             'count': len(applications),
#             'applications': applications
#         }), 200
#     except Exception as e:
#         print(f"❌ Error in get_applications: {str(e)}")
#         traceback.print_exc()
#         return jsonify({
#             'success': False,
#             'message': f'Server error: {str(e)}'
#         }), 500

# # ============== DASHBOARD ENDPOINT ==============

# @freelancer_bp.route('/dashboard', methods=['GET'])
# @token_required
# @freelancer_required
# def get_dashboard():
#     """Get freelancer dashboard data"""
#     try:
#         profile = FreelancerProfile.get_by_user_id(request.user_id)
#         applications = JobApplication.get_by_freelancer(request.user_id)
        
#         # Get recommended jobs based on skills
#         recommended_jobs = []
#         if profile and profile.get('skills'):
#             skill_names = [s['name'] for s in profile['skills']]
#             print(f"🎯 Freelancer skills: {skill_names}")
            
#             if skill_names:
#                 # Search for jobs with matching skills
#                 for skill in skill_names[:3]:
#                     jobs = Job.search_jobs({'search': skill})
#                     if jobs:
#                         print(f"Found {len(jobs)} jobs for skill: {skill}")
#                         recommended_jobs.extend(jobs[:2])
        
#         # Remove duplicates
#         seen = set()
#         unique_jobs = []
#         for job in recommended_jobs:
#             if job['id'] not in seen:
#                 seen.add(job['id'])
#                 unique_jobs.append(job)
        
#         print(f"📊 Recommended {len(unique_jobs)} unique jobs")
        
#         # Calculate profile completion percentage
#         profile_completion = 0
#         if profile:
#             fields = ['bio', 'hourly_rate', 'education', 'experience', 
#                      'github_url', 'linkedin_url', 'portfolio_url']
#             completed = sum(1 for field in fields if profile.get(field))
#             if profile.get('skills') and len(profile['skills']) > 0:
#                 completed += 1
#             if profile.get('tech_stacks') and len(profile['tech_stacks']) > 0:
#                 completed += 1
#             total_fields = len(fields) + 2
#             profile_completion = int((completed / total_fields) * 100)
        
#         stats = {
#             'total_applications': len(applications),
#             'pending_applications': sum(1 for a in applications if a['status'] == 'applied'),
#             'accepted_applications': sum(1 for a in applications if a['status'] == 'accepted'),
#             'rejected_applications': sum(1 for a in applications if a['status'] == 'rejected'),
#             'profile_completion': profile_completion
#         }
        
#         return jsonify({
#             'success': True,
#             'profile': profile,
#             'recent_applications': applications[:5],
#             'recommended_jobs': unique_jobs[:6],
#             'stats': stats
#         }), 200
        
#     except Exception as e:
#         print(f"❌ Error in get_dashboard: {str(e)}")
#         traceback.print_exc()
#         return jsonify({
#             'success': False,
#             'message': f'Server error: {str(e)}'
#         }), 500

# # ============== TEST EMAIL ENDPOINTS ==============
# # KEEP ONLY ONE VERSION OF EACH FUNCTION

# @freelancer_bp.route('/test-email-simple', methods=['GET'])
# def test_email_simple():
#     """Simple test endpoint for email - no auth required"""
#     try:
#         print("=" * 50)
#         print("TEST EMAIL SIMPLE ENDPOINT CALLED")
#         print("=" * 50)
        
#         from flask_mail import Message
#         from flask_mail import Mail
        
#         # Create a simple test message
#         msg = Message(
#             subject="Test Email from FreelanceHub",
#             recipients=["star36522253@gmail.com"],
#             body="This is a test email to verify SMTP configuration. If you received this, email is working!",
#             sender=current_app.config.get('FROM_EMAIL', 'noreply@freelancehub.com')
#         )
        
#         # Try to send
#         print(f"📧 Attempting to send test email to star36522253@gmail.com...")
#         print(f"📧 Mail server: {current_app.config.get('MAIL_SERVER')}")
#         print(f"📧 Mail username: {current_app.config.get('MAIL_USERNAME')}")
        
#         mail = Mail(current_app)
#         mail.send(msg)
#         print(f"✅ Test email sent successfully!")
        
#         return jsonify({'success': True, 'message': 'Test email sent! Check your inbox.'})
#     except Exception as e:
#         print(f"❌ Test email failed: {str(e)}")
#         traceback.print_exc()
#         return jsonify({'success': False, 'message': str(e)}), 500

# @freelancer_bp.route('/test-email-auth', methods=['GET'])
# @token_required
# def test_email_auth():
#     """Test email sending with auth"""
#     try:
#         print("=" * 50)
#         print("TEST EMAIL AUTH ENDPOINT CALLED")
#         print("=" * 50)
        
#         user = User.find_by_id(request.user_id)
#         if not user:
#             return jsonify({'success': False, 'message': 'User not found'}), 404
        
#         print(f"👤 User found: {user['email']}")
        
#         if email_service:
#             freelancer_name = f"{user['first_name']} {user['last_name']}"
#             print(f"📧 Calling email_service.send_application_confirmation...")
            
#             result = email_service.send_application_confirmation(
#                 to_email=user['email'],
#                 freelancer_name=freelancer_name,
#                 job_title="Test Job",
#                 company_name="Test Company",
#                 user_id=user['id']
#             )
            
#             print(f"📧 Email service returned: {result}")
            
#             return jsonify({'success': True, 'message': 'Test email sent! Check your inbox.'})
#         else:
#             print(f"❌ Email service is None!")
#             return jsonify({'success': False, 'message': 'Email service not initialized'}), 500
#     except Exception as e:
#         print(f"❌ Test email failed: {str(e)}")
#         traceback.print_exc()
#         return jsonify({'success': False, 'message': str(e)}), 500

# @freelancer_bp.route('/test-email-flask', methods=['GET'])
# def test_email_flask():
#     """Test email using Flask-Mail directly"""
#     try:
#         from flask_mail import Message
#         from flask_mail import Mail
        
#         print("=" * 50)
#         print("TEST EMAIL FLASK - DIRECT MAIL")
#         print("=" * 50)
        
#         # Get mail instance
#         mail = Mail(current_app)
        
#         # Create message
#         msg = Message(
#             subject="Flask-Mail Test from FreelanceHub",
#             recipients=["star36522253@gmail.com"],
#             body="If you received this, Flask-Mail is working correctly!",
#             sender=current_app.config.get('FROM_EMAIL')
#         )
        
#         # Send email
#         print(f"📧 Sending via Flask-Mail...")
#         mail.send(msg)
#         print(f"✅ Email sent successfully!")
        
#         return jsonify({'success': True, 'message': 'Flask-Mail test email sent!'})
#     except Exception as e:
#         print(f"❌ Error: {str(e)}")
#         traceback.print_exc()
#         return jsonify({'success': False, 'message': str(e)}), 500

# @freelancer_bp.route('/debug-email-status', methods=['GET'])
# def debug_email_status():
#     """Debug endpoint to check email service status"""
#     try:
#         status = {
#             'email_service_exists': email_service is not None,
#             'mail_configured': email_service.mail is not None if email_service else False,
#         }
        
#         if email_service and email_service.mail:
#             # Try to get mail config
#             try:
#                 status['mail_server'] = current_app.config.get('MAIL_SERVER')
#                 status['mail_username'] = current_app.config.get('MAIL_USERNAME')
#                 status['mail_port'] = current_app.config.get('MAIL_PORT')
#                 status['mail_use_tls'] = current_app.config.get('MAIL_USE_TLS')
#             except:
#                 pass
        
#         return jsonify({'success': True, 'status': status})
#     except Exception as e:
#         return jsonify({'success': False, 'error': str(e)}), 500



from flask import Blueprint, request, jsonify, current_app
from database.models import FreelancerProfile, Job, JobApplication, Notification, User
from utils.auth_utils import token_required, freelancer_required
from database.db_config import get_db_connection
from datetime import datetime
from services.email_instance import email_service
import traceback

freelancer_bp = Blueprint('freelancer', __name__, url_prefix='/api/freelancer')

# ============== PROFILE ENDPOINTS ==============

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
        print(f"❌ Error in get_profile: {str(e)}")
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
        print(f"❌ Error in update_profile: {str(e)}")
        traceback.print_exc()
        return jsonify({
            'success': False,
            'message': f'Server error: {str(e)}'
        }), 500

# ============== JOB SEARCH ENDPOINTS ==============

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
        
        print(f"🔍 Search filters: {filters}")
        
        jobs = Job.search_jobs(filters)
        
        print(f"✅ Found {len(jobs)} jobs")
        
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

# ============== APPLICATION ENDPOINTS ==============

@freelancer_bp.route('/jobs/<int:job_id>/apply', methods=['POST'])
@token_required
@freelancer_required
def apply_for_job(job_id):
    """Apply for a job with email notification"""
    try:
        data = request.get_json() or {}
        
        print(f"📝 Freelancer {request.user_id} applying for job {job_id}")
        print(f"📦 Application data: {data}")
        
        # Validate required fields
        if not data.get('cover_letter'):
            return jsonify({
                'success': False,
                'message': 'Cover letter is required'
            }), 400
        
        # First check if job exists
        job = Job.get_by_id(job_id)
        if not job:
            print(f"❌ Job {job_id} not found")
            return jsonify({
                'success': False,
                'message': 'Job not found'
            }), 404
            
        print(f"✅ Job found: {job['title']}")
        print(f"📧 Job details - Recruiter ID: {job['recruiter_id']}, Recruiter Email: {job.get('recruiter_email', 'N/A')}")
        
        # Create application
        application_id = JobApplication.create(
            job_id=job_id,
            freelancer_id=request.user_id,
            application_data=data
        )
        
        if not application_id:
            # ... existing duplicate check code ...
            pass
        
        print(f"✅ Application created with ID: {application_id}")
        
        # Get freelancer and recruiter info for notifications
        freelancer = User.find_by_id(request.user_id)
        recruiter = User.find_by_id(job['recruiter_id'])
        
        print(f"👤 Freelancer: {freelancer['email'] if freelancer else 'Not found'}")
        print(f"👤 Recruiter: {recruiter['email'] if recruiter else 'Not found'}")
        
        if freelancer and recruiter:
            freelancer_name = f"{freelancer['first_name']} {freelancer['last_name']}"
            recruiter_name = f"{recruiter['first_name']} {recruiter['last_name']}"
            
            # 1. Create in-app notification for recruiter
            Notification.create(
                user_id=job['recruiter_id'],
                title='New Job Application',
                message=f'{freelancer_name} has applied for {job["title"]}',
                notification_type='application',
                related_application_id=application_id,
                related_job_id=job_id
            )
            print(f"✅ In-app notification created for recruiter {job['recruiter_id']}")
            
            # 2. Send email notification to recruiter
            try:
                if email_service and email_service.mail:
                    print(f"📧 Email service exists, preparing to send to recruiter: {recruiter['email']}")
                    print(f"📧 Email service mail object: {email_service.mail is not None}")
                    
                    # TEST: Try sending a simple email first to isolate the issue
                    try:
                        from flask_mail import Message
                        test_msg = Message(
                            subject="Test from Application Flow",
                            recipients=[recruiter['email']],
                            body=f"This is a test to verify email sending in application flow. Application ID: {application_id}",
                            sender=current_app.config.get('FROM_EMAIL')
                        )
                        email_service.mail.send(test_msg)
                        print(f"✅ SIMPLE TEST EMAIL SENT SUCCESSFULLY!")
                    except Exception as test_error:
                        print(f"❌ SIMPLE TEST EMAIL FAILED: {test_error}")
                        traceback.print_exc()
                    
                    # Now try the actual application email
                    company_name = job.get('company_name', 'Company')
                    print(f"📧 Calling send_application_submitted_notification with:")
                    print(f"   - to_email: {recruiter['email']}")
                    print(f"   - recruiter_name: {recruiter_name}")
                    print(f"   - freelancer_name: {freelancer_name}")
                    print(f"   - job_title: {job['title']}")
                    print(f"   - job_id: {job_id}")
                    print(f"   - application_id: {application_id}")
                    print(f"   - user_id: {recruiter['id']}")
                    
                    result = email_service.send_application_submitted_notification(
                        to_email=recruiter['email'],
                        recruiter_name=recruiter_name,
                        freelancer_name=freelancer_name,
                        job_title=job['title'],
                        job_id=job_id,
                        application_id=application_id,
                        user_id=recruiter['id']
                    )
                    print(f"📧 Email send result to recruiter: {result}")
                    
                    # Manual log as backup
                    try:
                        connection = get_db_connection()
                        cursor = connection.cursor()
                        cursor.execute("""
                            INSERT INTO email_logs 
                            (user_id, recipient_email, email_type, subject, status, sent_at)
                            VALUES (%s, %s, %s, %s, %s, NOW())
                        """, (recruiter['id'], recruiter['email'], 'application_received', 
                              f"New Application: {freelancer_name} applied to {job['title']}", 'sent'))
                        connection.commit()
                        cursor.close()
                        connection.close()
                        print(f"📝 Manually logged email for recruiter")
                    except Exception as log_error:
                        print(f"⚠️ Manual log failed: {log_error}")
                else:
                    print(f"❌ Email service is None or mail not configured!")
                    print(f"   email_service: {email_service}")
                    if email_service:
                        print(f"   mail attribute: {email_service.mail is not None}")
            except Exception as e:
                print(f"⚠️ Failed to send email notification to recruiter: {e}")
                traceback.print_exc()
            
            # 3. Send confirmation email to freelancer
            try:
                if email_service and email_service.mail:
                    print(f"📧 Preparing to send confirmation to freelancer: {freelancer['email']}")
                    company_name = job.get('company_name', 'Company')
                    result = email_service.send_application_confirmation(
                        to_email=freelancer['email'],
                        freelancer_name=freelancer_name,
                        job_title=job['title'],
                        company_name=company_name,
                        user_id=freelancer['id']
                    )
                    print(f"📧 Email send result to freelancer: {result}")
                else:
                    print(f"❌ Email service is None for freelancer confirmation!")
            except Exception as e:
                print(f"⚠️ Failed to send confirmation email: {e}")
                traceback.print_exc()
        else:
            print(f"❌ Could not get freelancer or recruiter info")
        
        return jsonify({
            'success': True,
            'message': 'Application submitted successfully! The recruiter has been notified.',
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

# ============== DASHBOARD ENDPOINT ==============

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
                for skill in skill_names[:3]:
                    jobs = Job.search_jobs({'search': skill})
                    if jobs:
                        print(f"Found {len(jobs)} jobs for skill: {skill}")
                        recommended_jobs.extend(jobs[:2])
        
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

# ============== TEST EMAIL ENDPOINTS ==============
# KEEP ONLY ONE VERSION OF EACH FUNCTION

@freelancer_bp.route('/test-email-simple', methods=['GET'])
def test_email_simple():
    """Simple test endpoint for email - no auth required"""
    try:
        print("=" * 50)
        print("TEST EMAIL SIMPLE ENDPOINT CALLED")
        print("=" * 50)
        
        from flask_mail import Message
        from flask_mail import Mail
        
        # Create a simple test message
        msg = Message(
            subject="Test Email from FreelanceHub",
            recipients=["star36522253@gmail.com"],
            body="This is a test email to verify SMTP configuration. If you received this, email is working!",
            sender=current_app.config.get('FROM_EMAIL', 'noreply@freelancehub.com')
        )
        
        # Try to send
        print(f"📧 Attempting to send test email to star36522253@gmail.com...")
        print(f"📧 Mail server: {current_app.config.get('MAIL_SERVER')}")
        print(f"📧 Mail username: {current_app.config.get('MAIL_USERNAME')}")
        
        mail = Mail(current_app)
        mail.send(msg)
        print(f"✅ Test email sent successfully!")
        
        return jsonify({'success': True, 'message': 'Test email sent! Check your inbox.'})
    except Exception as e:
        print(f"❌ Test email failed: {str(e)}")
        traceback.print_exc()
        return jsonify({'success': False, 'message': str(e)}), 500

@freelancer_bp.route('/test-email-auth', methods=['GET'])
@token_required
def test_email_auth():
    """Test email sending with auth"""
    try:
        print("=" * 50)
        print("TEST EMAIL AUTH ENDPOINT CALLED")
        print("=" * 50)
        
        user = User.find_by_id(request.user_id)
        if not user:
            return jsonify({'success': False, 'message': 'User not found'}), 404
        
        print(f"👤 User found: {user['email']}")
        
        if email_service:
            freelancer_name = f"{user['first_name']} {user['last_name']}"
            print(f"📧 Calling email_service.send_application_confirmation...")
            
            result = email_service.send_application_confirmation(
                to_email=user['email'],
                freelancer_name=freelancer_name,
                job_title="Test Job",
                company_name="Test Company",
                user_id=user['id']
            )
            
            print(f"📧 Email service returned: {result}")
            
            return jsonify({'success': True, 'message': 'Test email sent! Check your inbox.'})
        else:
            print(f"❌ Email service is None!")
            return jsonify({'success': False, 'message': 'Email service not initialized'}), 500
    except Exception as e:
        print(f"❌ Test email failed: {str(e)}")
        traceback.print_exc()
        return jsonify({'success': False, 'message': str(e)}), 500

@freelancer_bp.route('/test-email-flask', methods=['GET'])
def test_email_flask():
    """Test email using Flask-Mail directly"""
    try:
        from flask_mail import Message
        from flask_mail import Mail
        
        print("=" * 50)
        print("TEST EMAIL FLASK - DIRECT MAIL")
        print("=" * 50)
        
        # Get mail instance
        mail = Mail(current_app)
        
        # Create message
        msg = Message(
            subject="Flask-Mail Test from FreelanceHub",
            recipients=["star36522253@gmail.com"],
            body="If you received this, Flask-Mail is working correctly!",
            sender=current_app.config.get('FROM_EMAIL')
        )
        
        # Send email
        print(f"📧 Sending via Flask-Mail...")
        mail.send(msg)
        print(f"✅ Email sent successfully!")
        
        return jsonify({'success': True, 'message': 'Flask-Mail test email sent!'})
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        traceback.print_exc()
        return jsonify({'success': False, 'message': str(e)}), 500

@freelancer_bp.route('/debug-email-status', methods=['GET'])
def debug_email_status():
    """Debug endpoint to check email service status"""
    try:
        status = {
            'email_service_exists': email_service is not None,
            'mail_configured': email_service.mail is not None if email_service else False,
        }
        
        if email_service and email_service.mail:
            # Try to get mail config
            try:
                status['mail_server'] = current_app.config.get('MAIL_SERVER')
                status['mail_username'] = current_app.config.get('MAIL_USERNAME')
                status['mail_port'] = current_app.config.get('MAIL_PORT')
                status['mail_use_tls'] = current_app.config.get('MAIL_USE_TLS')
            except:
                pass
        
        return jsonify({'success': True, 'status': status})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500
    
@freelancer_bp.route('/test-email-simple', methods=['GET'])
def test_email_simple():
    try:
        from flask_mail import Message

        msg = Message(
            subject="FreelanceHub Email Test",
            recipients=["star36522253@gmail.com"],
            body="SMTP is working correctly!",
            sender=current_app.config.get('MAIL_USERNAME')
        )

        email_service.mail.send(msg)

        return jsonify({
            "success": True,
            "message": "Email sent successfully"
        })

    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500