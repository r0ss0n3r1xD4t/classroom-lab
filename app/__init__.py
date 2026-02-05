from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
from dotenv import load_dotenv

# Load biến môi trường từ file .env
load_dotenv()

# Khởi tạo extensions
db = SQLAlchemy()
login_manager = LoginManager()
csrf = CSRFProtect()

def create_app():
    app = Flask(__name__, template_folder='views')
    
    # Load config
    app.config.from_object('app.config.Config')
    
    # Khởi tạo database
    db.init_app(app)
    
    # Khởi tạo CSRF protection
    csrf.init_app(app)
    
    # Khởi tạo login manager
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Vui lòng đăng nhập để truy cập trang này.'
    login_manager.login_message_category = 'warning'
    
    # User loader cho Flask-Login
    @login_manager.user_loader
    def load_user(user_id):
        from app.models.user import User
        return User.query.get(int(user_id))
    
    # Import models trước khi tạo tables (QUAN TRỌNG!)
    from app.models.user import User
    from app.models.assignment import Assignment
    from app.models.submission import Submission
    from app.models.challenge import Challenge
    
    # Tạo database tables
    with app.app_context():
        db.create_all()
        print("✓ Database tables created successfully!")
    
    # Import và đăng ký blueprints
    from app.controllers.auth_controller import auth_bp
    from app.controllers.user_controller import user_bp
    from app.controllers.assignment_controller import assignment_bp
    from app.controllers.challenge_controller import challenge_bp
    app.register_blueprint(auth_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(assignment_bp)
    app.register_blueprint(challenge_bp)
    
    return app
