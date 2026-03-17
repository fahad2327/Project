# # # # # # # from flask import Flask, jsonify
# # # # # # # from flask_cors import CORS
# # # # # # # from flask_jwt_extended import JWTManager
# # # # # # # from dotenv import load_dotenv
# # # # # # # import os

# # # # # # # # Load environment variables
# # # # # # # load_dotenv()

# # # # # # # # Import database initializer
# # # # # # # from database.db_config import init_database

# # # # # # # # Import blueprints
# # # # # # # from api.auth import auth_bp
# # # # # # # from api.freelancer import freelancer_bp
# # # # # # # from api.recruiter import recruiter_bp
# # # # # # # from api.jobs import jobs_bp
# # # # # # # from api.notifications import notifications_bp

# # # # # # # def create_app():
# # # # # # #     app = Flask(__name__)
    
# # # # # # #     # Configuration
# # # # # # #     app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
# # # # # # #     app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
    
# # # # # # #     # CORS configuration
# # # # # # #     cors_origins = os.getenv('CORS_ORIGINS', 'http://localhost:3000').split(',')
# # # # # # #     CORS(app, origins=cors_origins, supports_credentials=True)
    
# # # # # # #     # Initialize JWT
# # # # # # #     jwt = JWTManager(app)
    
# # # # # # #     # Register blueprints
# # # # # # #     app.register_blueprint(auth_bp)
# # # # # # #     app.register_blueprint(freelancer_bp)
# # # # # # #     app.register_blueprint(recruiter_bp)
# # # # # # #     app.register_blueprint(jobs_bp)
# # # # # # #     app.register_blueprint(notifications_bp)
    
# # # # # # #     # Initialize database
# # # # # # #     with app.app_context():
# # # # # # #         try:
# # # # # # #             init_database()
# # # # # # #             print("✅ Database initialized successfully")
# # # # # # #         except Exception as e:
# # # # # # #             print(f"❌ Database initialization failed: {e}")
    
# # # # # # #     # Health check endpoint
# # # # # # #     @app.route('/api/health', methods=['GET'])
# # # # # # #     def health_check():
# # # # # # #         return jsonify({
# # # # # # #             'success': True,
# # # # # # #             'status': 'healthy',
# # # # # # #             'message': 'Freelancer Platform API is running',
# # # # # # #             'version': '1.0.0'
# # # # # # #         }), 200
    
# # # # # # #     # Error handlers
# # # # # # #     @app.errorhandler(404)
# # # # # # #     def not_found(error):
# # # # # # #         return jsonify({
# # # # # # #             'success': False,
# # # # # # #             'message': 'Resource not found'
# # # # # # #         }), 404
    
# # # # # # #     @app.errorhandler(500)
# # # # # # #     def internal_error(error):
# # # # # # #         return jsonify({
# # # # # # #             'success': False,
# # # # # # #             'message': 'Internal server error'
# # # # # # #         }), 500
    
# # # # # # #     return app

# # # # # # # if __name__ == '__main__':
# # # # # # #     app = create_app()
# # # # # # #     port = int(os.getenv('PORT', 5000))
# # # # # # #     debug = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    
# # # # # # #     app.run(
# # # # # # #         host='0.0.0.0',
# # # # # # #         port=port,
# # # # # # #         debug=debug
# # # # # # #     )
# # # # # # # app.py - Make sure you don't have SQLAlchemy initialized

# # # # # # from flask import Flask, jsonify
# # # # # # from flask_cors import CORS
# # # # # # from flask_jwt_extended import JWTManager
# # # # # # from flask_mail import Mail
# # # # # # from dotenv import load_dotenv
# # # # # # import os

# # # # # # # Load environment variables
# # # # # # load_dotenv()

# # # # # # # Import blueprints
# # # # # # from api.auth import auth_bp, mail
# # # # # # from api.freelancer import freelancer_bp
# # # # # # from api.recruiter import recruiter_bp
# # # # # # from api.jobs import jobs_bp
# # # # # # from api.notifications import notifications_bp

# # # # # # def create_app():
# # # # # #     app = Flask(__name__)
    
# # # # # #     # Configuration
# # # # # #     app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
# # # # # #     app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'jwt-secret-key-change-in-production')
    
# # # # # #     # CORS configuration
# # # # # #     cors_origins = os.getenv('CORS_ORIGINS', 'http://localhost:3000').split(',')
# # # # # #     CORS(app, origins=cors_origins, supports_credentials=True)
    
# # # # # #     # Email Configuration
# # # # # #     app.config['MAIL_SERVER'] = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
# # # # # #     app.config['MAIL_PORT'] = int(os.getenv('SMTP_PORT', 587))
# # # # # #     app.config['MAIL_USE_TLS'] = os.getenv('MAIL_USE_TLS', 'True').lower() == 'true'
# # # # # #     app.config['MAIL_USERNAME'] = os.getenv('SMTP_USERNAME')
# # # # # #     app.config['MAIL_PASSWORD'] = os.getenv('SMTP_PASSWORD')
# # # # # #     app.config['MAIL_DEFAULT_SENDER'] = os.getenv('FROM_EMAIL', 'noreply@freelancehub.com')
    
# # # # # #     # Custom app config
# # # # # #     app.config['BASE_URL'] = os.getenv('BASE_URL', 'http://localhost:3000')
# # # # # #     app.config['FROM_EMAIL'] = os.getenv('FROM_EMAIL', 'noreply@freelancehub.com')
# # # # # #     app.config['FROM_NAME'] = os.getenv('FROM_NAME', 'FreelanceHub')
    
# # # # # #     # Initialize extensions
# # # # # #     mail.init_app(app)
# # # # # #     jwt = JWTManager(app)
    
# # # # # #     # Register blueprints
# # # # # #     app.register_blueprint(auth_bp)
# # # # # #     app.register_blueprint(freelancer_bp)
# # # # # #     app.register_blueprint(recruiter_bp)
# # # # # #     app.register_blueprint(jobs_bp)
# # # # # #     app.register_blueprint(notifications_bp)
    
# # # # # #     # Health check endpoint
# # # # # #     @app.route('/api/health', methods=['GET'])
# # # # # #     def health_check():
# # # # # #         return jsonify({
# # # # # #             'success': True,
# # # # # #             'status': 'healthy',
# # # # # #             'message': 'Freelancer Platform API is running',
# # # # # #             'version': '1.0.0'
# # # # # #         }), 200
    
# # # # # #     # Error handlers
# # # # # #     @app.errorhandler(404)
# # # # # #     def not_found(error):
# # # # # #         return jsonify({
# # # # # #             'success': False,
# # # # # #             'message': 'Resource not found'
# # # # # #         }), 404
    
# # # # # #     @app.errorhandler(500)
# # # # # #     def internal_error(error):
# # # # # #         return jsonify({
# # # # # #             'success': False,
# # # # # #             'message': 'Internal server error'
# # # # # #         }), 500
    
# # # # # #     return app

# # # # # # if __name__ == '__main__':
# # # # # #     app = create_app()
# # # # # #     port = int(os.getenv('PORT', 5000))
# # # # # #     debug = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    
# # # # # #     app.run(
# # # # # #         host='0.0.0.0',
# # # # # #         port=port,
# # # # # #         debug=debug
# # # # # #     )
# # # # # # app.py

# # # # # from flask import Flask, jsonify
# # # # # from flask_cors import CORS
# # # # # from flask_jwt_extended import JWTManager
# # # # # from flask_mail import Mail
# # # # # from dotenv import load_dotenv
# # # # # import os

# # # # # # Load environment variables
# # # # # load_dotenv()

# # # # # # Import blueprints
# # # # # from api.auth import auth_bp, mail
# # # # # from api.freelancer import freelancer_bp
# # # # # from api.recruiter import recruiter_bp
# # # # # from api.jobs import jobs_bp
# # # # # from api.notifications import notifications_bp

# # # # # def create_app():
# # # # #     app = Flask(__name__)
    
# # # # #     # Configuration
# # # # #     app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
# # # # #     app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'jwt-secret-key-change-in-production')
    
# # # # #     # CORS configuration
# # # # #     cors_origins = os.getenv('CORS_ORIGINS', 'http://localhost:3000').split(',')
# # # # #     CORS(app, origins=cors_origins, supports_credentials=True)
    
# # # # #     # Email Configuration
# # # # #     app.config['MAIL_SERVER'] = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
# # # # #     app.config['MAIL_PORT'] = int(os.getenv('SMTP_PORT', 587))
# # # # #     app.config['MAIL_USE_TLS'] = os.getenv('MAIL_USE_TLS', 'True').lower() == 'true'
# # # # #     app.config['MAIL_USERNAME'] = os.getenv('SMTP_USERNAME')
# # # # #     app.config['MAIL_PASSWORD'] = os.getenv('SMTP_PASSWORD')
# # # # #     app.config['MAIL_DEFAULT_SENDER'] = os.getenv('FROM_EMAIL', 'noreply@freelancehub.com')
    
# # # # #     # Custom app config
# # # # #     app.config['BASE_URL'] = os.getenv('BASE_URL', 'http://localhost:3000')
# # # # #     app.config['FROM_EMAIL'] = os.getenv('FROM_EMAIL', 'noreply@freelancehub.com')
# # # # #     app.config['FROM_NAME'] = os.getenv('FROM_NAME', 'FreelanceHub')
    
# # # # #     # Initialize extensions
# # # # #     mail.init_app(app)
# # # # #     jwt = JWTManager(app)
    
# # # # #     # Register blueprints
# # # # #     app.register_blueprint(auth_bp)
# # # # #     app.register_blueprint(freelancer_bp)
# # # # #     app.register_blueprint(recruiter_bp)
# # # # #     app.register_blueprint(jobs_bp)
# # # # #     app.register_blueprint(notifications_bp)
    
# # # # #     # Health check endpoint
# # # # #     @app.route('/api/health', methods=['GET'])
# # # # #     def health_check():
# # # # #         return jsonify({
# # # # #             'success': True,
# # # # #             'status': 'healthy',
# # # # #             'message': 'Freelancer Platform API is running',
# # # # #             'version': '1.0.0'
# # # # #         }), 200
    
# # # # #     # Error handlers
# # # # #     @app.errorhandler(404)
# # # # #     def not_found(error):
# # # # #         return jsonify({
# # # # #             'success': False,
# # # # #             'message': 'Resource not found'
# # # # #         }), 404
    
# # # # #     @app.errorhandler(500)
# # # # #     def internal_error(error):
# # # # #         return jsonify({
# # # # #             'success': False,
# # # # #             'message': 'Internal server error'
# # # # #         }), 500
    
# # # # #     return app

# # # # # if __name__ == '__main__':
# # # # #     app = create_app()
# # # # #     port = int(os.getenv('PORT', 5000))
# # # # #     debug = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    
# # # # #     app.run(
# # # # #         host='0.0.0.0',
# # # # #         port=port,
# # # # #         debug=debug
# # # # #     )
# # # # # app.py

# # # # from flask import Flask, jsonify
# # # # from flask_cors import CORS
# # # # from flask_jwt_extended import JWTManager
# # # # from flask_mail import Mail
# # # # from dotenv import load_dotenv
# # # # import os

# # # # # Load environment variables
# # # # load_dotenv()

# # # # # Import blueprints
# # # # from api.auth import auth_bp, mail
# # # # from api.freelancer import freelancer_bp
# # # # from api.recruiter import recruiter_bp
# # # # from api.jobs import jobs_bp
# # # # from api.notifications import notifications_bp

# # # # def create_app():
# # # #     app = Flask(__name__)
    
# # # #     # Configuration
# # # #     app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
# # # #     app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'jwt-secret-key-change-in-production')
    
# # # #     # CORS configuration
# # # #     cors_origins = os.getenv('CORS_ORIGINS', 'http://localhost:3000').split(',')
# # # #     CORS(app, origins=cors_origins, supports_credentials=True)
    
# # # #     # Email Configuration
# # # #     app.config['MAIL_SERVER'] = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
# # # #     app.config['MAIL_PORT'] = int(os.getenv('SMTP_PORT', 587))
# # # #     app.config['MAIL_USE_TLS'] = os.getenv('MAIL_USE_TLS', 'True').lower() == 'true'
# # # #     app.config['MAIL_USERNAME'] = os.getenv('SMTP_USERNAME')
# # # #     app.config['MAIL_PASSWORD'] = os.getenv('SMTP_PASSWORD')
# # # #     app.config['MAIL_DEFAULT_SENDER'] = os.getenv('FROM_EMAIL', 'noreply@freelancehub.com')
    
# # # #     # Custom app config
# # # #     app.config['BASE_URL'] = os.getenv('BASE_URL', 'http://localhost:3000')
# # # #     app.config['FROM_EMAIL'] = os.getenv('FROM_EMAIL', 'noreply@freelancehub.com')
# # # #     app.config['FROM_NAME'] = os.getenv('FROM_NAME', 'FreelanceHub')
    
# # # #     # Initialize extensions
# # # #     mail.init_app(app)
# # # #     jwt = JWTManager(app)
    
# # # #     # Register blueprints
# # # #     app.register_blueprint(auth_bp)
# # # #     app.register_blueprint(freelancer_bp)
# # # #     app.register_blueprint(recruiter_bp)
# # # #     app.register_blueprint(jobs_bp)
# # # #     app.register_blueprint(notifications_bp)
    
# # # #     # Health check endpoint
# # # #     @app.route('/api/health', methods=['GET'])
# # # #     def health_check():
# # # #         return jsonify({
# # # #             'success': True,
# # # #             'status': 'healthy',
# # # #             'message': 'Freelancer Platform API is running',
# # # #             'version': '1.0.0'
# # # #         }), 200
    
# # # #     # Error handlers
# # # #     @app.errorhandler(404)
# # # #     def not_found(error):
# # # #         return jsonify({
# # # #             'success': False,
# # # #             'message': 'Resource not found'
# # # #         }), 404
    
# # # #     @app.errorhandler(500)
# # # #     def internal_error(error):
# # # #         return jsonify({
# # # #             'success': False,
# # # #             'message': 'Internal server error'
# # # #         }), 500
    
# # # #     return app

# # # # if __name__ == '__main__':
# # # #     app = create_app()
# # # #     port = int(os.getenv('PORT', 5000))
# # # #     debug = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    
# # # #     app.run(
# # # #         host='0.0.0.0',
# # # #         port=port,
# # # #         debug=debug
# # # #     )
# # # # app.py

# # # from flask import Flask, jsonify
# # # from flask_cors import CORS
# # # from flask_jwt_extended import JWTManager
# # # from flask_mail import Mail
# # # from dotenv import load_dotenv
# # # import os

# # # # Load environment variables
# # # load_dotenv()

# # # # Import blueprints
# # # from api.auth import auth_bp, mail
# # # from api.freelancer import freelancer_bp
# # # from api.recruiter import recruiter_bp
# # # from api.jobs import jobs_bp
# # # from api.notifications import notifications_bp

# # # def create_app():
# # #     app = Flask(__name__)
    
# # #     # Configuration
# # #     app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
# # #     app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'jwt-secret-key-change-in-production')
    
# # #     # CORS configuration
# # #     cors_origins = os.getenv('CORS_ORIGINS', 'http://localhost:3000').split(',')
# # #     CORS(app, origins=cors_origins, supports_credentials=True)
    
# # #     # Email Configuration
# # #     app.config['MAIL_SERVER'] = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
# # #     app.config['MAIL_PORT'] = int(os.getenv('SMTP_PORT', 587))
# # #     app.config['MAIL_USE_TLS'] = os.getenv('MAIL_USE_TLS', 'True').lower() == 'true'
# # #     app.config['MAIL_USERNAME'] = os.getenv('SMTP_USERNAME')
# # #     app.config['MAIL_PASSWORD'] = os.getenv('SMTP_PASSWORD')
# # #     app.config['MAIL_DEFAULT_SENDER'] = os.getenv('FROM_EMAIL', 'noreply@freelancehub.com')
    
# # #     # Custom app config
# # #     app.config['BASE_URL'] = os.getenv('BASE_URL', 'http://localhost:3000')
# # #     app.config['FROM_EMAIL'] = os.getenv('FROM_EMAIL', 'noreply@freelancehub.com')
# # #     app.config['FROM_NAME'] = os.getenv('FROM_NAME', 'FreelanceHub')
    
# # #     # Initialize extensions
# # #     mail.init_app(app)
# # #     jwt = JWTManager(app)
    
# # #     # Register blueprints
# # #     app.register_blueprint(auth_bp)
# # #     app.register_blueprint(freelancer_bp)
# # #     app.register_blueprint(recruiter_bp)
# # #     app.register_blueprint(jobs_bp)
# # #     app.register_blueprint(notifications_bp)
    
# # #     # Health check endpoint
# # #     @app.route('/api/health', methods=['GET'])
# # #     def health_check():
# # #         return jsonify({
# # #             'success': True,
# # #             'status': 'healthy',
# # #             'message': 'Freelancer Platform API is running',
# # #             'version': '1.0.0'
# # #         }), 200
    
# # #     # Error handlers
# # #     @app.errorhandler(404)
# # #     def not_found(error):
# # #         return jsonify({
# # #             'success': False,
# # #             'message': 'Resource not found'
# # #         }), 404
    
# # #     @app.errorhandler(500)
# # #     def internal_error(error):
# # #         return jsonify({
# # #             'success': False,
# # #             'message': 'Internal server error'
# # #         }), 500
    
# # #     return app

# # # if __name__ == '__main__':
# # #     app = create_app()
# # #     port = int(os.getenv('PORT', 5000))
# # #     debug = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    
# # #     app.run(
# # #         host='0.0.0.0',
# # #         port=port,
# # #         debug=debug
# # #     )
# # # In your app.py, make sure you have:

# # from flask import Flask
# # from flask_cors import CORS
# # from flask_mail import Mail
# # from dotenv import load_dotenv
# # import os

# # # Load environment variables
# # load_dotenv()

# # # Import blueprints
# # from api.auth import auth_bp, mail
# # from api.freelancer import freelancer_bp
# # from api.recruiter import recruiter_bp
# # from api.jobs import jobs_bp
# # from api.notifications import notifications_bp

# # # Import email service
# # from services.email_service import EmailService, email_service

# # def create_app():
# #     app = Flask(__name__)
    
# #     # Configuration
# #     app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key')
# #     app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'jwt-secret-key')
    
# #     # CORS configuration
# #     CORS(app, origins=['http://localhost:3000'], supports_credentials=True)
    
# #     # Email Configuration
# #     app.config['MAIL_SERVER'] = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
# #     app.config['MAIL_PORT'] = int(os.getenv('SMTP_PORT', 587))
# #     app.config['MAIL_USE_TLS'] = os.getenv('MAIL_USE_TLS', 'True').lower() == 'true'
# #     app.config['MAIL_USERNAME'] = os.getenv('SMTP_USERNAME')
# #     app.config['MAIL_PASSWORD'] = os.getenv('SMTP_PASSWORD')
# #     app.config['MAIL_DEFAULT_SENDER'] = os.getenv('FROM_EMAIL', 'noreply@freelancehub.com')
    
# #     # Custom app config
# #     app.config['BASE_URL'] = os.getenv('BASE_URL', 'http://localhost:3000')
# #     app.config['FROM_EMAIL'] = os.getenv('FROM_EMAIL', 'noreply@freelancehub.com')
# #     app.config['FROM_NAME'] = os.getenv('FROM_NAME', 'FreelanceHub')
    
# #     # Initialize extensions
# #     mail.init_app(app)
    
# #     # Initialize email service globally
# #     global email_service
# #     email_service = EmailService(mail)
    
# #     # Register blueprints
# #     app.register_blueprint(auth_bp)
# #     app.register_blueprint(freelancer_bp)
# #     app.register_blueprint(recruiter_bp)
# #     app.register_blueprint(jobs_bp)
# #     app.register_blueprint(notifications_bp)
    
# #     return app

# # if __name__ == '__main__':
# #     app = create_app()
# #     port = int(os.getenv('PORT', 5000))
# #     app.run(host='0.0.0.0', port=port, debug=True)
# # app.py (add these lines where you initialize your app)

# # from flask import Flask
# # from flask_cors import CORS
# # from flask_mail import Mail
# # from dotenv import load_dotenv
# # import os

# # # Load environment variables
# # load_dotenv()

# # # Import blueprints
# # from api.auth import auth_bp, mail
# # from api.freelancer import freelancer_bp
# # from api.recruiter import recruiter_bp
# # from api.jobs import jobs_bp
# # from api.notifications import notifications_bp

# # # Import email service
# # from services.email_service import EmailService, email_service

# # def create_app():
# #     app = Flask(__name__)
    
# #     # Configuration
# #     app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key')
# #     app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'jwt-secret-key')
    
# #     # CORS configuration
# #     cors_origins = os.getenv('CORS_ORIGINS', 'http://localhost:3000').split(',')
# #     CORS(app, origins=cors_origins, supports_credentials=True)
    
# #     # Email Configuration
# #     app.config['MAIL_SERVER'] = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
# #     app.config['MAIL_PORT'] = int(os.getenv('SMTP_PORT', 587))
# #     app.config['MAIL_USE_TLS'] = os.getenv('MAIL_USE_TLS', 'True').lower() == 'true'
# #     app.config['MAIL_USERNAME'] = os.getenv('SMTP_USERNAME')
# #     app.config['MAIL_PASSWORD'] = os.getenv('SMTP_PASSWORD')
# #     app.config['MAIL_DEFAULT_SENDER'] = os.getenv('FROM_EMAIL', 'noreply@freelancehub.com')
    
# #     # Custom app config
# #     app.config['BASE_URL'] = os.getenv('BASE_URL', 'http://localhost:3000')
# #     app.config['FROM_EMAIL'] = os.getenv('FROM_EMAIL', 'noreply@freelancehub.com')
# #     app.config['FROM_NAME'] = os.getenv('FROM_NAME', 'FreelanceHub')
    
# #     # Initialize extensions
# #     mail.init_app(app)
    
# #     # Initialize email service globally
# #     global email_service
# #     email_service = EmailService(mail)
# #     print("✅ Email service initialized")
    
# #     # Register blueprints
# #     app.register_blueprint(auth_bp)
# #     app.register_blueprint(freelancer_bp)
# #     app.register_blueprint(recruiter_bp)
# #     app.register_blueprint(jobs_bp)
# #     app.register_blueprint(notifications_bp)


# #     # In your app.py, after creating the app


# # from services.email_service import EmailService, email_service

# # # In app.py, when creating the app:

# # def create_app():
# #     app = Flask(__name__)
    
# #     # Configuration
# #     app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key')
# #     app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'jwt-secret-key')
    
# #     # CORS configuration - IMPORTANT
# #     CORS(app, origins=['http://localhost:3000'], supports_credentials=True)
    
# #     # Email Configuration
# #     app.config['MAIL_SERVER'] = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
# #     app.config['MAIL_PORT'] = int(os.getenv('SMTP_PORT', 587))
# #     app.config['MAIL_USE_TLS'] = os.getenv('MAIL_USE_TLS', 'True').lower() == 'true'
# #     app.config['MAIL_USERNAME'] = os.getenv('SMTP_USERNAME')
# #     app.config['MAIL_PASSWORD'] = os.getenv('SMTP_PASSWORD')
# #     app.config['MAIL_DEFAULT_SENDER'] = os.getenv('FROM_EMAIL', 'noreply@freelancehub.com')
    
# #     # Custom app config
# #     app.config['BASE_URL'] = os.getenv('BASE_URL', 'http://localhost:3000')
# #     app.config['FROM_EMAIL'] = os.getenv('FROM_EMAIL', 'noreply@freelancehub.com')
# #     app.config['FROM_NAME'] = os.getenv('FROM_NAME', 'FreelanceHub')
    
# #     # Initialize extensions
# #     mail.init_app(app)
    
# #     # Initialize email service globally (with app context)
# #     with app.app_context():
# #         global email_service
# #         from services.email_service import EmailService
# #         email_service = EmailService(mail)
# #         print("✅ Email service initialized")
# #         print(f"📧 Mail configured for: {app.config['MAIL_USERNAME']}")
    
# #     # Register blueprints
# #     app.register_blueprint(auth_bp)
# #     app.register_blueprint(freelancer_bp)
# #     app.register_blueprint(recruiter_bp)
# #     app.register_blueprint(jobs_bp)
# #     app.register_blueprint(notifications_bp)
    

# #     global email_service
# #     email_service = EmailService(mail)
# #     print(f"🔧 EmailService initialized with mail: {email_service.mail is not None}")
# #     print(f"✅ Email service initialized")
    
# #     # Store in app config for easy access
# #     app.config['EMAIL_SERVICE'] = email_service


# #     return app

# # if __name__ == '__main__':
# #     app = create_app()
# #     port = int(os.getenv('PORT', 5000))
# #     app.run(host='0.0.0.0', port=port, debug=True)

# from flask import Flask, jsonify
# from flask_cors import CORS
# from flask_mail import Mail
# from dotenv import load_dotenv
# import os

# # Load environment variables
# load_dotenv()

# # Import blueprints
# from api.auth import auth_bp
# from api.freelancer import freelancer_bp
# from api.recruiter import recruiter_bp
# from api.jobs import jobs_bp
# from api.notifications import notifications_bp

# # Initialize mail
# mail = Mail()

# def create_app():
#     app = Flask(__name__)
    
#     # Configuration
#     app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key')
#     app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'jwt-secret-key')
    
#     # CORS configuration
#     CORS(app, origins=['http://localhost:3000'], supports_credentials=True)
    
#     # Email Configuration
#     app.config['MAIL_SERVER'] = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
#     app.config['MAIL_PORT'] = int(os.getenv('SMTP_PORT', 587))
#     app.config['MAIL_USE_TLS'] = os.getenv('MAIL_USE_TLS', 'True').lower() == 'true'
#     app.config['MAIL_USERNAME'] = os.getenv('SMTP_USERNAME')
#     app.config['MAIL_PASSWORD'] = os.getenv('SMTP_PASSWORD')
#     app.config['MAIL_DEFAULT_SENDER'] = os.getenv('FROM_EMAIL', 'noreply@freelancehub.com')
    
#     # Custom app config
#     app.config['BASE_URL'] = os.getenv('BASE_URL', 'http://localhost:3000')
#     app.config['FROM_EMAIL'] = os.getenv('FROM_EMAIL', 'noreply@freelancehub.com')
#     app.config['FROM_NAME'] = os.getenv('FROM_NAME', 'FreelanceHub')
    
#     # Initialize extensions
#     mail.init_app(app)
    
#     # Initialize email service globally
#     with app.app_context():
#         from services.email_service import EmailService
#         import services.email_instance
        
#         # Create the email service instance
#         email_service_instance = EmailService(mail)
        
#         # Set it in the global holder
#         services.email_instance.email_service = email_service_instance
        
#         print(f"🔧 EmailService initialized with mail: {email_service_instance.mail is not None}")
#         print("✅ Email service initialized")
#         print(f"📧 Mail configured for: {app.config['MAIL_USERNAME']}")
        
#         # Store in app config for easy access
#         app.config['EMAIL_SERVICE'] = email_service_instance
    
#     # Register blueprints
#     app.register_blueprint(auth_bp)
#     app.register_blueprint(freelancer_bp)
#     app.register_blueprint(recruiter_bp)
#     app.register_blueprint(jobs_bp)
#     app.register_blueprint(notifications_bp)
    
#     # Route to list all endpoints
#     @app.route('/api/routes', methods=['GET'])
#     def list_routes():
#         """List all registered routes"""
#         routes = []
#         for rule in app.url_map.iter_rules():
#             # Filter out static routes
#             if not str(rule).startswith('/static'):
#                 routes.append({
#                     'endpoint': rule.endpoint,
#                     'methods': list(rule.methods),
#                     'path': str(rule)
#                 })
#         return jsonify({'routes': routes})
    
#     return app

# if __name__ == '__main__':
#     app = create_app()
#     port = int(os.getenv('PORT', 5000))
#     app.run(host='0.0.0.0', port=port, debug=True)

from flask import Flask, jsonify
from flask_cors import CORS
from flask_mail import Mail
from dotenv import load_dotenv
import os

load_dotenv()

# Import blueprints from routes (not api)
from routes.auth_routes import auth_bp
from routes.freelancer_routes import freelancer_bp
from routes.recruiter_routes import recruiter_bp
from routes.job_routes import jobs_bp
from routes.notification_routes import notifications_bp

mail = Mail()

def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret')
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'jwt-secret')
    app.config['BASE_URL'] = os.getenv('BASE_URL', 'http://localhost:3000')

    # Email config
    app.config['MAIL_SERVER'] = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
    app.config['MAIL_PORT'] = int(os.getenv('SMTP_PORT', 587))
    app.config['MAIL_USE_TLS'] = os.getenv('MAIL_USE_TLS', 'True').lower() == 'true'
    app.config['MAIL_USERNAME'] = os.getenv('SMTP_USERNAME')
    app.config['MAIL_PASSWORD'] = os.getenv('SMTP_PASSWORD')
    app.config['MAIL_DEFAULT_SENDER'] = os.getenv('FROM_EMAIL', 'noreply@freelancehub.com')
    app.config['FROM_EMAIL'] = os.getenv('FROM_EMAIL')

    CORS(app, origins=['http://localhost:3000'], supports_credentials=True)

    mail.init_app(app)

    # Initialize global email service
    with app.app_context():
        from services.email_service import EmailService
        import services.email_instance
        services.email_instance.email_service = EmailService(mail)
        app.config['EMAIL_SERVICE'] = services.email_instance.email_service
        print("✅ Email service initialized")
        print(f"📧 Mail configured for: {app.config['MAIL_USERNAME']}")

    # Register blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(freelancer_bp)
    app.register_blueprint(recruiter_bp)
    app.register_blueprint(jobs_bp)
    app.register_blueprint(notifications_bp)

    @app.route('/api/health')
    def health():
        return jsonify({
            'success': True,
            'status': 'healthy',
            'blueprints': list(app.blueprints.keys())
        })

    @app.route('/api/routes', methods=['GET'])
    def list_routes():
        routes = []
        for rule in app.url_map.iter_rules():
            if not str(rule).startswith('/static'):
                routes.append({
                    'endpoint': rule.endpoint,
                    'methods': list(rule.methods),
                    'path': str(rule)
                })
        return jsonify({'routes': routes})

    return app

if __name__ == '__main__':
    app = create_app()
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)