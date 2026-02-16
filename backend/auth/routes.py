from flask import Blueprint, request, jsonify
from flask_jwt_extended import (
    create_access_token, 
    create_refresh_token,
    jwt_required, 
    get_jwt_identity,
    unset_jwt_cookies  # Fixed: removed 'python' and corrected the import
)
from datetime import timedelta, datetime
import os
from database.db_config import get_db_connection
from auth.utils import (
    hash_password, 
    check_password, 
    validate_email_format,
    validate_password_strength,
    sanitize_input
)

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/api/auth/register', methods=['POST'])
def register():
    """User registration endpoint"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['name', 'email', 'password']
        for field in required_fields:
            if field not in data or not data[field]:
                return jsonify({
                    'success': False,
                    'message': f'{field} is required'
                }), 400
        
        # Sanitize inputs
        name = sanitize_input(data['name'])
        email = sanitize_input(data['email'])
        password = data['password']
        
        # Validate email
        is_valid_email, email_result = validate_email_format(email)
        if not is_valid_email:
            return jsonify({
                'success': False,
                'message': email_result
            }), 400
        
        # Validate password strength
        is_valid_password, password_message = validate_password_strength(password)
        if not is_valid_password:
            return jsonify({
                'success': False,
                'message': password_message
            }), 400
        
        # Check if user already exists
        connection = get_db_connection()
        cursor = connection.cursor()
        
        cursor.execute("SELECT id FROM users WHERE email = %s", (email,))
        existing_user = cursor.fetchone()
        
        if existing_user:
            cursor.close()
            connection.close()
            return jsonify({
                'success': False,
                'message': 'Email already registered'
            }), 409
        
        # Hash password and create user
        password_hash = hash_password(password)
        
        cursor.execute("""
            INSERT INTO users (name, email, password_hash)
            VALUES (%s, %s, %s)
        """, (name, email, password_hash))
        
        user_id = cursor.lastrowid
        
        # Create empty profile for user
        cursor.execute("""
            INSERT INTO user_profiles (user_id)
            VALUES (%s)
        """, (user_id,))
        
        connection.commit()
        
        # Generate tokens
        access_token = create_access_token(
            identity=user_id,
            additional_claims={"email": email, "name": name},
            expires_delta=timedelta(hours=1)
        )
        refresh_token = create_refresh_token(
            identity=user_id,
            expires_delta=timedelta(days=30)
        )
        
        cursor.close()
        connection.close()
        
        return jsonify({
            'success': True,
            'message': 'Registration successful',
            'access_token': access_token,
            'refresh_token': refresh_token,
            'user': {
                'id': user_id,
                'name': name,
                'email': email
            }
        }), 201
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Registration failed: {str(e)}'
        }), 500

@auth_bp.route('/api/auth/login', methods=['POST'])
def login():
    """User login endpoint"""
    try:
        data = request.get_json()
        
        # Validate required fields
        if 'email' not in data or 'password' not in data:
            return jsonify({
                'success': False,
                'message': 'Email and password are required'
            }), 400
        
        email = sanitize_input(data['email'])
        password = data['password']
        
        connection = get_db_connection()
        cursor = connection.cursor()
        
        # Get user from database
        cursor.execute("""
            SELECT id, name, email, password_hash 
            FROM users 
            WHERE email = %s AND is_active = TRUE
        """, (email,))
        
        user = cursor.fetchone()
        
        if not user or not check_password(password, user['password_hash']):
            cursor.close()
            connection.close()
            return jsonify({
                'success': False,
                'message': 'Invalid email or password'
            }), 401
        
        # Update last login
        cursor.execute("""
            UPDATE users 
            SET last_login = CURRENT_TIMESTAMP 
            WHERE id = %s
        """, (user['id'],))
        
        connection.commit()
        
        # Generate tokens
        access_token = create_access_token(
            identity=user['id'],
            additional_claims={
                "email": user['email'],
                "name": user['name']
            },
            expires_delta=timedelta(hours=1)
        )
        refresh_token = create_refresh_token(
            identity=user['id'],
            expires_delta=timedelta(days=30)
        )
        
        cursor.close()
        connection.close()
        
        return jsonify({
            'success': True,
            'message': 'Login successful',
            'access_token': access_token,
            'refresh_token': refresh_token,
            'user': {
                'id': user['id'],
                'name': user['name'],
                'email': user['email']
            }
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Login failed: {str(e)}'
        }), 500

@auth_bp.route('/api/auth/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    """Refresh access token"""
    try:
        current_user_id = get_jwt_identity()
        
        connection = get_db_connection()
        cursor = connection.cursor()
        
        cursor.execute("""
            SELECT id, name, email 
            FROM users 
            WHERE id = %s AND is_active = TRUE
        """, (current_user_id,))
        
        user = cursor.fetchone()
        cursor.close()
        connection.close()
        
        if not user:
            return jsonify({
                'success': False,
                'message': 'User not found'
            }), 404
        
        # Create new access token
        access_token = create_access_token(
            identity=user['id'],
            additional_claims={
                "email": user['email'],
                "name": user['name']
            },
            expires_delta=timedelta(hours=1)
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

@auth_bp.route('/api/auth/logout', methods=['POST'])
@jwt_required()
def logout():
    """User logout endpoint"""
    try:
        response = jsonify({
            'success': True,
            'message': 'Logout successful'
        })
        unset_jwt_cookies(response)
        return response, 200
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Logout failed: {str(e)}'
        }), 500

@auth_bp.route('/api/auth/me', methods=['GET'])
@jwt_required()
def get_current_user():
    """Get current user information"""
    try:
        current_user_id = get_jwt_identity()
        
        connection = get_db_connection()
        cursor = connection.cursor()
        
        cursor.execute("""
            SELECT u.id, u.name, u.email, u.created_at, u.last_login,
                   up.phone, up.address, up.skills, up.bio, up.profile_picture
            FROM users u
            LEFT JOIN user_profiles up ON u.id = up.user_id
            WHERE u.id = %s AND u.is_active = TRUE
        """, (current_user_id,))
        
        user = cursor.fetchone()
        cursor.close()
        connection.close()
        
        if not user:
            return jsonify({
                'success': False,
                'message': 'User not found'
            }), 404
        
        return jsonify({
            'success': True,
            'user': user
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Failed to fetch user: {str(e)}'
        }), 500

@auth_bp.route('/api/auth/update-profile', methods=['PUT'])
@jwt_required()
def update_profile():
    """Update user profile"""
    try:
        current_user_id = get_jwt_identity()
        data = request.get_json()
        
        connection = get_db_connection()
        cursor = connection.cursor()
        
        # Update user_profiles table
        update_fields = []
        values = []
        
        profile_fields = ['phone', 'address', 'skills', 'bio']
        for field in profile_fields:
            if field in data:
                update_fields.append(f"{field} = %s")
                values.append(sanitize_input(data[field]))
        
        if update_fields:
            values.append(current_user_id)
            query = f"""
                UPDATE user_profiles 
                SET {', '.join(update_fields)}
                WHERE user_id = %s
            """
            cursor.execute(query, values)
        
        # Update user name if provided
        if 'name' in data and data['name']:
            cursor.execute("""
                UPDATE users 
                SET name = %s 
                WHERE id = %s
            """, (sanitize_input(data['name']), current_user_id))
        
        connection.commit()
        cursor.close()
        connection.close()
        
        return jsonify({
            'success': True,
            'message': 'Profile updated successfully'
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Failed to update profile: {str(e)}'
        }), 500

@auth_bp.route('/api/auth/change-password', methods=['POST'])
@jwt_required()
def change_password():
    """Change user password"""
    try:
        current_user_id = get_jwt_identity()
        data = request.get_json()
        
        if 'current_password' not in data or 'new_password' not in data:
            return jsonify({
                'success': False,
                'message': 'Current password and new password are required'
            }), 400
        
        connection = get_db_connection()
        cursor = connection.cursor()
        
        # Get current password hash
        cursor.execute("""
            SELECT password_hash 
            FROM users 
            WHERE id = %s
        """, (current_user_id,))
        
        user = cursor.fetchone()
        
        if not user or not check_password(data['current_password'], user['password_hash']):
            cursor.close()
            connection.close()
            return jsonify({
                'success': False,
                'message': 'Current password is incorrect'
            }), 401
        
        # Validate new password
        is_valid, message = validate_password_strength(data['new_password'])
        if not is_valid:
            cursor.close()
            connection.close()
            return jsonify({
                'success': False,
                'message': message
            }), 400
        
        # Update password
        new_password_hash = hash_password(data['new_password'])
        cursor.execute("""
            UPDATE users 
            SET password_hash = %s 
            WHERE id = %s
        """, (new_password_hash, current_user_id))
        
        connection.commit()
        cursor.close()
        connection.close()
        
        return jsonify({
            'success': True,
            'message': 'Password changed successfully'
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Failed to change password: {str(e)}'
        }), 500