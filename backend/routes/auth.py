# routes/auth.py (Enhanced with emails)

from flask import Blueprint, current_app, request, jsonify
from itsdangerous import URLSafeTimedSerializer
from models import db, User
from services.email_service import EmailService
from flask_mail import Mail
import logging
from datetime import datetime, timedelta
import jwt

auth_bp = Blueprint('auth', __name__)
mail = Mail()
email_service = EmailService(mail)

def generate_verification_token(email):
    serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    return serializer.dumps(email, salt='email-verification')

def verify_token(token, expiration=86400):
    serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    try:
        email = serializer.loads(token, salt='email-verification', max_age=expiration)
        return email
    except:
        return None

@auth_bp.route('/register', methods=['POST'])
def register():
    try:
        data = request.get_json()
        
        # Check if user exists
        if User.query.filter_by(email=data['email']).first():
            return jsonify({'success': False, 'message': 'Email already registered'}), 400
        
        # Create user (unverified)
        user = User(
            username=data['username'],
            email=data['email'],
            first_name=data.get('first_name', ''),
            last_name=data.get('last_name', ''),
            role=data.get('role', 'freelancer'),
            is_verified=False
        )
        user.set_password(data['password'])
        
        db.session.add(user)
        db.session.commit()
        
        # Generate verification token
        token = generate_verification_token(user.email)
        verification_link = f"{current_app.config['BASE_URL']}/verify-email/{token}"
        
        # Send verification email
        email_service.send_email(
            to_email=user.email,
            subject="Verify Your Email - FreelanceHub",
            template='verify_email',
            name=user.first_name or user.username,
            verification_link=verification_link
        )
        
        # Generate JWT
        jwt_token = jwt.encode(
            {'user_id': user.id, 'email': user.email},
            current_app.config['JWT_SECRET_KEY'],
            algorithm='HS256'
        )
        
        return jsonify({
            'success': True,
            'message': 'Registration successful. Please check your email for verification.',
            'token': jwt_token,
            'user': user.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        logging.error(f"Registration error: {str(e)}")
        return jsonify({'success': False, 'message': 'Registration failed'}), 500

@auth_bp.route('/verify-email/<token>', methods=['GET'])
def verify_email(token):
    try:
        email = verify_token(token)
        
        if not email:
            return jsonify({
                'success': False,
                'message': 'Invalid or expired verification link'
            }), 400
        
        user = User.query.filter_by(email=email).first()
        
        if not user:
            return jsonify({'success': False, 'message': 'User not found'}), 404
        
        if user.is_verified:
            return jsonify({'success': True, 'message': 'Email already verified'})
        
        # Mark as verified
        user.is_verified = True
        user.verified_at = datetime.utcnow()
        db.session.commit()
        
        # Send welcome email
        email_service.send_email(
            to_email=user.email,
            subject="Welcome to FreelanceHub! 🎉",
            template='welcome',
            name=user.first_name or user.username
        )
        
        return jsonify({
            'success': True,
            'message': 'Email verified successfully'
        })
        
    except Exception as e:
        logging.error(f"Verification error: {str(e)}")
        return jsonify({'success': False, 'message': 'Server error'}), 500

@auth_bp.route('/resend-verification', methods=['POST'])
def resend_verification():
    try:
        user_id = get_current_user_id()  # Get from auth token
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({'success': False, 'message': 'User not found'}), 404
        
        if user.is_verified:
            return jsonify({'success': False, 'message': 'Email already verified'}), 400
        
        # Generate new token
        token = generate_verification_token(user.email)
        verification_link = f"{current_app.config['BASE_URL']}/verify-email/{token}"
        
        # Send verification email
        email_service.send_email(
            to_email=user.email,
            subject="Verify Your Email - FreelanceHub",
            template='verify_email',
            name=user.first_name or user.username,
            verification_link=verification_link
        )
        
        return jsonify({
            'success': True,
            'message': 'Verification email resent successfully'
        })
        
    except Exception as e:
        logging.error(f"Resend error: {str(e)}")
        return jsonify({'success': False, 'message': 'Server error'}), 500

@auth_bp.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        user = User.query.filter_by(email=data['email']).first()
        
        if not user or not user.check_password(data['password']):
            return jsonify({'success': False, 'message': 'Invalid credentials'}), 401
        
        # Generate JWT
        token = jwt.encode(
            {'user_id': user.id, 'email': user.email},
            current_app.config['JWT_SECRET_KEY'],
            algorithm='HS256'
        )
        
        response = {
            'success': True,
            'token': token,
            'user': user.to_dict()
        }
        
        # If not verified, add warning
        if not user.is_verified:
            response['warning'] = 'Please verify your email address'
            response['needs_verification'] = True
        
        return jsonify(response)
        
    except Exception as e:
        logging.error(f"Login error: {str(e)}")
        return jsonify({'success': False, 'message': 'Login failed'}), 500