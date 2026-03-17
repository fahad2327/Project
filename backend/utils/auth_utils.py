# # # import bcrypt
# # # import re
# # # import jwt
# # # from datetime import datetime, timedelta
# # # from functools import wraps
# # # from flask import request, jsonify, current_app
# # # import os

# # # def hash_password(password):
# # #     """Hash a password using bcrypt"""
# # #     salt = bcrypt.gensalt()
# # #     return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')

# # # def check_password(password, hashed):
# # #     """Verify a password against its hash"""
# # #     return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))

# # # def validate_email(email):
# # #     """Validate email format"""
# # #     pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
# # #     return re.match(pattern, email) is not None

# # # def validate_password(password):
# # #     """Validate password strength"""
# # #     errors = []
# # #     if len(password) < 8:
# # #         errors.append("Password must be at least 8 characters long")
# # #     if not re.search(r"[A-Z]", password):
# # #         errors.append("Password must contain at least one uppercase letter")
# # #     if not re.search(r"[a-z]", password):
# # #         errors.append("Password must contain at least one lowercase letter")
# # #     if not re.search(r"\d", password):
# # #         errors.append("Password must contain at least one number")
# # #     if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
# # #         errors.append("Password must contain at least one special character")
    
# # #     return len(errors) == 0, ", ".join(errors) if errors else "Password is valid"

# # # def generate_token(user_id, user_type, expires_delta=None):
# # #     """Generate JWT token"""
# # #     payload = {
# # #         'user_id': user_id,
# # #         'user_type': user_type,
# # #         'exp': datetime.utcnow() + (expires_delta or timedelta(hours=1))
# # #     }
# # #     return jwt.encode(payload, os.getenv('JWT_SECRET_KEY'), algorithm='HS256')

# # # def decode_token(token):
# # #     """Decode JWT token"""
# # #     try:
# # #         payload = jwt.decode(token, os.getenv('JWT_SECRET_KEY'), algorithms=['HS256'])
# # #         return payload
# # #     except jwt.ExpiredSignatureError:
# # #         return None
# # #     except jwt.InvalidTokenError:
# # #         return None

# # # def token_required(f):
# # #     """Decorator to require valid JWT token"""
# # #     @wraps(f)
# # #     def decorated(*args, **kwargs):
# # #         token = None
        
# # #         if 'Authorization' in request.headers:
# # #             auth_header = request.headers['Authorization']
# # #             try:
# # #                 token = auth_header.split(" ")[1]
# # #             except IndexError:
# # #                 return jsonify({'success': False, 'message': 'Invalid token format'}), 401
        
# # #         if not token:
# # #             return jsonify({'success': False, 'message': 'Token is missing'}), 401
        
# # #         payload = decode_token(token)
# # #         if not payload:
# # #             return jsonify({'success': False, 'message': 'Invalid or expired token'}), 401
        
# # #         request.user_id = payload['user_id']
# # #         request.user_type = payload['user_type']
        
# # #         return f(*args, **kwargs)
    
# # #     return decorated

# # # def freelancer_required(f):
# # #     """Decorator to require freelancer role"""
# # #     @wraps(f)
# # #     def decorated(*args, **kwargs):
# # #         if request.user_type != 'freelancer':
# # #             return jsonify({'success': False, 'message': 'Freelancer access required'}), 403
# # #         return f(*args, **kwargs)
# # #     return decorated

# # # def recruiter_required(f):
# # #     """Decorator to require recruiter role"""
# # #     @wraps(f)
# # #     def decorated(*args, **kwargs):
# # #         if request.user_type != 'recruiter':
# # #             return jsonify({'success': False, 'message': 'Recruiter access required'}), 403
# # #         return f(*args, **kwargs)
# # #     return decorated

# # # def sanitize_input(data):
# # #     """Basic input sanitization"""
# # #     if isinstance(data, str):
# # #         data = data.strip()
# # #         data = re.sub(r'[<>"\']', '', data)
# # #     return data
# # # utils/auth_utils.py
# # import jwt
# # from functools import wraps
# # from flask import request, jsonify, current_app
# # import bcrypt
# # import re
# # from email_validator import validate_email, EmailNotValidError

# # def hash_password(password):
# #     """Hash a password using bcrypt"""
# #     salt = bcrypt.gensalt()
# #     return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')

# # def check_password(password, hashed):
# #     """Verify a password against its hash"""
# #     return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))

# # def validate_email_format(email):
# #     """Validate email format"""
# #     try:
# #         valid = validate_email(email)
# #         return True, valid.email
# #     except EmailNotValidError as e:
# #         return False, str(e)

# # def validate_password_strength(password):
# #     """
# #     Validate password strength:
# #     - At least 8 characters
# #     - At least one uppercase letter
# #     - At least one lowercase letter
# #     - At least one number
# #     - At least one special character
# #     """
# #     if len(password) < 8:
# #         return False, "Password must be at least 8 characters long"
    
# #     if not re.search(r"[A-Z]", password):
# #         return False, "Password must contain at least one uppercase letter"
    
# #     if not re.search(r"[a-z]", password):
# #         return False, "Password must contain at least one lowercase letter"
    
# #     if not re.search(r"\d", password):
# #         return False, "Password must contain at least one number"
    
# #     if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
# #         return False, "Password must contain at least one special character"
    
# #     return True, "Password is valid"

# # def sanitize_input(data):
# #     """Basic input sanitization"""
# #     if isinstance(data, str):
# #         data = data.strip()
# #         data = re.sub(r'[<>"\']', '', data)
# #     return data

# # def token_required(f):
# #     @wraps(f)
# #     def decorated(*args, **kwargs):
# #         token = None
        
# #         if 'Authorization' in request.headers:
# #             auth_header = request.headers['Authorization']
# #             try:
# #                 token = auth_header.split(" ")[1]
# #             except IndexError:
# #                 return jsonify({'success': False, 'message': 'Invalid token format'}), 401
        
# #         if not token:
# #             return jsonify({'success': False, 'message': 'Token is missing'}), 401
        
# #         try:
# #             # Decode token
# #             payload = jwt.decode(
# #                 token, 
# #                 current_app.config['JWT_SECRET_KEY'], 
# #                 algorithms=['HS256']
# #             )
            
# #             # Set user_id in request
# #             request.user_id = payload['user_id']
            
# #             # Set user_type if it exists, otherwise set a default or None
# #             request.user_type = payload.get('user_type', None)
            
# #         except jwt.ExpiredSignatureError:
# #             return jsonify({'success': False, 'message': 'Token expired'}), 401
# #         except jwt.InvalidTokenError:
# #             return jsonify({'success': False, 'message': 'Invalid token'}), 401
        
# #         return f(*args, **kwargs)
    
# #     return decorated

# # def freelancer_required(f):
# #     @wraps(f)
# #     def decorated(*args, **kwargs):
# #         if getattr(request, 'user_type', None) != 'freelancer':
# #             return jsonify({'success': False, 'message': 'Freelancer access required'}), 403
# #         return f(*args, **kwargs)
# #     return decorated

# # def recruiter_required(f):
# #     @wraps(f)
# #     def decorated(*args, **kwargs):
# #         if getattr(request, 'user_type', None) != 'recruiter':
# #             return jsonify({'success': False, 'message': 'Recruiter access required'}), 403
# #         return f(*args, **kwargs)
# #     return decorated
# import jwt
# from functools import wraps
# from flask import request, jsonify, current_app, g
# import bcrypt
# import re
# from email_validator import validate_email, EmailNotValidError

# def hash_password(password):
#     """Hash a password using bcrypt"""
#     salt = bcrypt.gensalt()
#     return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')

# def check_password(password, hashed):
#     """Verify a password against its hash"""
#     return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))

# def validate_email_format(email):
#     """Validate email format"""
#     try:
#         valid = validate_email(email)
#         return True, valid.email
#     except EmailNotValidError as e:
#         return False, str(e)

# def validate_password_strength(password):
#     """Validate password strength"""
#     if len(password) < 8:
#         return False, "Password must be at least 8 characters long"
    
#     if not re.search(r"[A-Z]", password):
#         return False, "Password must contain at least one uppercase letter"
    
#     if not re.search(r"[a-z]", password):
#         return False, "Password must contain at least one lowercase letter"
    
#     if not re.search(r"\d", password):
#         return False, "Password must contain at least one number"
    
#     if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
#         return False, "Password must contain at least one special character"
    
#     return True, "Password is valid"

# def sanitize_input(data):
#     """Basic input sanitization"""
#     if isinstance(data, str):
#         data = data.strip()
#         data = re.sub(r'[<>"\']', '', data)
#     return data

# def token_required(f):
#     @wraps(f)
#     def decorated(*args, **kwargs):
#         token = None
        
#         print("🔐 Token verification started")
        
#         if 'Authorization' in request.headers:
#             auth_header = request.headers['Authorization']
#             print(f"📨 Auth header: {auth_header[:30]}...")
#             try:
#                 token = auth_header.split(" ")[1]
#                 print(f"🔑 Token extracted: {token[:20]}...")
#             except IndexError:
#                 print("❌ Invalid token format")
#                 return jsonify({'success': False, 'message': 'Invalid token format'}), 401
        
#         if not token:
#             print("❌ No token provided")
#             return jsonify({'success': False, 'message': 'Token is missing'}), 401
        
#         try:
#             # Decode token
#             payload = jwt.decode(
#                 token, 
#                 current_app.config['JWT_SECRET_KEY'], 
#                 algorithms=['HS256']
#             )
            
#             print(f"✅ Token decoded successfully")
#             print(f"📦 Payload contents: {payload}")
            
#             # Set user_id in request
#             request.user_id = payload['user_id']
            
#             # Set user_type if it exists
#             if 'user_type' in payload:
#                 request.user_type = payload['user_type']
#                 print(f"👤 User type from token: {request.user_type}")
#             else:
#                 print("⚠️ No user_type in token payload")
#                 request.user_type = None
            
#         except jwt.ExpiredSignatureError:
#             print("❌ Token expired")
#             return jsonify({'success': False, 'message': 'Token expired'}), 401
#         except jwt.InvalidTokenError as e:
#             print(f"❌ Invalid token: {e}")
#             return jsonify({'success': False, 'message': 'Invalid token'}), 401
        
#         return f(*args, **kwargs)
    
#     return decorated

# def freelancer_required(f):
#     @wraps(f)
#     def decorated(*args, **kwargs):
#         # Get user_type from request
#         user_type = getattr(request, 'user_type', None)
        
#         print(f"🔍 Freelancer access check:")
#         print(f"   - user_id: {getattr(request, 'user_id', 'Not set')}")
#         print(f"   - user_type: {user_type}")
#         print(f"   - Required: freelancer")
        
#         if user_type is None:
#             print("❌ user_type is None - token might not contain user_type claim")
#             return jsonify({
#                 'success': False, 
#                 'message': 'User type not found in token. Please login again.'
#             }), 403
            
#         if user_type != 'freelancer':
#             print(f"❌ Access denied: user_type={user_type}, required=freelancer")
#             return jsonify({
#                 'success': False, 
#                 'message': f'Freelancer access required. Current user type: {user_type}'
#             }), 403
        
#         print("✅ Freelancer access granted")
#         return f(*args, **kwargs)
#     return decorated

# def recruiter_required(f):
#     @wraps(f)
#     def decorated(*args, **kwargs):
#         user_type = getattr(request, 'user_type', None)
        
#         print(f"🔍 Recruiter access check: user_type={user_type}")
        
#         if user_type is None:
#             print("❌ user_type is None")
#             return jsonify({
#                 'success': False, 
#                 'message': 'User type not found in token. Please login again.'
#             }), 403
            
#         if user_type != 'recruiter':
#             print(f"❌ Access denied: user_type={user_type}, required=recruiter")
#             return jsonify({
#                 'success': False, 
#                 'message': f'Recruiter access required. Current user type: {user_type}'
#             }), 403
        
#         print("✅ Recruiter access granted")
#         return f(*args, **kwargs)
#     return decorated
import re
import jwt
import bcrypt
from datetime import datetime, timedelta
from flask import current_app, request, jsonify
from functools import wraps

def validate_email(email):
    if not email:
        return False
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_password(password):
    if not password:
        return False, "Password is required"
    if len(password) < 8:
        return False, "Password must be at least 8 characters long"
    if not re.search(r"[A-Z]", password):
        return False, "Password must contain at least one uppercase letter"
    if not re.search(r"[a-z]", password):
        return False, "Password must contain at least one lowercase letter"
    if not re.search(r"\d", password):
        return False, "Password must contain at least one number"
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        return False, "Password must contain at least one special character"
    return True, "Password is valid"

def hash_password(password):
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')

def check_password(password, hashed):
    return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))

def generate_token(user_id, user_type, expires_delta=None):
    if expires_delta is None:
        expires_delta = timedelta(hours=1)
    payload = {
        'user_id': user_id,
        'user_type': user_type,
        'exp': datetime.utcnow() + expires_delta,
        'iat': datetime.utcnow()
    }
    return jwt.encode(payload, current_app.config['JWT_SECRET_KEY'], algorithm='HS256')

def decode_token(token):
    try:
        return jwt.decode(token, current_app.config['JWT_SECRET_KEY'], algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        auth_header = request.headers.get('Authorization')
        if auth_header and auth_header.startswith('Bearer '):
            token = auth_header.split(' ')[1]
        if not token:
            return jsonify({'success': False, 'message': 'Token is missing'}), 401
        payload = decode_token(token)
        if not payload:
            return jsonify({'success': False, 'message': 'Invalid or expired token'}), 401
        request.user_id = payload.get('user_id')
        request.user_type = payload.get('user_type')
        return f(*args, **kwargs)
    return decorated

def freelancer_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not hasattr(request, 'user_type') or request.user_type != 'freelancer':
            return jsonify({'success': False, 'message': 'Freelancer access required'}), 403
        return f(*args, **kwargs)
    return decorated

def recruiter_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not hasattr(request, 'user_type') or request.user_type != 'recruiter':
            return jsonify({'success': False, 'message': 'Recruiter access required'}), 403
        return f(*args, **kwargs)
    return decorated