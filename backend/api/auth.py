# # # # from flask import Blueprint, request, jsonify
# # # # from database.models import User
# # # # from utils.auth_utils import validate_email, validate_password, generate_token, decode_token
# # # # from datetime import timedelta
# # # # import os

# # # # auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')

# # # # @auth_bp.route('/register', methods=['POST'])
# # # # def register():
# # # #     """User registration endpoint"""
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
        
# # # #         existing_username = User.find_by_email(data['username'])
# # # #         if existing_username:
# # # #             return jsonify({
# # # #                 'success': False,
# # # #                 'message': 'Username already taken'
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
# # # #             'message': 'Registration successful',
# # # #             'access_token': access_token,
# # # #             'refresh_token': refresh_token,
# # # #             'user': user
# # # #         }), 201
        
# # # #     except Exception as e:
# # # #         return jsonify({
# # # #             'success': False,
# # # #             'message': f'Registration failed: {str(e)}'
# # # #         }), 500

# # # # @auth_bp.route('/login', methods=['POST'])
# # # # def login():
# # # #     """User login endpoint"""
# # # #     try:
# # # #         data = request.get_json()
        
# # # #         if 'email' not in data or 'password' not in data:
# # # #             return jsonify({
# # # #                 'success': False,
# # # #                 'message': 'Email and password are required'
# # # #             }), 400
        
# # # #         # Authenticate user
# # # #         user = User.authenticate(data['email'], data['password'])
        
# # # #         if not user:
# # # #             return jsonify({
# # # #                 'success': False,
# # # #                 'message': 'Invalid email or password'
# # # #             }), 401
        
# # # #         # Generate tokens
# # # #         access_token = generate_token(
# # # #             user['id'],
# # # #             user['user_type'],
# # # #             timedelta(hours=1)
# # # #         )
# # # #         refresh_token = generate_token(
# # # #             user['id'],
# # # #             user['user_type'],
# # # #             timedelta(days=7)
# # # #         )
        
# # # #         return jsonify({
# # # #             'success': True,
# # # #             'message': 'Login successful',
# # # #             'access_token': access_token,
# # # #             'refresh_token': refresh_token,
# # # #             'user': user
# # # #         }), 200
        
# # # #     except Exception as e:
# # # #         return jsonify({
# # # #             'success': False,
# # # #             'message': f'Login failed: {str(e)}'
# # # #         }), 500

# # # # @auth_bp.route('/refresh', methods=['POST'])
# # # # def refresh():
# # # #     """Refresh access token"""
# # # #     try:
# # # #         auth_header = request.headers.get('Authorization')
# # # #         if not auth_header:
# # # #             return jsonify({
# # # #                 'success': False,
# # # #                 'message': 'Refresh token is required'
# # # #             }), 401
        
# # # #         token = auth_header.split(" ")[1]
# # # #         payload = decode_token(token)
        
# # # #         if not payload:
# # # #             return jsonify({
# # # #                 'success': False,
# # # #                 'message': 'Invalid or expired refresh token'
# # # #             }), 401
        
# # # #         # Generate new access token
# # # #         access_token = generate_token(
# # # #             payload['user_id'],
# # # #             payload['user_type'],
# # # #             timedelta(hours=1)
# # # #         )
        
# # # #         return jsonify({
# # # #             'success': True,
# # # #             'access_token': access_token
# # # #         }), 200
        
# # # #     except Exception as e:
# # # #         return jsonify({
# # # #             'success': False,
# # # #             'message': f'Token refresh failed: {str(e)}'
# # # #         }), 500

# # # # @auth_bp.route('/me', methods=['GET'])
# # # # def get_current_user():
# # # #     """Get current user"""
# # # #     from utils.auth_utils import token_required, decode_token
    
# # # #     auth_header = request.headers.get('Authorization')
# # # #     if not auth_header:
# # # #         return jsonify({
# # # #             'success': False,
# # # #             'message': 'Token is required'
# # # #         }), 401
    
# # # #     token = auth_header.split(" ")[1]
# # # #     payload = decode_token(token)
    
# # # #     if not payload:
# # # #         return jsonify({
# # # #             'success': False,
# # # #             'message': 'Invalid or expired token'
# # # #         }), 401
    
# # # #     user = User.find_by_id(payload['user_id'])
# # # #     if not user:
# # # #         return jsonify({
# # # #             'success': False,
# # # #             'message': 'User not found'
# # # #         }), 404
    
# # # #     if 'password_hash' in user:
# # # #         del user['password_hash']
    
# # # #     return jsonify({
# # # #         'success': True,
# # # #         'user': user
# # # #     }), 200

# # # # @auth_bp.route('/logout', methods=['POST'])
# # # # def logout():
# # # #     """User logout endpoint"""
# # # #     return jsonify({
# # # #         'success': True,
# # # #         'message': 'Logout successful'
# # # #     }), 200
# # # # api/auth.py - UPDATED VERSION (Remove db import)

# # # from flask import Blueprint, request, jsonify, current_app
# # # from flask_mail import Message, Mail
# # # from itsdangerous import URLSafeTimedSerializer, SignatureExpired, BadSignature
# # # from database.models import User  # REMOVED db from import
# # # from utils.email_templates import EmailTemplates
# # # import logging
# # # from datetime import datetime, timedelta
# # # import jwt
# # # import traceback

# # # auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')
# # # mail = Mail()

# # # def generate_verification_token(email):
# # #     """Generate a secure token for email verification"""
# # #     serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
# # #     return serializer.dumps(email, salt='email-verification-salt')

# # # def verify_verification_token(token, expiration=86400):  # 24 hours
# # #     """Verify the token and return email if valid"""
# # #     serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
# # #     try:
# # #         email = serializer.loads(token, salt='email-verification-salt', max_age=expiration)
# # #         return email
# # #     except (SignatureExpired, BadSignature):
# # #         return None

# # # def send_verification_email(user):
# # #     """Send verification email to user"""
# # #     try:
# # #         token = generate_verification_token(user['email'])
# # #         verification_link = f"{current_app.config['BASE_URL']}/verify-email/{token}"
        
# # #         # Get email template
# # #         html_content, subject = EmailTemplates.email_verification(
# # #             user_name=user['first_name'] or user['username'],
# # #             verification_token=token
# # #         )
        
# # #         # Create message
# # #         msg = Message(
# # #             subject=subject,
# # #             recipients=[user['email']],
# # #             html=html_content,
# # #             sender=current_app.config.get('FROM_EMAIL', 'noreply@freelancehub.com')
# # #         )
        
# # #         # Send email
# # #         mail.send(msg)
        
# # #         print(f"✅ Verification email sent to {user['email']}")
# # #         return True
        
# # #     except Exception as e:
# # #         print(f"❌ Failed to send verification email: {str(e)}")
# # #         traceback.print_exc()
# # #         return False

# # # @auth_bp.route('/register', methods=['POST'])
# # # def register():
# # #     """Register a new user with email verification"""
# # #     try:
# # #         data = request.get_json()
        
# # #         print(f"📝 Registration attempt: {data.get('email')}")
        
# # #         # Check required fields
# # #         required_fields = ['email', 'password', 'first_name', 'last_name', 'username', 'user_type']
# # #         for field in required_fields:
# # #             if field not in data:
# # #                 return jsonify({
# # #                     'success': False,
# # #                     'message': f'{field} is required'
# # #                 }), 400
        
# # #         # Check if user exists
# # #         existing_user = User.find_by_email(data['email'])
# # #         if existing_user:
# # #             return jsonify({
# # #                 'success': False,
# # #                 'message': 'Email already registered. Please login instead.'
# # #             }), 400
        
# # #         # Create user
# # #         user_id = User.create(
# # #             username=data['username'],
# # #             email=data['email'],
# # #             password=data['password'],
# # #             first_name=data['first_name'],
# # #             last_name=data['last_name'],
# # #             user_type=data.get('user_type', 'freelancer')
# # #         )
        
# # #         if not user_id:
# # #             return jsonify({
# # #                 'success': False,
# # #                 'message': 'Failed to create user'
# # #             }), 500
        
# # #         # Get created user
# # #         user = User.find_by_id(user_id)
        
# # #         # Send verification email
# # #         email_sent = send_verification_email(user)
        
# # #         # Generate JWT token
# # #         token = jwt.encode(
# # #             {
# # #                 'user_id': user['id'],
# # #                 'email': user['email'],
# # #                 'exp': datetime.utcnow() + timedelta(days=7)
# # #             },
# # #             current_app.config['JWT_SECRET_KEY'],
# # #             algorithm='HS256'
# # #         )
        
# # #         response_data = {
# # #             'success': True,
# # #             'message': 'Registration successful! Please check your email for verification link.',
# # #             'token': token,
# # #             'user': user,
# # #             'email_sent': email_sent
# # #         }
        
# # #         if not email_sent:
# # #             response_data['warning'] = 'Account created but verification email could not be sent. Please contact support.'
        
# # #         return jsonify(response_data), 201
        
# # #     except Exception as e:
# # #         print(f"❌ Registration error: {str(e)}")
# # #         traceback.print_exc()
# # #         return jsonify({
# # #             'success': False,
# # #             'message': f'Registration failed: {str(e)}'
# # #         }), 500

# # # @auth_bp.route('/login', methods=['POST'])
# # # def login():
# # #     """Login user"""
# # #     try:
# # #         data = request.get_json()
        
# # #         if not data or not data.get('email') or not data.get('password'):
# # #             return jsonify({
# # #                 'success': False,
# # #                 'message': 'Email and password are required'
# # #             }), 400
            
# # #         user = User.find_by_email(data['email'])
        
# # #         if not user:
# # #             return jsonify({
# # #                 'success': False,
# # #                 'message': 'Invalid email or password'
# # #             }), 401
            
# # #         # Check password (you'll need to implement this in your User model)
# # #         # For now, let's assume it's correct
# # #         # You should add a check_password method to your User model
        
# # #         # Generate JWT
# # #         token = jwt.encode(
# # #             {
# # #                 'user_id': user['id'],
# # #                 'email': user['email'],
# # #                 'exp': datetime.utcnow() + timedelta(days=7)
# # #             },
# # #             current_app.config['JWT_SECRET_KEY'],
# # #             algorithm='HS256'
# # #         )
        
# # #         response = {
# # #             'success': True,
# # #             'token': token,
# # #             'user': user
# # #         }
        
# # #         return jsonify(response)
        
# # #     except Exception as e:
# # #         print(f"❌ Login error: {str(e)}")
# # #         return jsonify({
# # #             'success': False,
# # #             'message': 'Login failed'
# # #         }), 500

# # # @auth_bp.route('/me', methods=['GET'])
# # # def get_current_user():
# # #     """Get current user info"""
# # #     try:
# # #         auth_header = request.headers.get('Authorization', '')
# # #         token = auth_header.replace('Bearer ', '') if auth_header else None
        
# # #         if not token:
# # #             return jsonify({
# # #                 'success': False,
# # #                 'message': 'No token provided'
# # #             }), 401
            
# # #         try:
# # #             payload = jwt.decode(
# # #                 token,
# # #                 current_app.config['JWT_SECRET_KEY'],
# # #                 algorithms=['HS256']
# # #             )
# # #             user_id = payload.get('user_id')
# # #             user = User.find_by_id(user_id)
# # #         except jwt.ExpiredSignatureError:
# # #             return jsonify({
# # #                 'success': False,
# # #                 'message': 'Token expired'
# # #             }), 401
# # #         except jwt.InvalidTokenError:
# # #             return jsonify({
# # #                 'success': False,
# # #                 'message': 'Invalid token'
# # #             }), 401
        
# # #         if not user:
# # #             return jsonify({
# # #                 'success': False,
# # #                 'message': 'User not found'
# # #             }), 404
            
# # #         return jsonify({
# # #             'success': True,
# # #             'user': user
# # #         })
        
# # #     except Exception as e:
# # #         print(f"❌ Get user error: {str(e)}")
# # #         return jsonify({
# # #             'success': False,
# # #             'message': 'Server error'
# # #         }), 500
# # # api/auth.py - FINAL VERSION with Email Verification

# # from flask import Blueprint, request, jsonify, current_app
# # from flask_mail import Message, Mail
# # from itsdangerous import URLSafeTimedSerializer, SignatureExpired, BadSignature
# # from database.models import User
# # from datetime import datetime, timedelta
# # import jwt
# # import traceback

# # # Initialize blueprint and mail
# # auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')
# # mail = Mail()  # This will be initialized in app.py

# # def generate_verification_token(email):
# #     """Generate a secure token for email verification"""
# #     serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
# #     return serializer.dumps(email, salt='email-verification-salt')

# # def verify_verification_token(token, expiration=86400):  # 24 hours
# #     """Verify the token and return email if valid"""
# #     serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
# #     try:
# #         email = serializer.loads(token, salt='email-verification-salt', max_age=expiration)
# #         return email
# #     except (SignatureExpired, BadSignature):
# #         return None

# # def send_verification_email(user):
# #     """Send verification email to user"""
# #     try:
# #         token = generate_verification_token(user['email'])
# #         verification_link = f"{current_app.config['BASE_URL']}/verify-email/{token}"
        
# #         # Save token to user record
# #         User.set_verification_token(user['id'], token)
        
# #         # HTML Email Template
# #         html_content = f"""
# #         <!DOCTYPE html>
# #         <html>
# #         <head>
# #             <meta charset="UTF-8">
# #             <meta name="viewport" content="width=device-width, initial-scale=1.0">
# #             <style>
# #                 body {{
# #                     font-family: Arial, sans-serif;
# #                     line-height: 1.6;
# #                     color: #333;
# #                     max-width: 600px;
# #                     margin: 0 auto;
# #                     padding: 20px;
# #                 }}
# #                 .header {{
# #                     background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
# #                     color: white;
# #                     padding: 30px;
# #                     text-align: center;
# #                     border-radius: 10px 10px 0 0;
# #                 }}
# #                 .content {{
# #                     background: #f9f9f9;
# #                     padding: 30px;
# #                     border-radius: 0 0 10px 10px;
# #                 }}
# #                 .button {{
# #                     display: inline-block;
# #                     padding: 15px 40px;
# #                     background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
# #                     color: white;
# #                     text-decoration: none;
# #                     border-radius: 50px;
# #                     font-weight: bold;
# #                     margin: 20px 0;
# #                 }}
# #                 .footer {{
# #                     text-align: center;
# #                     color: #666;
# #                     font-size: 12px;
# #                     margin-top: 20px;
# #                 }}
# #             </style>
# #         </head>
# #         <body>
# #             <div class="header">
# #                 <h1>Welcome to FreelanceHub! 🚀</h1>
# #             </div>
# #             <div class="content">
# #                 <h2>Hello {user['first_name']}!</h2>
# #                 <p>Thank you for signing up! Please verify your email address to get started.</p>
# #                 <div style="text-align: center;">
# #                     <a href="{verification_link}" class="button">Verify Email Address</a>
# #                 </div>
# #                 <p style="color: #666; font-size: 14px;">Or copy this link: {verification_link}</p>
# #                 <p style="color: #666; font-size: 14px;">This link will expire in 24 hours.</p>
# #             </div>
# #             <div class="footer">
# #                 <p>&copy; 2026 FreelanceHub. All rights reserved.</p>
# #             </div>
# #         </body>
# #         </html>
# #         """
        
# #         # Create message
# #         msg = Message(
# #             subject="Verify Your Email - FreelanceHub",
# #             recipients=[user['email']],
# #             html=html_content,
# #             sender=current_app.config.get('FROM_EMAIL', 'noreply@freelancehub.com')
# #         )
        
# #         # Send email
# #         mail.send(msg)
# #         print(f"✅ Verification email sent to {user['email']}")
# #         return True
        
# #     except Exception as e:
# #         print(f"❌ Failed to send verification email: {str(e)}")
# #         traceback.print_exc()
# #         return False

# # @auth_bp.route('/register', methods=['POST'])
# # def register():
# #     """Register a new user with email verification"""
# #     try:
# #         data = request.get_json()
        
# #         print(f"📝 Registration attempt: {data.get('email')}")
        
# #         # Check required fields
# #         required_fields = ['email', 'password', 'first_name', 'last_name', 'username', 'user_type']
# #         for field in required_fields:
# #             if field not in data:
# #                 return jsonify({
# #                     'success': False,
# #                     'message': f'{field} is required'
# #                 }), 400
        
# #         # Check if user exists
# #         existing_user = User.find_by_email(data['email'])
# #         if existing_user:
# #             return jsonify({
# #                 'success': False,
# #                 'message': 'Email already registered. Please login instead.'
# #             }), 400
        
# #         # Create user
# #         user_id = User.create(
# #             username=data['username'],
# #             email=data['email'],
# #             password=data['password'],
# #             first_name=data['first_name'],
# #             last_name=data['last_name'],
# #             user_type=data.get('user_type', 'freelancer')
# #         )
        
# #         if not user_id:
# #             return jsonify({
# #                 'success': False,
# #                 'message': 'Failed to create user'
# #             }), 500
        
# #         # Get created user
# #         user = User.find_by_id(user_id)
        
# #         # Send verification email
# #         email_sent = send_verification_email(user)
        
# #         # Generate JWT token
# #         token = jwt.encode(
# #             {
# #                 'user_id': user['id'],
# #                 'email': user['email'],
# #                 'exp': datetime.utcnow() + timedelta(days=7)
# #             },
# #             current_app.config['JWT_SECRET_KEY'],
# #             algorithm='HS256'
# #         )
        
# #         response_data = {
# #             'success': True,
# #             'message': 'Registration successful! Please check your email for verification link.',
# #             'token': token,
# #             'user': user,
# #             'email_sent': email_sent
# #         }
        
# #         if not email_sent:
# #             response_data['warning'] = 'Account created but verification email could not be sent. Please contact support.'
        
# #         return jsonify(response_data), 201
        
# #     except Exception as e:
# #         print(f"❌ Registration error: {str(e)}")
# #         traceback.print_exc()
# #         return jsonify({
# #             'success': False,
# #             'message': f'Registration failed: {str(e)}'
# #         }), 500

# # @auth_bp.route('/verify-email/<token>', methods=['GET'])
# # def verify_email(token):
# #     """Verify email with token"""
# #     try:
# #         print(f"📧 Verifying email with token: {token[:20]}...")
        
# #         email = verify_verification_token(token)
        
# #         if not email:
# #             return jsonify({
# #                 'success': False,
# #                 'message': 'Invalid or expired verification link. Please request a new one.'
# #             }), 400
            
# #         user = User.find_by_email(email)
        
# #         if not user:
# #             return jsonify({
# #                 'success': False,
# #                 'message': 'User not found'
# #             }), 404
            
# #         if user.get('is_verified'):
# #             return jsonify({
# #                 'success': True,
# #                 'message': 'Email already verified'
# #             })
            
# #         # Mark user as verified
# #         User.verify_email(user['id'])
        
# #         print(f"✅ Email verified for {user['email']}")
        
# #         return jsonify({
# #             'success': True,
# #             'message': 'Email verified successfully! Welcome to FreelanceHub! 🎉'
# #         })
        
# #     except Exception as e:
# #         print(f"❌ Verification error: {str(e)}")
# #         traceback.print_exc()
# #         return jsonify({
# #             'success': False,
# #             'message': 'Server error during verification'
# #         }), 500

# # @auth_bp.route('/login', methods=['POST'])
# # def login():
# #     """Login user"""
# #     try:
# #         data = request.get_json()
        
# #         if not data or not data.get('email') or not data.get('password'):
# #             return jsonify({
# #                 'success': False,
# #                 'message': 'Email and password are required'
# #             }), 400
            
# #         user = User.authenticate(data['email'], data['password'])
        
# #         if not user:
# #             return jsonify({
# #                 'success': False,
# #                 'message': 'Invalid email or password'
# #             }), 401
            
# #         # Generate JWT
# #         token = jwt.encode(
# #             {
# #                 'user_id': user['id'],
# #                 'email': user['email'],
# #                 'exp': datetime.utcnow() + timedelta(days=7)
# #             },
# #             current_app.config['JWT_SECRET_KEY'],
# #             algorithm='HS256'
# #         )
        
# #         response = {
# #             'success': True,
# #             'token': token,
# #             'user': user
# #         }
        
# #         # Add warning if not verified
# #         if not user.get('is_verified'):
# #             response['warning'] = 'Please verify your email address to receive notifications'
# #             response['needs_verification'] = True
        
# #         return jsonify(response)
        
# #     except Exception as e:
# #         print(f"❌ Login error: {str(e)}")
# #         return jsonify({
# #             'success': False,
# #             'message': 'Login failed'
# #         }), 500

# # @auth_bp.route('/resend-verification', methods=['POST'])
# # def resend_verification():
# #     """Resend verification email"""
# #     try:
# #         # Get user from token
# #         auth_header = request.headers.get('Authorization', '')
# #         token = auth_header.replace('Bearer ', '') if auth_header else None
        
# #         if not token:
# #             return jsonify({
# #                 'success': False,
# #                 'message': 'Authentication required'
# #             }), 401
            
# #         try:
# #             payload = jwt.decode(
# #                 token,
# #                 current_app.config['JWT_SECRET_KEY'],
# #                 algorithms=['HS256']
# #             )
# #             user_id = payload.get('user_id')
# #             user = User.find_by_id(user_id)
# #         except jwt.ExpiredSignatureError:
# #             return jsonify({
# #                 'success': False,
# #                 'message': 'Session expired. Please login again.'
# #             }), 401
# #         except jwt.InvalidTokenError:
# #             return jsonify({
# #                 'success': False,
# #                 'message': 'Invalid token'
# #             }), 401
        
# #         if not user:
# #             return jsonify({
# #                 'success': False,
# #                 'message': 'User not found'
# #             }), 404
            
# #         if user.get('is_verified'):
# #             return jsonify({
# #                 'success': False,
# #                 'message': 'Email already verified'
# #             }), 400
            
# #         # Send verification email
# #         if send_verification_email(user):
# #             return jsonify({
# #                 'success': True,
# #                 'message': 'Verification email sent successfully! Please check your inbox.'
# #             })
# #         else:
# #             return jsonify({
# #                 'success': False,
# #                 'message': 'Failed to send verification email. Please try again later.'
# #             }), 500
            
# #     except Exception as e:
# #         print(f"❌ Resend verification error: {str(e)}")
# #         return jsonify({
# #             'success': False,
# #             'message': 'Server error'
# #         }), 500

# # @auth_bp.route('/me', methods=['GET'])
# # def get_current_user():
# #     """Get current user info"""
# #     try:
# #         auth_header = request.headers.get('Authorization', '')
# #         token = auth_header.replace('Bearer ', '') if auth_header else None
        
# #         if not token:
# #             return jsonify({
# #                 'success': False,
# #                 'message': 'No token provided'
# #             }), 401
            
# #         try:
# #             payload = jwt.decode(
# #                 token,
# #                 current_app.config['JWT_SECRET_KEY'],
# #                 algorithms=['HS256']
# #             )
# #             user_id = payload.get('user_id')
# #             user = User.find_by_id(user_id)
# #         except jwt.ExpiredSignatureError:
# #             return jsonify({
# #                 'success': False,
# #                 'message': 'Token expired'
# #             }), 401
# #         except jwt.InvalidTokenError:
# #             return jsonify({
# #                 'success': False,
# #                 'message': 'Invalid token'
# #             }), 401
        
# #         if not user:
# #             return jsonify({
# #                 'success': False,
# #                 'message': 'User not found'
# #             }), 404
            
# #         return jsonify({
# #             'success': True,
# #             'user': user
# #         })
        
# #     except Exception as e:
# #         print(f"❌ Get user error: {str(e)}")
# #         return jsonify({
# #             'success': False,
# #             'message': 'Server error'
# #         }), 500
# # api/auth.py

# from flask import Blueprint, request, jsonify, current_app
# from flask_mail import Message, Mail
# from itsdangerous import URLSafeTimedSerializer, SignatureExpired, BadSignature
# from database.models import User
# from datetime import datetime, timedelta
# import jwt
# import traceback

# # Initialize blueprint and mail
# auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')
# mail = Mail()

# def generate_verification_token(email):
#     """Generate a secure token for email verification"""
#     serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
#     return serializer.dumps(email, salt='email-verification-salt')

# def verify_verification_token(token, expiration=86400):  # 24 hours
#     """Verify the token and return email if valid"""
#     serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
#     try:
#         email = serializer.loads(token, salt='email-verification-salt', max_age=expiration)
#         return email
#     except (SignatureExpired, BadSignature):
#         return None

# def send_verification_email(user):
#     """Send verification email to user"""
#     try:
#         token = generate_verification_token(user['email'])
#         verification_link = f"{current_app.config['BASE_URL']}/verify-email/{token}"
        
#         # Save token to user record
#         User.set_verification_token(user['id'], token)
        
#         # HTML Email Template
#         html_content = f"""
#         <!DOCTYPE html>
#         <html>
#         <head>
#             <meta charset="UTF-8">
#             <meta name="viewport" content="width=device-width, initial-scale=1.0">
#             <style>
#                 body {{
#                     font-family: Arial, sans-serif;
#                     line-height: 1.6;
#                     color: #333;
#                     max-width: 600px;
#                     margin: 0 auto;
#                     padding: 20px;
#                 }}
#                 .header {{
#                     background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
#                     color: white;
#                     padding: 30px;
#                     text-align: center;
#                     border-radius: 10px 10px 0 0;
#                 }}
#                 .content {{
#                     background: #f9f9f9;
#                     padding: 30px;
#                     border-radius: 0 0 10px 10px;
#                 }}
#                 .button {{
#                     display: inline-block;
#                     padding: 15px 40px;
#                     background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
#                     color: white;
#                     text-decoration: none;
#                     border-radius: 50px;
#                     font-weight: bold;
#                     margin: 20px 0;
#                 }}
#                 .footer {{
#                     text-align: center;
#                     color: #666;
#                     font-size: 12px;
#                     margin-top: 20px;
#                 }}
#             </style>
#         </head>
#         <body>
#             <div class="header">
#                 <h1>Welcome to FreelanceHub! 🚀</h1>
#             </div>
#             <div class="content">
#                 <h2>Hello {user['first_name']}!</h2>
#                 <p>Thank you for signing up! Please verify your email address to get started.</p>
#                 <div style="text-align: center;">
#                     <a href="{verification_link}" class="button">Verify Email Address</a>
#                 </div>
#                 <p style="color: #666; font-size: 14px;">Or copy this link: {verification_link}</p>
#                 <p style="color: #666; font-size: 14px;">This link will expire in 24 hours.</p>
#             </div>
#             <div class="footer">
#                 <p>&copy; 2026 FreelanceHub. All rights reserved.</p>
#             </div>
#         </body>
#         </html>
#         """
        
#         # Create message
#         msg = Message(
#             subject="Verify Your Email - FreelanceHub",
#             recipients=[user['email']],
#             html=html_content,
#             sender=current_app.config.get('FROM_EMAIL', 'noreply@freelancehub.com')
#         )
        
#         # Send email
#         mail.send(msg)
#         print(f"✅ Verification email sent to {user['email']}")
#         return True
        
#     except Exception as e:
#         print(f"❌ Failed to send verification email: {str(e)}")
#         traceback.print_exc()
#         return False

# @auth_bp.route('/register', methods=['POST'])
# def register():
#     """Register a new user with email verification"""
#     try:
#         data = request.get_json()
        
#         print(f"📝 Registration attempt: {data.get('email')}")
        
#         # Check required fields
#         required_fields = ['email', 'password', 'first_name', 'last_name', 'username', 'user_type']
#         for field in required_fields:
#             if field not in data:
#                 return jsonify({
#                     'success': False,
#                     'message': f'{field} is required'
#                 }), 400
        
#         # Check if user exists
#         existing_user = User.find_by_email(data['email'])
#         if existing_user:
#             return jsonify({
#                 'success': False,
#                 'message': 'Email already registered. Please login instead.'
#             }), 400
        
#         # Create user
#         user_id = User.create(
#             username=data['username'],
#             email=data['email'],
#             password=data['password'],
#             first_name=data['first_name'],
#             last_name=data['last_name'],
#             user_type=data.get('user_type', 'freelancer')
#         )
        
#         if not user_id:
#             return jsonify({
#                 'success': False,
#                 'message': 'Failed to create user'
#             }), 500
        
#         # Get created user
#         user = User.find_by_id(user_id)
        
#         # Send verification email
#         email_sent = send_verification_email(user)
        
#         # Generate JWT token
#         token = jwt.encode(
#             {
#                 'user_id': user['id'],
#                 'email': user['email'],
#                 'exp': datetime.utcnow() + timedelta(days=7)
#             },
#             current_app.config['JWT_SECRET_KEY'],
#             algorithm='HS256'
#         )
        
#         response_data = {
#             'success': True,
#             'message': 'Registration successful! Please check your email for verification link.',
#             'token': token,
#             'user': user,
#             'email_sent': email_sent
#         }
        
#         if not email_sent:
#             response_data['warning'] = 'Account created but verification email could not be sent. Please contact support.'
        
#         return jsonify(response_data), 201
        
#     except Exception as e:
#         print(f"❌ Registration error: {str(e)}")
#         traceback.print_exc()
#         return jsonify({
#             'success': False,
#             'message': f'Registration failed: {str(e)}'
#         }), 500

# @auth_bp.route('/verify-email/<token>', methods=['GET'])
# def verify_email(token):
#     """Verify email with token"""
#     try:
#         print(f"📧 Verifying email with token: {token[:20]}...")
        
#         email = verify_verification_token(token)
        
#         if not email:
#             return jsonify({
#                 'success': False,
#                 'message': 'Invalid or expired verification link. Please request a new one.'
#             }), 400
            
#         user = User.find_by_email(email)
        
#         if not user:
#             return jsonify({
#                 'success': False,
#                 'message': 'User not found'
#             }), 404
            
#         if user.get('is_verified'):
#             return jsonify({
#                 'success': True,
#                 'message': 'Email already verified'
#             })
            
#         # Mark user as verified
#         User.verify_email(user['id'])
        
#         print(f"✅ Email verified for {user['email']}")
        
#         return jsonify({
#             'success': True,
#             'message': 'Email verified successfully! Welcome to FreelanceHub! 🎉'
#         })
        
#     except Exception as e:
#         print(f"❌ Verification error: {str(e)}")
#         traceback.print_exc()
#         return jsonify({
#             'success': False,
#             'message': 'Server error during verification'
#         }), 500

# @auth_bp.route('/login', methods=['POST'])
# def login():
#     """Login user"""
#     try:
#         data = request.get_json()
        
#         if not data or not data.get('email') or not data.get('password'):
#             return jsonify({
#                 'success': False,
#                 'message': 'Email and password are required'
#             }), 400
            
#         user = User.authenticate(data['email'], data['password'])
        
#         if not user:
#             return jsonify({
#                 'success': False,
#                 'message': 'Invalid email or password'
#             }), 401
            
#         # Generate JWT
#         token = jwt.encode(
#             {
#                 'user_id': user['id'],
#                 'email': user['email'],
#                 'exp': datetime.utcnow() + timedelta(days=7)
#             },
#             current_app.config['JWT_SECRET_KEY'],
#             algorithm='HS256'
#         )
        
#         response = {
#             'success': True,
#             'token': token,
#             'user': user
#         }
        
#         # Add warning if not verified
#         if not user.get('is_verified'):
#             response['warning'] = 'Please verify your email address to receive notifications'
#             response['needs_verification'] = True
        
#         return jsonify(response)
        
#     except Exception as e:
#         print(f"❌ Login error: {str(e)}")
#         return jsonify({
#             'success': False,
#             'message': 'Login failed'
#         }), 500

# @auth_bp.route('/resend-verification', methods=['POST'])
# def resend_verification():
#     """Resend verification email"""
#     try:
#         # Get user from token
#         auth_header = request.headers.get('Authorization', '')
#         token = auth_header.replace('Bearer ', '') if auth_header else None
        
#         if not token:
#             return jsonify({
#                 'success': False,
#                 'message': 'Authentication required'
#             }), 401
            
#         try:
#             payload = jwt.decode(
#                 token,
#                 current_app.config['JWT_SECRET_KEY'],
#                 algorithms=['HS256']
#             )
#             user_id = payload.get('user_id')
#             user = User.find_by_id(user_id)
#         except jwt.ExpiredSignatureError:
#             return jsonify({
#                 'success': False,
#                 'message': 'Session expired. Please login again.'
#             }), 401
#         except jwt.InvalidTokenError:
#             return jsonify({
#                 'success': False,
#                 'message': 'Invalid token'
#             }), 401
        
#         if not user:
#             return jsonify({
#                 'success': False,
#                 'message': 'User not found'
#             }), 404
            
#         if user.get('is_verified'):
#             return jsonify({
#                 'success': False,
#                 'message': 'Email already verified'
#             }), 400
            
#         # Send verification email
#         if send_verification_email(user):
#             return jsonify({
#                 'success': True,
#                 'message': 'Verification email sent successfully! Please check your inbox.'
#             })
#         else:
#             return jsonify({
#                 'success': False,
#                 'message': 'Failed to send verification email. Please try again later.'
#             }), 500
            
#     except Exception as e:
#         print(f"❌ Resend verification error: {str(e)}")
#         return jsonify({
#             'success': False,
#             'message': 'Server error'
#         }), 500

# @auth_bp.route('/me', methods=['GET'])
# def get_current_user():
#     """Get current user info"""
#     try:
#         auth_header = request.headers.get('Authorization', '')
#         token = auth_header.replace('Bearer ', '') if auth_header else None
        
#         if not token:
#             return jsonify({
#                 'success': False,
#                 'message': 'No token provided'
#             }), 401
            
#         try:
#             payload = jwt.decode(
#                 token,
#                 current_app.config['JWT_SECRET_KEY'],
#                 algorithms=['HS256']
#             )
#             user_id = payload.get('user_id')
#             user = User.find_by_id(user_id)
#         except jwt.ExpiredSignatureError:
#             return jsonify({
#                 'success': False,
#                 'message': 'Token expired'
#             }), 401
#         except jwt.InvalidTokenError:
#             return jsonify({
#                 'success': False,
#                 'message': 'Invalid token'
#             }), 401
        
#         if not user:
#             return jsonify({
#                 'success': False,
#                 'message': 'User not found'
#             }), 404
            
#         return jsonify({
#             'success': True,
#             'user': user
#         })
        
#     except Exception as e:
#         print(f"❌ Get user error: {str(e)}")
#         return jsonify({
#             'success': False,
#             'message': 'Server error'
#         }), 500
        
        


from flask import Blueprint, request, jsonify, current_app
from flask_mail import Message, Mail
from itsdangerous import URLSafeTimedSerializer, SignatureExpired, BadSignature
from database.models import User
from datetime import datetime, timedelta
import jwt
import traceback

# Initialize blueprint
auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')
mail = Mail()

def generate_verification_token(email):
    """Generate a secure token for email verification"""
    serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    return serializer.dumps(email, salt='email-verification-salt')

def verify_verification_token(token, expiration=86400):  # 24 hours
    """Verify the token and return email if valid"""
    serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    try:
        email = serializer.loads(token, salt='email-verification-salt', max_age=expiration)
        return email
    except (SignatureExpired, BadSignature):
        return None

def send_verification_email(user):
    """Send verification email to user"""
    try:
        token = generate_verification_token(user['email'])
        verification_link = f"{current_app.config['BASE_URL']}/verify-email/{token}"
        
        # Save token to user record
        User.set_verification_token(user['id'], token)
        
        # HTML Email Template
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    line-height: 1.6;
                    color: #333;
                    max-width: 600px;
                    margin: 0 auto;
                    padding: 20px;
                }}
                .header {{
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    color: white;
                    padding: 30px;
                    text-align: center;
                    border-radius: 10px 10px 0 0;
                }}
                .content {{
                    background: #f9f9f9;
                    padding: 30px;
                    border-radius: 0 0 10px 10px;
                }}
                .button {{
                    display: inline-block;
                    padding: 15px 40px;
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    color: white;
                    text-decoration: none;
                    border-radius: 50px;
                    font-weight: bold;
                    margin: 20px 0;
                }}
                .footer {{
                    text-align: center;
                    color: #666;
                    font-size: 12px;
                    margin-top: 20px;
                }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1>Welcome to FreelanceHub! 🚀</h1>
            </div>
            <div class="content">
                <h2>Hello {user['first_name']}!</h2>
                <p>Thank you for signing up! Please verify your email address to get started.</p>
                <div style="text-align: center;">
                    <a href="{verification_link}" class="button">Verify Email Address</a>
                </div>
                <p style="color: #666; font-size: 14px;">Or copy this link: {verification_link}</p>
                <p style="color: #666; font-size: 14px;">This link will expire in 24 hours.</p>
            </div>
            <div class="footer">
                <p>&copy; 2026 FreelanceHub. All rights reserved.</p>
            </div>
        </body>
        </html>
        """
        
        # Create message
        msg = Message(
            subject="Verify Your Email - FreelanceHub",
            recipients=[user['email']],
            html=html_content,
            sender=current_app.config.get('FROM_EMAIL', 'noreply@freelancehub.com')
        )
        
        # Send email
        mail.send(msg)
        print(f"✅ Verification email sent to {user['email']}")
        return True
        
    except Exception as e:
        print(f"❌ Failed to send verification email: {str(e)}")
        traceback.print_exc()
        return False

@auth_bp.route('/register', methods=['POST'])
def register():
    """Register a new user with email verification"""
    try:
        data = request.get_json()
        
        print(f"📝 Registration attempt: {data.get('email')}")
        
        # Check required fields
        required_fields = ['email', 'password', 'first_name', 'last_name', 'username', 'user_type']
        for field in required_fields:
            if field not in data:
                return jsonify({
                    'success': False,
                    'message': f'{field} is required'
                }), 400
        
        # Check if user exists
        existing_user = User.find_by_email(data['email'])
        if existing_user:
            return jsonify({
                'success': False,
                'message': 'Email already registered. Please login instead.'
            }), 400
        
        # Create user
        user_id = User.create(
            username=data['username'],
            email=data['email'],
            password=data['password'],
            first_name=data['first_name'],
            last_name=data['last_name'],
            user_type=data.get('user_type', 'freelancer')
        )
        
        if not user_id:
            return jsonify({
                'success': False,
                'message': 'Failed to create user'
            }), 500
        
        # Get created user
        user = User.find_by_id(user_id)
        
        # Send verification email (don't fail if email doesn't work)
        try:
            email_sent = send_verification_email(user)
        except Exception as e:
            print(f"⚠️ Email sending failed but continuing: {e}")
            email_sent = False
        
        # Generate JWT token with user_type included
        token = jwt.encode(
            {
                'user_id': user['id'],
                'email': user['email'],
                'user_type': user['user_type'],  # IMPORTANT: Include user_type
                'exp': datetime.utcnow() + timedelta(days=7)
            },
            current_app.config['JWT_SECRET_KEY'],
            algorithm='HS256'
        )
        
        response_data = {
            'success': True,
            'message': 'Registration successful! Please check your email for verification link.',
            'token': token,
            'user': user,
            'email_sent': email_sent
        }
        
        if not email_sent:
            response_data['warning'] = 'Account created but verification email could not be sent. Please contact support.'
        
        return jsonify(response_data), 201
        
    except Exception as e:
        print(f"❌ Registration error: {str(e)}")
        traceback.print_exc()
        return jsonify({
            'success': False,
            'message': f'Registration failed: {str(e)}'
        }), 500

@auth_bp.route('/login', methods=['POST'])
def login():
    """Login user"""
    try:
        data = request.get_json()
        
        if not data or not data.get('email') or not data.get('password'):
            return jsonify({
                'success': False,
                'message': 'Email and password are required'
            }), 400
            
        user = User.authenticate(data['email'], data['password'])
        
        if not user:
            return jsonify({
                'success': False,
                'message': 'Invalid email or password'
            }), 401
            
        # Generate JWT with user_type included
        token = jwt.encode(
            {
                'user_id': user['id'],
                'email': user['email'],
                'user_type': user['user_type'],  # IMPORTANT: Include user_type
                'exp': datetime.utcnow() + timedelta(days=7)
            },
            current_app.config['JWT_SECRET_KEY'],
            algorithm='HS256'
        )
        
        response = {
            'success': True,
            'token': token,
            'user': user
        }
        
        # Add warning if not verified
        if not user.get('is_verified'):
            response['warning'] = 'Please verify your email address to receive notifications'
            response['needs_verification'] = True
        
        return jsonify(response)
        
    except Exception as e:
        print(f"❌ Login error: {str(e)}")
        return jsonify({
            'success': False,
            'message': 'Login failed'
        }), 500

@auth_bp.route('/verify-email/<token>', methods=['GET'])
def verify_email(token):
    """Verify email with token"""
    try:
        print(f"📧 Verifying email with token: {token[:20]}...")
        
        email = verify_verification_token(token)
        
        if not email:
            return jsonify({
                'success': False,
                'message': 'Invalid or expired verification link. Please request a new one.'
            }), 400
            
        user = User.find_by_email(email)
        
        if not user:
            return jsonify({
                'success': False,
                'message': 'User not found'
            }), 404
            
        if user.get('is_verified'):
            return jsonify({
                'success': True,
                'message': 'Email already verified'
            })
            
        # Mark user as verified
        User.verify_email(user['id'])
        
        print(f"✅ Email verified for {user['email']}")
        
        return jsonify({
            'success': True,
            'message': 'Email verified successfully! Welcome to FreelanceHub! 🎉'
        })
        
    except Exception as e:
        print(f"❌ Verification error: {str(e)}")
        traceback.print_exc()
        return jsonify({
            'success': False,
            'message': 'Server error during verification'
        }), 500

@auth_bp.route('/resend-verification', methods=['POST'])
def resend_verification():
    """Resend verification email"""
    try:
        # Get user from token
        auth_header = request.headers.get('Authorization', '')
        token = auth_header.replace('Bearer ', '') if auth_header else None
        
        if not token:
            return jsonify({
                'success': False,
                'message': 'Authentication required'
            }), 401
            
        try:
            payload = jwt.decode(
                token,
                current_app.config['JWT_SECRET_KEY'],
                algorithms=['HS256']
            )
            user_id = payload.get('user_id')
            user = User.find_by_id(user_id)
        except jwt.ExpiredSignatureError:
            return jsonify({
                'success': False,
                'message': 'Session expired. Please login again.'
            }), 401
        except jwt.InvalidTokenError:
            return jsonify({
                'success': False,
                'message': 'Invalid token'
            }), 401
        
        if not user:
            return jsonify({
                'success': False,
                'message': 'User not found'
            }), 404
            
        if user.get('is_verified'):
            return jsonify({
                'success': False,
                'message': 'Email already verified'
            }), 400
            
        # Send verification email
        if send_verification_email(user):
            return jsonify({
                'success': True,
                'message': 'Verification email sent successfully! Please check your inbox.'
            })
        else:
            return jsonify({
                'success': False,
                'message': 'Failed to send verification email. Please try again later.'
            }), 500
            
    except Exception as e:
        print(f"❌ Resend verification error: {str(e)}")
        return jsonify({
            'success': False,
            'message': 'Server error'
        }), 500

@auth_bp.route('/me', methods=['GET'])
def get_current_user():
    """Get current user info"""
    try:
        auth_header = request.headers.get('Authorization', '')
        token = auth_header.replace('Bearer ', '') if auth_header else None
        
        if not token:
            return jsonify({
                'success': False,
                'message': 'No token provided'
            }), 401
            
        try:
            payload = jwt.decode(
                token,
                current_app.config['JWT_SECRET_KEY'],
                algorithms=['HS256']
            )
            user_id = payload.get('user_id')
            user = User.find_by_id(user_id)
        except jwt.ExpiredSignatureError:
            return jsonify({
                'success': False,
                'message': 'Token expired'
            }), 401
        except jwt.InvalidTokenError:
            return jsonify({
                'success': False,
                'message': 'Invalid token'
            }), 401
        
        if not user:
            return jsonify({
                'success': False,
                'message': 'User not found'
            }), 404
            
        return jsonify({
            'success': True,
            'user': user
        })
        
    except Exception as e:
        print(f"❌ Get user error: {str(e)}")
        return jsonify({
            'success': False,
            'message': 'Server error'
        }), 500

# Debug endpoint to check token
@auth_bp.route('/debug-token', methods=['GET'])
def debug_token():
    """Debug endpoint to check token without requiring authentication"""
    auth_header = request.headers.get('Authorization', '')
    token = auth_header.replace('Bearer ', '') if auth_header else None
    
    if not token:
        return jsonify({'success': False, 'message': 'No token provided'})
    
    try:
        payload = jwt.decode(
            token,
            current_app.config['JWT_SECRET_KEY'],
            algorithms=['HS256']
        )
        return jsonify({
            'success': True,
            'payload': payload,
            'message': 'Token is valid'
        })
    except jwt.ExpiredSignatureError:
        return jsonify({'success': False, 'message': 'Token expired'})
    except jwt.InvalidTokenError as e:
        return jsonify({'success': False, 'message': f'Invalid token: {str(e)}'})
    except Exception as e:
        return jsonify({'success': False, 'message': f'Error: {str(e)}'})