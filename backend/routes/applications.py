# routes/applications.py (Enhanced with emails)

from flask import Blueprint, request, jsonify
from models import db, User, Job, Application, Notification
from services.email_service import EmailService
from flask_mail import Mail
import logging

applications_bp = Blueprint('applications', __name__)
mail = Mail()
email_service = EmailService(mail)

@applications_bp.route('/apply', methods=['POST'])
def apply_for_job():
    try:
        data = request.get_json()
        freelancer_id = get_current_user_id()  # Get from auth token
        job_id = data.get('job_id')
        
        # Get job and users
        job = Job.query.get(job_id)
        freelancer = User.query.get(freelancer_id)
        recruiter = User.query.get(job.recruiter_id)
        
        # Create application
        application = Application(
            job_id=job_id,
            freelancer_id=freelancer_id,
            status='pending',
            cover_letter=data.get('cover_letter'),
            proposed_rate=data.get('proposed_rate')
        )
        
        db.session.add(application)
        db.session.commit()
        
        # 1. IN-APP NOTIFICATION for recruiter
        notification = Notification(
            user_id=recruiter.id,
            type='application_received',
            title='New Job Application',
            message=f'{freelancer.first_name or freelancer.username} applied for "{job.title}"',
            data={
                'job_id': job.id,
                'job_title': job.title,
                'application_id': application.id,
                'freelancer_name': f"{freelancer.first_name} {freelancer.last_name}".strip() or freelancer.username,
                'proposed_rate': data.get('proposed_rate')
            }
        )
        db.session.add(notification)
        db.session.commit()
        
        # 2. EMAIL NOTIFICATION for recruiter
        email_service.send_email(
            to_email=recruiter.email,
            subject=f"New Application: {job.title}",
            template='application_received',
            job_title=job.title,
            freelancer_name=freelancer.first_name or freelancer.username,
            proposed_rate=data.get('proposed_rate')
        )
        
        # 3. CONFIRMATION EMAIL for freelancer
        email_service.send_email(
            to_email=freelancer.email,
            subject="Application Submitted Successfully",
            template='welcome',  # You can create a confirmation template
            name=freelancer.first_name or freelancer.username,
            job_title=job.title
        )
        
        return jsonify({
            'success': True,
            'message': 'Application submitted. Recruiter has been notified.',
            'application': application.to_dict()
        })
        
    except Exception as e:
        db.session.rollback()
        logging.error(f"Error in application: {str(e)}")
        return jsonify({'success': False, 'message': 'Server error'}), 500

@applications_bp.route('/<int:application_id>/status', methods=['PUT'])
def update_application_status(application_id):
    try:
        data = request.get_json()
        new_status = data.get('status')  # 'accepted' or 'rejected'
        recruiter_id = get_current_user_id()
        
        # Get application with details
        application = Application.query.get_or_404(application_id)
        job = Job.query.get(application.job_id)
        freelancer = User.query.get(application.freelancer_id)
        recruiter = User.query.get(recruiter_id)
        
        # Update status
        application.status = new_status
        db.session.commit()
        
        # IN-APP and EMAIL notifications based on status
        if new_status == 'accepted':
            # In-app for freelancer
            notification = Notification(
                user_id=freelancer.id,
                type='application_accepted',
                title='Application Accepted! 🎉',
                message=f'Congratulations! Your application for "{job.title}" was accepted',
                data={'job_id': job.id, 'job_title': job.title}
            )
            db.session.add(notification)
            
            # Email for freelancer
            email_service.send_email(
                to_email=freelancer.email,
                subject=f"Application Accepted: {job.title}",
                template='application_accepted',
                job_title=job.title,
                recruiter_name=recruiter.first_name or recruiter.username
            )
            
        elif new_status == 'rejected':
            # In-app for freelancer
            notification = Notification(
                user_id=freelancer.id,
                type='application_rejected',
                title='Application Update',
                message=f'Your application for "{job.title}" was not selected',
                data={'job_id': job.id, 'job_title': job.title}
            )
            db.session.add(notification)
            
            # Email for freelancer
            email_service.send_email(
                to_email=freelancer.email,
                subject=f"Application Update: {job.title}",
                template='application_rejected',
                job_title=job.title
            )
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': f'Application {new_status}. Freelancer has been notified via email and in-app.'
        })
        
    except Exception as e:
        db.session.rollback()
        logging.error(f"Error updating status: {str(e)}")
        return jsonify({'success': False, 'message': 'Server error'}), 500