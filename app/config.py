"""
File cấu hình cho ứng dụng Flask
Chứa các thiết lập về database, secret key, upload folder...
"""
import os

# Lấy đường dẫn tuyệt đối của thư mục hiện tại
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    """Cấu hình chung cho ứng dụng"""
    
    # Secret key để mã hóa session (nên đổi thành chuỗi ngẫu nhiên)
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    
    # Cấu hình database SQLite
    # Database sẽ được lưu trong thư mục instance/classroom.db
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, '..', 'instance', 'classroom.db')
    
    # Tắt track modifications để tiết kiệm bộ nhớ
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Cấu hình upload file
    UPLOAD_FOLDER = os.path.join(basedir, 'static', 'uploads')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # Giới hạn 16MB
    
    # Các loại file được phép upload
    ALLOWED_EXTENSIONS = {'txt', 'pdf', 'doc', 'docx', 'zip'}

class DevelopmentConfig(Config):
    """Cấu hình cho môi trường development (phát triển)"""
    DEBUG = True  # Bật chế độ debug
    TESTING = False

class ProductionConfig(Config):
    """Cấu hình cho môi trường production (triển khai thực tế)"""
    DEBUG = False
    TESTING = False

# Dictionary để chọn config theo môi trường
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}