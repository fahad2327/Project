import bcrypt
import re
import jwt
from datetime import datetime, timedelta
from functools import wraps
from flask import request, jsonify, current_app
import os

def hash_password(password):
    """Hash a password using bcrypt"""
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')

def check_password(password, hashed):
    """Verify a password against its hash"""
    return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))

def validate_email(email):
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_password(password):
    """Validate password strength"""
    errors = []
    if len(password) < 8:
        errors.append("Password must be at least 8 characters long")
    if not re.search(r"[A-Z]", password):
        errors.append("Password must contain at least one uppercase letter")
    if not re.search(r"[a-z]", password):
        errors.append("Password must contain at least one lowercase letter")
    if not re.search(r"\d", password):
        errors.append("Password must contain at least one number")
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        errors.append("Password must contain at least one special character")
    
    return len(errors) == 0, ", ".join(errors) if errors else "Password is valid"

def generate_token(user_id, user_type, expires_delta=None):
    """Generate JWT token"""
    payload = {
        'user_id': user_id,
        'user_type': user_type,
        'exp': datetime.utcnow() + (expires_delta or timedelta(hours=1))
    }
    return jwt.encode(payload, os.getenv('JWT_SECRET_KEY'), algorithm='HS256')

def decode_token(token):
    """Decode JWT token"""
    try:
        payload = jwt.decode(token, os.getenv('JWT_SECRET_KEY'), algorithms=['HS256'])
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

def token_required(f):
    """Decorator to require valid JWT token"""
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            try:
                token = auth_header.split(" ")[1]
            except IndexError:
                return jsonify({'success': False, 'message': 'Invalid token format'}), 401
        
        if not token:
            return jsonify({'success': False, 'message': 'Token is missing'}), 401
        
        payload = decode_token(token)
        if not payload:
            return jsonify({'success': False, 'message': 'Invalid or expired token'}), 401
        
        request.user_id = payload['user_id']
        request.user_type = payload['user_type']
        
        return f(*args, **kwargs)
    
    return decorated

def freelancer_required(f):
    """Decorator to require freelancer role"""
    @wraps(f)
    def decorated(*args, **kwargs):
        if request.user_type != 'freelancer':
            return jsonify({'success': False, 'message': 'Freelancer access required'}), 403
        return f(*args, **kwargs)
    return decorated

def recruiter_required(f):
    """Decorator to require recruiter role"""
    @wraps(f)
    def decorated(*args, **kwargs):
        if request.user_type != 'recruiter':
            return jsonify({'success': False, 'message': 'Recruiter access required'}), 403
        return f(*args, **kwargs)
    return decorated

def sanitize_input(data):
    """Basic input sanitization"""
    if isinstance(data, str):
        data = data.strip()
        data = re.sub(r'[<>"\']', '', data)
    return data