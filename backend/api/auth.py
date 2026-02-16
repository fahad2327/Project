from flask import Blueprint, request, jsonify
from database.models import User
from utils.auth_utils import validate_email, validate_password, generate_token, decode_token
from datetime import timedelta
import os

auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')

@auth_bp.route('/register', methods=['POST'])
def register():
    """User registration endpoint"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['username', 'email', 'password', 'first_name', 'last_name', 'user_type']
        for field in required_fields:
            if field not in data or not data[field]:
                return jsonify({
                    'success': False,
                    'message': f'{field} is required'
                }), 400
        
        # Validate email
        if not validate_email(data['email']):
            return jsonify({
                'success': False,
                'message': 'Invalid email format'
            }), 400
        
        # Validate password strength
        is_valid, message = validate_password(data['password'])
        if not is_valid:
            return jsonify({
                'success': False,
                'message': message
            }), 400
        
        # Validate user type
        if data['user_type'] not in ['freelancer', 'recruiter']:
            return jsonify({
                'success': False,
                'message': 'Invalid user type'
            }), 400
        
        # Check if user exists
        existing_user = User.find_by_email(data['email'])
        if existing_user:
            return jsonify({
                'success': False,
                'message': 'Email already registered'
            }), 409
        
        existing_username = User.find_by_email(data['username'])
        if existing_username:
            return jsonify({
                'success': False,
                'message': 'Username already taken'
            }), 409
        
        # Create user
        user_id = User.create(
            username=data['username'],
            email=data['email'],
            password=data['password'],
            first_name=data['first_name'],
            last_name=data['last_name'],
            user_type=data['user_type']
        )
        
        # Generate tokens
        access_token = generate_token(
            user_id, 
            data['user_type'],
            timedelta(hours=1)
        )
        refresh_token = generate_token(
            user_id,
            data['user_type'],
            timedelta(days=7)
        )
        
        # Get user data
        user = User.find_by_id(user_id)
        if user and 'password_hash' in user:
            del user['password_hash']
        
        return jsonify({
            'success': True,
            'message': 'Registration successful',
            'access_token': access_token,
            'refresh_token': refresh_token,
            'user': user
        }), 201
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Registration failed: {str(e)}'
        }), 500

@auth_bp.route('/login', methods=['POST'])
def login():
    """User login endpoint"""
    try:
        data = request.get_json()
        
        if 'email' not in data or 'password' not in data:
            return jsonify({
                'success': False,
                'message': 'Email and password are required'
            }), 400
        
        # Authenticate user
        user = User.authenticate(data['email'], data['password'])
        
        if not user:
            return jsonify({
                'success': False,
                'message': 'Invalid email or password'
            }), 401
        
        # Generate tokens
        access_token = generate_token(
            user['id'],
            user['user_type'],
            timedelta(hours=1)
        )
        refresh_token = generate_token(
            user['id'],
            user['user_type'],
            timedelta(days=7)
        )
        
        return jsonify({
            'success': True,
            'message': 'Login successful',
            'access_token': access_token,
            'refresh_token': refresh_token,
            'user': user
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Login failed: {str(e)}'
        }), 500

@auth_bp.route('/refresh', methods=['POST'])
def refresh():
    """Refresh access token"""
    try:
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return jsonify({
                'success': False,
                'message': 'Refresh token is required'
            }), 401
        
        token = auth_header.split(" ")[1]
        payload = decode_token(token)
        
        if not payload:
            return jsonify({
                'success': False,
                'message': 'Invalid or expired refresh token'
            }), 401
        
        # Generate new access token
        access_token = generate_token(
            payload['user_id'],
            payload['user_type'],
            timedelta(hours=1)
        )
        
        return jsonify({
            'success': True,
            'access_token': access_token
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Token refresh failed: {str(e)}'
        }), 500

@auth_bp.route('/me', methods=['GET'])
def get_current_user():
    """Get current user"""
    from utils.auth_utils import token_required, decode_token
    
    auth_header = request.headers.get('Authorization')
    if not auth_header:
        return jsonify({
            'success': False,
            'message': 'Token is required'
        }), 401
    
    token = auth_header.split(" ")[1]
    payload = decode_token(token)
    
    if not payload:
        return jsonify({
            'success': False,
            'message': 'Invalid or expired token'
        }), 401
    
    user = User.find_by_id(payload['user_id'])
    if not user:
        return jsonify({
            'success': False,
            'message': 'User not found'
        }), 404
    
    if 'password_hash' in user:
        del user['password_hash']
    
    return jsonify({
        'success': True,
        'user': user
    }), 200

@auth_bp.route('/logout', methods=['POST'])
def logout():
    """User logout endpoint"""
    return jsonify({
        'success': True,
        'message': 'Logout successful'
    }), 200