# # # # from flask import Blueprint, request, jsonify
# # # # from database.models import User
# # # # from services.email_service import EmailService
# # # # from utils.auth_utils import (
# # # #     validate_email, validate_password, generate_token, decode_token,
# # # #     token_required, hash_password, check_password
# # # # )
# # # # from datetime import timedelta
# # # # import os

# # # # auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')

# # # # @auth_bp.route('/register', methods=['POST'])
# # # # def register():
# # # #     """User registration endpoint with email verification"""
# # # #     try:
# # # #         data = request.get_json()
        
# # # #         # Validate required fields
# # # #         required_fields = ['username', 'email', 'password', 'first_name', 'last_name', 'user_type']
# # # #         for field in required_fields:
# # # #             if field not in data or not data[field]:
# # # #                 return jsonify({
# # # #                     'success': False,
# # # #                     'message': f'{field} is required'
# # # #                 }), 400
        
# # # #         # Validate email
# # # #         if not validate_email(data['email']):
# # # #             return jsonify({
# # # #                 'success': False,
# # # #                 'message': 'Invalid email format'
# # # #             }), 400
        
# # # #         # Validate password strength
# # # #         is_valid, message = validate_password(data['password'])
# # # #         if not is_valid:
# # # #             return jsonify({
# # # #                 'success': False,
# # # #                 'message': message
# # # #             }), 400
        
# # # #         # Validate user type
# # # #         if data['user_type'] not in ['freelancer', 'recruiter']:
# # # #             return jsonify({
# # # #                 'success': False,
# # # #                 'message': 'Invalid user type'
# # # #             }), 400
        
# # # #         # Check if user exists
# # # #         existing_user = User.find_by_email(data['email'])
# # # #         if existing_user:
# # # #             return jsonify({
# # # #                 'success': False,
# # # #                 'message': 'Email already registered'
# # # #             }), 409
        
# # # #         # Create user
# # # #         user_id = User.create(
# # # #             username=data['username'],
# # # #             email=data['email'],
# # # #             password=data['password'],
# # # #             first_name=data['first_name'],
# # # #             last_name=data['last_name'],
# # # #             user_type=data['user_type']
# # # #         )
        
# # # #         # Send verification email
# # # #         EmailService.send_verification_email(user_id)
        
# # # #         # Send welcome email
# # # #         EmailService.send_welcome_email(user_id)
        
# # # #         # Generate tokens
# # # #         access_token = generate_token(
# # # #             user_id, 
# # # #             data['user_type'],
# # # #             timedelta(hours=1)
# # # #         )
# # # #         refresh_token = generate_token(
# # # #             user_id,
# # # #             data['user_type'],
# # # #             timedelta(days=7)
# # # #         )
        
# # # #         # Get user data
# # # #         user = User.find_by_id(user_id)
# # # #         if user and 'password_hash' in user:
# # # #             del user['password_hash']
        
# # # #         return jsonify({
# # # #             'success': True,
# # # #             'message': 'Registration successful! Please check your email to verify your account.',
# # # #             'access_token': access_token,
# # # #             'refresh_token': refresh_token,
# # # #             'user': user
# # # #         }), 201
        
# # # #     except Exception as e:
# # # #         return jsonify({
# # # #             'success': False,
# # # #             'message': f'Registration failed: {str(e)}'
# # # #         }), 500

# # # # @auth_bp.route('/verify-email/<token>', methods=['GET'])
# # # # def verify_email(token):
# # # #     """Verify email address"""
# # # #     try:
# # # #         payload = decode_token(token)
# # # #         if not payload or payload.get('type') != 'email_verification':
# # # #             return jsonify({
# # # #                 'success': False,
# # # #                 'message': 'Invalid or expired verification token'
# # # #             }), 400
        
# # # #         user_id = payload['user_id']
        
# # # #         # Update user as verified
# # # #         connection = get_db_connection()
# # # #         cursor = connection.cursor()
# # # #         cursor.execute("""
# # # #             UPDATE users SET is_verified = TRUE, email_verified_at = NOW()
# # # #             WHERE id = %s
# # # #         """, (user_id,))
# # # #         connection.commit()
# # # #         cursor.close()
# # # #         connection.close()
        
# # # #         return jsonify({
# # # #             'success': True,
# # # #             'message': 'Email verified successfully! You can now log in.'
# # # #         }), 200
        
# # # #     except Exception as e:
# # # #         return jsonify({
# # # #             'success': False,
# # # #             'message': f'Verification failed: {str(e)}'
# # # #         }), 500

# # # # @auth_bp.route('/resend-verification', methods=['POST'])
# # # # @token_required
# # # # def resend_verification():
# # # #     """Resend verification email"""
# # # #     try:
# # # #         user = User.find_by_id(request.user_id)
# # # #         if not user:
# # # #             return jsonify({
# # # #                 'success': False,
# # # #                 'message': 'User not found'
# # # #             }), 404
        
# # # #         if user.get('is_verified'):
# # # #             return jsonify({
# # # #                 'success': False,
# # # #                 'message': 'Email already verified'
# # # #             }), 400
        
# # # #         EmailService.send_verification_email(request.user_id)
        
# # # #         return jsonify({
# # # #             'success': True,
# # # #             'message': 'Verification email sent successfully'
# # # #         }), 200
        
# # # #     except Exception as e:
# # # #         return jsonify({
# # # #             'success': False,
# # # #             'message': f'Failed to send verification email: {str(e)}'
# # # #         }), 500

# # # # @auth_bp.route('/forgot-password', methods=['POST'])
# # # # def forgot_password():
# # # #     """Send password reset email"""
# # # #     try:
# # # #         data = request.get_json()
        
# # # #         if 'email' not in data:
# # # #             return jsonify({
# # # #                 'success': False,
# # # #                 'message': 'Email is required'
# # # #             }), 400
        
# # # #         user = User.find_by_email(data['email'])
# # # #         if not user:
# # # #             return jsonify({
# # # #                 'success': False,
# # # #                 'message': 'If this email exists, a reset link has been sent'
# # # #             }), 200  # Don't reveal if email exists
        
# # # #         EmailService.send_password_reset_email(user['id'])
        
# # # #         return jsonify({
# # # #             'success': True,
# # # #             'message': 'If this email exists, a reset link has been sent'
# # # #         }), 200
        
# # # #     except Exception as e:
# # # #         return jsonify({
# # # #             'success': False,
# # # #             'message': f'Failed to send reset email: {str(e)}'
# # # #         }), 500

# # # # @auth_bp.route('/reset-password/<token>', methods=['POST'])
# # # # def reset_password(token):
# # # #     """Reset password using token"""
# # # #     try:
# # # #         payload = decode_token(token)
# # # #         if not payload or payload.get('type') != 'password_reset':
# # # #             return jsonify({
# # # #                 'success': False,
# # # #                 'message': 'Invalid or expired reset token'
# # # #             }), 400
        
# # # #         data = request.get_json()
        
# # # #         if 'password' not in data:
# # # #             return jsonify({
# # # #                 'success': False,
# # # #                 'message': 'New password is required'
# # # #             }), 400
        
# # # #         # Validate password strength
# # # #         is_valid, message = validate_password(data['password'])
# # # #         if not is_valid:
# # # #             return jsonify({
# # # #                 'success': False,
# # # #                 'message': message
# # # #             }), 400
        
# # # #         # Update password
# # # #         password_hash = hash_password(data['password'])
        
# # # #         connection = get_db_connection()
# # # #         cursor = connection.cursor()
# # # #         cursor.execute("""
# # # #             UPDATE users SET password_hash = %s, updated_at = NOW()
# # # #             WHERE id = %s
# # # #         """, (password_hash, payload['user_id']))
# # # #         connection.commit()
# # # #         cursor.close()
# # # #         connection.close()
        
# # # #         return jsonify({
# # # #             'success': True,
# # # #             'message': 'Password reset successfully! You can now log in with your new password.'
# # # #         }), 200
        
# # # #     except Exception as e:
# # # #         return jsonify({
# # # #             'success': False,
# # # #             'message': f'Password reset failed: {str(e)}'
# # # #         }), 500



# # # from flask import Blueprint, request, jsonify, current_app
# # # from flask_mail import Message
# # # from itsdangerous import URLSafeTimedSerializer, SignatureExpired, BadSignature
# # # from database.models import User
# # # from utils.auth_utils import validate_email, validate_password, generate_token, decode_token
# # # from datetime import datetime, timedelta
# # # import traceback

# # # auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')

# # # def get_mail():
# # #     return current_app.extensions['mail']

# # # def generate_verification_token(email):
# # #     s = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
# # #     return s.dumps(email, salt='email-verification-salt')

# # # def verify_verification_token(token, expiration=86400):
# # #     s = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
# # #     try:
# # #         email = s.loads(token, salt='email-verification-salt', max_age=expiration)
# # #         return email
# # #     except (SignatureExpired, BadSignature):
# # #         return None

# # # def send_verification_email(user):
# # #     try:
# # #         token = generate_verification_token(user['email'])
# # #         link = f"{current_app.config['BASE_URL']}/verify-email/{token}"
# # #         User.set_verification_token(user['id'], token)

# # #         html = f"""<!DOCTYPE html>
# # #         <html><body>
# # #         <h2>Hello {user['first_name']}!</h2>
# # #         <p>Please verify your email: <a href="{link}">Verify Email</a></p>
# # #         </body></html>"""

# # #         msg = Message(
# # #             subject="Verify Your Email - FreelanceHub",
# # #             recipients=[user['email']],
# # #             html=html,
# # #             sender=current_app.config.get('FROM_EMAIL')
# # #         )
# # #         mail = get_mail()
# # #         mail.send(msg)
# # #         return True
# # #     except Exception as e:
# # #         print(f"❌ Email error: {e}")
# # #         traceback.print_exc()
# # #         return False

# # # @auth_bp.route('/register', methods=['POST'])
# # # def register():
# # #     try:
# # #         data = request.get_json()
# # #         print(f"📝 Registration attempt: {data.get('email')}")

# # #         required = ['email', 'password', 'first_name', 'last_name', 'username', 'user_type']
# # #         for f in required:
# # #             if f not in data:
# # #                 return jsonify({'success': False, 'message': f'{f} is required'}), 400

# # #         if not validate_email(data['email']):
# # #             return jsonify({'success': False, 'message': 'Invalid email format'}), 400

# # #         valid, msg = validate_password(data['password'])
# # #         if not valid:
# # #             return jsonify({'success': False, 'message': msg}), 400

# # #         if data['user_type'] not in ['freelancer', 'recruiter']:
# # #             return jsonify({'success': False, 'message': 'Invalid user type'}), 400

# # #         if User.find_by_email(data['email']):
# # #             return jsonify({'success': False, 'message': 'Email already registered'}), 400

# # #         user_id = User.create(
# # #             username=data['username'],
# # #             email=data['email'],
# # #             password=data['password'],
# # #             first_name=data['first_name'],
# # #             last_name=data['last_name'],
# # #             user_type=data['user_type']
# # #         )
# # #         if not user_id:
# # #             return jsonify({'success': False, 'message': 'Failed to create user'}), 500

# # #         user = User.find_by_id(user_id)
# # #         email_sent = send_verification_email(user)

# # #         token = generate_token(user['id'], user['user_type'], timedelta(days=7))

# # #         return jsonify({
# # #             'success': True,
# # #             'message': 'Registration successful! Please check your email for verification.',
# # #             'token': token,
# # #             'user': user,
# # #             'email_sent': email_sent
# # #         }), 201
# # #     except Exception as e:
# # #         traceback.print_exc()
# # #         return jsonify({'success': False, 'message': str(e)}), 500

# # # @auth_bp.route('/login', methods=['POST'])
# # # def login():
# # #     try:
# # #         data = request.get_json()
# # #         if not data or not data.get('email') or not data.get('password'):
# # #             return jsonify({'success': False, 'message': 'Email and password required'}), 400

# # #         user = User.authenticate(data['email'], data['password'])
# # #         if not user:
# # #             return jsonify({'success': False, 'message': 'Invalid credentials'}), 401

# # #         token = generate_token(user['id'], user['user_type'], timedelta(days=7))
# # #         response = {'success': True, 'token': token, 'user': user}
# # #         if not user.get('is_verified'):
# # #             response['warning'] = 'Please verify your email address'
# # #             response['needs_verification'] = True
# # #         return jsonify(response)
# # #     except Exception as e:
# # #         traceback.print_exc()
# # #         return jsonify({'success': False, 'message': 'Login failed'}), 500

# # # @auth_bp.route('/verify-email/<token>', methods=['GET'])
# # # def verify_email(token):
# # #     try:
# # #         email = verify_verification_token(token)
# # #         if not email:
# # #             return jsonify({'success': False, 'message': 'Invalid or expired token'}), 400

# # #         user = User.find_by_email(email)
# # #         if not user:
# # #             return jsonify({'success': False, 'message': 'User not found'}), 404

# # #         if user.get('is_verified'):
# # #             return jsonify({'success': True, 'message': 'Email already verified'})

# # #         User.verify_email(user['id'])
# # #         return jsonify({'success': True, 'message': 'Email verified successfully!'})
# # #     except Exception as e:
# # #         traceback.print_exc()
# # #         return jsonify({'success': False, 'message': 'Server error'}), 500

# # # @auth_bp.route('/me', methods=['GET'])
# # # def get_current_user():
# # #     try:
# # #         auth_header = request.headers.get('Authorization', '')
# # #         token = auth_header.replace('Bearer ', '') if auth_header else None
# # #         if not token:
# # #             return jsonify({'success': False, 'message': 'No token'}), 401

# # #         payload = decode_token(token)
# # #         if not payload:
# # #             return jsonify({'success': False, 'message': 'Invalid token'}), 401

# # #         user = User.find_by_id(payload['user_id'])
# # #         if not user:
# # #             return jsonify({'success': False, 'message': 'User not found'}), 404

# # #         return jsonify({'success': True, 'user': user})
# # #     except Exception as e:
# # #         return jsonify({'success': False, 'message': str(e)}), 500



# # from flask import Blueprint, request, jsonify, current_app
# # from flask_mail import Message
# # from itsdangerous import URLSafeTimedSerializer, SignatureExpired, BadSignature
# # from database.models import User, FreelancerProfile, RecruiterProfile
# # from utils.auth_utils import validate_email, validate_password, generate_token, decode_token
# # from datetime import datetime, timedelta
# # import traceback

# # auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')

# # def get_mail():
# #     return current_app.extensions['mail']

# # def generate_verification_token(email):
# #     s = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
# #     return s.dumps(email, salt='email-verification-salt')

# # def verify_verification_token(token, expiration=86400):
# #     s = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
# #     try:
# #         email = s.loads(token, salt='email-verification-salt', max_age=expiration)
# #         return email
# #     except (SignatureExpired, BadSignature):
# #         return None

# # def send_verification_email(user):
# #     try:
# #         token = generate_verification_token(user['email'])
# #         link = f"{current_app.config['BASE_URL']}/verify-email/{token}"

# #         html = f"..."
# #         msg = Message(...)
# #         mail.send(msg)
# #         return True
# #     except Exception as e:
# #         print(f"❌ Email error: {e}")
# #         traceback.print_exc()
# #         return False
    

# #         html = f"""<!DOCTYPE html>
# # <html>
# # <body>
# #     <h2>Hello {user['first_name']}!</h2>
# #     <p>Please verify your email by clicking the link below:</p>
# #     <p><a href="{link}">Verify Email</a></p>
# # </body>
# # </html>"""

# #         msg = Message(
# #             subject="Verify Your Email - FreelanceHub",
# #             recipients=[user['email']],
# #             html=html,
# #             sender=current_app.config.get('FROM_EMAIL')
# #         )
# #         mail = get_mail()
# #         mail.send(msg)
# #         return True
# #     except Exception as e:
# #         print(f"❌ Email error: {e}")
# #         traceback.print_exc()
# #         return False

# # @auth_bp.route('/register', methods=['POST'])
# # def register():
# #     try:
# #         data = request.get_json()
# #         print(f"📝 Registration attempt: {data.get('email')}")

# #         required = ['email', 'password', 'first_name', 'last_name', 'username', 'user_type']
# #         for f in required:
# #             if f not in data:
# #                 return jsonify({'success': False, 'message': f'{f} is required'}), 400

# #         if not validate_email(data['email']):
# #             return jsonify({'success': False, 'message': 'Invalid email format'}), 400

# #         valid, msg = validate_password(data['password'])
# #         if not valid:
# #             return jsonify({'success': False, 'message': msg}), 400

# #         if data['user_type'] not in ['freelancer', 'recruiter']:
# #             return jsonify({'success': False, 'message': 'Invalid user type'}), 400

# #         if User.find_by_email(data['email']):
# #             return jsonify({'success': False, 'message': 'Email already registered'}), 400

# #         user_id = User.create(
# #             username=data['username'],
# #             email=data['email'],
# #             password=data['password'],
# #             first_name=data['first_name'],
# #             last_name=data['last_name'],
# #             user_type=data['user_type']
# #         )
# #         if not user_id:
# #             return jsonify({'success': False, 'message': 'Failed to create user'}), 500

# #         user = User.find_by_id(user_id)
# #         email_sent = send_verification_email(user)

# #         token = generate_token(user['id'], user['user_type'], timedelta(days=7))

# #         return jsonify({
# #             'success': True,
# #             'message': 'Registration successful! Please check your email for verification.',
# #             'token': token,
# #             'user': user,
# #             'email_sent': email_sent
# #         }), 201
# #     except Exception as e:
# #         traceback.print_exc()
# #         return jsonify({'success': False, 'message': str(e)}), 500

# # @auth_bp.route('/login', methods=['POST'])
# # def login():
# #     try:
# #         data = request.get_json()
# #         if not data or not data.get('email') or not data.get('password'):
# #             return jsonify({'success': False, 'message': 'Email and password required'}), 400

# #         user = User.authenticate(data['email'], data['password'])
# #         if not user:
# #             return jsonify({'success': False, 'message': 'Invalid credentials'}), 401

# #         token = generate_token(user['id'], user['user_type'], timedelta(days=7))
# #         response = {'success': True, 'token': token, 'user': user}
# #         if not user.get('is_verified'):
# #             response['warning'] = 'Please verify your email address'
# #             response['needs_verification'] = True
# #         return jsonify(response)
# #     except Exception as e:
# #         traceback.print_exc()
# #         return jsonify({'success': False, 'message': 'Login failed'}), 500

# # @auth_bp.route('/verify-email/<token>', methods=['GET'])
# # def verify_email(token):
# #     try:
# #         email = verify_verification_token(token)
# #         if not email:
# #             return jsonify({'success': False, 'message': 'Invalid or expired token'}), 400

# #         user = User.find_by_email(email)
# #         if not user:
# #             return jsonify({'success': False, 'message': 'User not found'}), 404

# #         if user.get('is_verified'):
# #             return jsonify({'success': True, 'message': 'Email already verified'})

# #         User.verify_email(user['id'])
# #         return jsonify({'success': True, 'message': 'Email verified successfully!'})
# #     except Exception as e:
# #         traceback.print_exc()
# #         return jsonify({'success': False, 'message': 'Server error'}), 500

# # @auth_bp.route('/me', methods=['GET'])
# # def get_current_user():
# #     try:
# #         auth_header = request.headers.get('Authorization', '')
# #         token = auth_header.replace('Bearer ', '') if auth_header else None
# #         if not token:
# #             return jsonify({'success': False, 'message': 'No token'}), 401

# #         payload = decode_token(token)
# #         if not payload:
# #             return jsonify({'success': False, 'message': 'Invalid token'}), 401

# #         user = User.find_by_id(payload['user_id'])
# #         if not user:
# #             return jsonify({'success': False, 'message': 'User not found'}), 404

# #         return jsonify({'success': True, 'user': user})
# #     except Exception as e:
# #         return jsonify({'success': False, 'message': str(e)}), 500

# # @auth_bp.route('/refresh', methods=['POST'])
# # def refresh_token():
# #     try:
# #         auth_header = request.headers.get('Authorization', '')
# #         token = auth_header.replace('Bearer ', '') if auth_header else None
# #         if not token:
# #             return jsonify({'success': False, 'message': 'No refresh token'}), 401

# #         payload = decode_token(token)
# #         if not payload:
# #             return jsonify({'success': False, 'message': 'Invalid refresh token'}), 401

# #         new_token = generate_token(payload['user_id'], payload['user_type'], timedelta(days=7))
# #         return jsonify({'success': True, 'access_token': new_token})
# #     except Exception as e:
# #         return jsonify({'success': False, 'message': str(e)}), 500
    


# from flask import Blueprint, request, jsonify, current_app
# from flask_mail import Message
# from itsdangerous import URLSafeTimedSerializer, SignatureExpired, BadSignature
# from database.models import User, FreelancerProfile, RecruiterProfile
# from utils.auth_utils import validate_email, validate_password, generate_token, decode_token
# from datetime import datetime, timedelta
# import traceback

# auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')

# def get_mail():
#     return current_app.extensions['mail']

# def generate_verification_token(email):
#     s = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
#     return s.dumps(email, salt='email-verification-salt')

# def verify_verification_token(token, expiration=86400):
#     s = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
#     try:
#         email = s.loads(token, salt='email-verification-salt', max_age=expiration)
#         return email
#     except (SignatureExpired, BadSignature):
#         return None

# def send_verification_email(user):
#     """Send verification email to user (fixed version)."""
#     try:
#         token = generate_verification_token(user['email'])
#         link = f"{current_app.config['BASE_URL']}/verify-email/{token}"

#         html = f"""<!DOCTYPE html>
# <html>
# <body>
#     <h2>Hello {user['first_name']}!</h2>
#     <p>Please verify your email by clicking the link below:</p>
#     <p><a href="{link}">Verify Email</a></p>
#     <p>This link will expire in 24 hours.</p>
# </body>
# </html>"""

#         msg = Message(
#             subject="Verify Your Email - FreelanceHub",
#             recipients=[user['email']],
#             html=html,
#             sender=current_app.config.get('FROM_EMAIL')
#         )
#         mail = get_mail()
#         mail.send(msg)
#         print(f"✅ Verification email sent to {user['email']}")
#         return True
#     except Exception as e:
#         print(f"❌ Email error: {e}")
#         traceback.print_exc()
#         return False

# @auth_bp.route('/register', methods=['POST'])
# def register():
#     try:
#         data = request.get_json()
#         print(f"📝 Registration attempt: {data.get('email')}")

#         required = ['email', 'password', 'first_name', 'last_name', 'username', 'user_type']
#         for f in required:
#             if f not in data:
#                 return jsonify({'success': False, 'message': f'{f} is required'}), 400

#         if not validate_email(data['email']):
#             return jsonify({'success': False, 'message': 'Invalid email format'}), 400

#         valid, msg = validate_password(data['password'])
#         if not valid:
#             return jsonify({'success': False, 'message': msg}), 400

#         if data['user_type'] not in ['freelancer', 'recruiter']:
#             return jsonify({'success': False, 'message': 'Invalid user type'}), 400

#         if User.find_by_email(data['email']):
#             return jsonify({'success': False, 'message': 'Email already registered'}), 400

#         user_id = User.create(
#             username=data['username'],
#             email=data['email'],
#             password=data['password'],
#             first_name=data['first_name'],
#             last_name=data['last_name'],
#             user_type=data['user_type']
#         )
#         if not user_id:
#             return jsonify({'success': False, 'message': 'Failed to create user'}), 500

#         user = User.find_by_id(user_id)

#         # Send verification email (no set_verification_token)
#         email_sent = send_verification_email(user)

#         token = generate_token(user['id'], user['user_type'], timedelta(days=7))

#         return jsonify({
#             'success': True,
#             'message': 'Registration successful! Please check your email for verification.',
#             'token': token,
#             'user': user,
#             'email_sent': email_sent
#         }), 201
#     except Exception as e:
#         traceback.print_exc()
#         return jsonify({'success': False, 'message': str(e)}), 500

# @auth_bp.route('/login', methods=['POST'])
# def login():
#     try:
#         data = request.get_json()
#         if not data or not data.get('email') or not data.get('password'):
#             return jsonify({'success': False, 'message': 'Email and password required'}), 400

#         user = User.authenticate(data['email'], data['password'])
#         if not user:
#             return jsonify({'success': False, 'message': 'Invalid credentials'}), 401

#         token = generate_token(user['id'], user['user_type'], timedelta(days=7))
#         response = {'success': True, 'token': token, 'user': user}
#         if not user.get('is_verified'):
#             response['warning'] = 'Please verify your email address'
#             response['needs_verification'] = True
#         return jsonify(response)
#     except Exception as e:
#         traceback.print_exc()
#         return jsonify({'success': False, 'message': 'Login failed'}), 500

# @auth_bp.route('/verify-email/<token>', methods=['GET'])
# def verify_email(token):
#     try:
#         email = verify_verification_token(token)
#         if not email:
#             return jsonify({'success': False, 'message': 'Invalid or expired token'}), 400

#         user = User.find_by_email(email)
#         if not user:
#             return jsonify({'success': False, 'message': 'User not found'}), 404

#         if user.get('is_verified'):
#             return jsonify({'success': True, 'message': 'Email already verified'})

#         User.verify_email(user['id'])
#         return jsonify({'success': True, 'message': 'Email verified successfully!'})
#     except Exception as e:
#         traceback.print_exc()
#         return jsonify({'success': False, 'message': 'Server error'}), 500

# @auth_bp.route('/me', methods=['GET'])
# def get_current_user():
#     try:
#         auth_header = request.headers.get('Authorization', '')
#         token = auth_header.replace('Bearer ', '') if auth_header else None
#         if not token:
#             return jsonify({'success': False, 'message': 'No token'}), 401

#         payload = decode_token(token)
#         if not payload:
#             return jsonify({'success': False, 'message': 'Invalid token'}), 401

#         user = User.find_by_id(payload['user_id'])
#         if not user:
#             return jsonify({'success': False, 'message': 'User not found'}), 404

#         return jsonify({'success': True, 'user': user})
#     except Exception as e:
#         return jsonify({'success': False, 'message': str(e)}), 500

# @auth_bp.route('/refresh', methods=['POST'])
# def refresh_token():
#     try:
#         auth_header = request.headers.get('Authorization', '')
#         token = auth_header.replace('Bearer ', '') if auth_header else None
#         if not token:
#             return jsonify({'success': False, 'message': 'No refresh token'}), 401

#         payload = decode_token(token)
#         if not payload:
#             return jsonify({'success': False, 'message': 'Invalid refresh token'}), 401

#         new_token = generate_token(payload['user_id'], payload['user_type'], timedelta(days=7))
#         return jsonify({'success': True, 'access_token': new_token})
#     except Exception as e:
#         return jsonify({'success': False, 'message': str(e)}), 500

        

from flask import Blueprint, request, jsonify, current_app
from flask_mail import Message
from itsdangerous import URLSafeTimedSerializer, SignatureExpired, BadSignature
from database.models import User
from utils.auth_utils import validate_email, validate_password, generate_token, decode_token
from datetime import datetime, timedelta
import traceback

auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')


# ---------------------------------------------------
# MAIL INSTANCE
# ---------------------------------------------------
def get_mail():
    return current_app.extensions['mail']


# ---------------------------------------------------
# TOKEN GENERATION
# ---------------------------------------------------
def generate_verification_token(email):
    serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    return serializer.dumps(email, salt="email-verification")


def verify_verification_token(token, expiration=86400):
    serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    try:
        email = serializer.loads(token, salt="email-verification", max_age=expiration)
        return email
    except (SignatureExpired, BadSignature):
        return None


# ---------------------------------------------------
# SEND EMAIL
# ---------------------------------------------------
def send_verification_email(user):
    try:
        token = generate_verification_token(user['email'])

        verify_url = f"{current_app.config['BASE_URL']}/api/auth/verify-email/{token}"

        html = f"""
        <html>
        <body style="font-family:Arial;">
            <h2>Hello {user['first_name']} 👋</h2>

            <p>Thank you for registering on <b>FreelanceHub</b>.</p>

            <p>Please verify your email by clicking the button below:</p>

            <p>
                <a href="{verify_url}" 
                   style="
                        background:#2563eb;
                        color:white;
                        padding:10px 20px;
                        text-decoration:none;
                        border-radius:5px;">
                    Verify Email
                </a>
            </p>

            <p>This verification link will expire in 24 hours.</p>

            <br>
            <p>Regards,<br>FreelanceHub Team</p>
        </body>
        </html>
        """

        msg = Message(
            subject="Verify your email - FreelanceHub",
            recipients=[user['email']],
            html=html,
            sender=current_app.config.get("MAIL_USERNAME")
        )

        mail = get_mail()
        mail.send(msg)

        print(f"✅ Verification email sent to {user['email']}")

        return True

    except Exception as e:
        print("❌ Email error:", e)
        traceback.print_exc()
        return False


# ---------------------------------------------------
# REGISTER
# ---------------------------------------------------
@auth_bp.route('/register', methods=['POST'])
def register():
    try:

        data = request.get_json()

        required = ['email', 'password', 'first_name', 'last_name', 'username', 'user_type']

        for field in required:
            if not data.get(field):
                return jsonify({
                    "success": False,
                    "message": f"{field} is required"
                }), 400

        # Email validation
        if not validate_email(data['email']):
            return jsonify({
                "success": False,
                "message": "Invalid email format"
            }), 400

        # Password validation
        valid, message = validate_password(data['password'])
        if not valid:
            return jsonify({
                "success": False,
                "message": message
            }), 400

        # User type validation
        if data['user_type'] not in ['freelancer', 'recruiter']:
            return jsonify({
                "success": False,
                "message": "Invalid user type"
            }), 400

        # Existing user check
        if User.find_by_email(data['email']):
            return jsonify({
                "success": False,
                "message": "Email already registered"
            }), 400

        # Create user
        user_id = User.create(
            username=data['username'],
            email=data['email'],
            password=data['password'],
            first_name=data['first_name'],
            last_name=data['last_name'],
            user_type=data['user_type']
        )

        if not user_id:
            return jsonify({
                "success": False,
                "message": "Failed to create user"
            }), 500

        user = User.find_by_id(user_id)

        # Send verification email
        email_sent = send_verification_email(user)

        token = generate_token(user['id'], user['user_type'], timedelta(days=7))

        return jsonify({
            "success": True,
            "message": "Registration successful. Please verify your email.",
            "token": token,
            "email_sent": email_sent,
            "user": user
        }), 201

    except Exception as e:
        traceback.print_exc()
        return jsonify({
            "success": False,
            "message": str(e)
        }), 500


# ---------------------------------------------------
# LOGIN
# ---------------------------------------------------
@auth_bp.route('/login', methods=['POST'])
def login():
    try:

        data = request.get_json()

        if not data or not data.get("email") or not data.get("password"):
            return jsonify({
                "success": False,
                "message": "Email and password required"
            }), 400

        user = User.authenticate(data["email"], data["password"])

        if not user:
            return jsonify({
                "success": False,
                "message": "Invalid credentials"
            }), 401

        token = generate_token(user['id'], user['user_type'], timedelta(days=7))

        response = {
            "success": True,
            "token": token,
            "user": user
        }

        if not user.get("is_verified"):
            response["warning"] = "Please verify your email"
            response["needs_verification"] = True

        return jsonify(response)

    except Exception as e:
        traceback.print_exc()
        return jsonify({
            "success": False,
            "message": "Login failed"
        }), 500


# ---------------------------------------------------
# VERIFY EMAIL
# ---------------------------------------------------
@auth_bp.route('/verify-email/<token>', methods=['GET'])
def verify_email(token):

    try:

        email = verify_verification_token(token)

        if not email:
            return jsonify({
                "success": False,
                "message": "Invalid or expired token"
            }), 400

        user = User.find_by_email(email)

        if not user:
            return jsonify({
                "success": False,
                "message": "User not found"
            }), 404

        if user.get("is_verified"):
            return jsonify({
                "success": True,
                "message": "Email already verified"
            })

        User.verify_email(user['id'])

        return jsonify({
            "success": True,
            "message": "Email verified successfully!"
        })

    except Exception as e:
        traceback.print_exc()
        return jsonify({
            "success": False,
            "message": "Server error"
        }), 500


# ---------------------------------------------------
# CURRENT USER
# ---------------------------------------------------
@auth_bp.route('/me', methods=['GET'])
def get_current_user():

    try:

        auth_header = request.headers.get("Authorization", "")
        token = auth_header.replace("Bearer ", "")

        if not token:
            return jsonify({
                "success": False,
                "message": "No token provided"
            }), 401

        payload = decode_token(token)

        if not payload:
            return jsonify({
                "success": False,
                "message": "Invalid token"
            }), 401

        user = User.find_by_id(payload["user_id"])

        if not user:
            return jsonify({
                "success": False,
                "message": "User not found"
            }), 404

        return jsonify({
            "success": True,
            "user": user
        })

    except Exception as e:
        return jsonify({
            "success": False,
            "message": str(e)
        }), 500


# ---------------------------------------------------
# REFRESH TOKEN
# ---------------------------------------------------
@auth_bp.route('/refresh', methods=['POST'])
def refresh_token():

    try:

        auth_header = request.headers.get("Authorization", "")
        token = auth_header.replace("Bearer ", "")

        payload = decode_token(token)

        if not payload:
            return jsonify({
                "success": False,
                "message": "Invalid token"
            }), 401

        new_token = generate_token(
            payload['user_id'],
            payload['user_type'],
            timedelta(days=7)
        )

        return jsonify({
            "success": True,
            "access_token": new_token
        })

    except Exception as e:
        return jsonify({
            "success": False,
            "message": str(e)
        }), 500