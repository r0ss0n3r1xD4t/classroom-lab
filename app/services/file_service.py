import os
from werkzeug.utils import secure_filename
from flask import current_app, send_file
from datetime import datetime


class FileService:
    """Service layer cho xử lý file upload/download"""
    
    @staticmethod
    def allowed_file(filename):
        """Kiểm tra file có được phép upload không"""
        if '.' not in filename:
            return False
        ext = filename.rsplit('.', 1)[1].lower()
        return ext in current_app.config['ALLOWED_EXTENSIONS']
    
    @staticmethod
    def safe_join_path(base_path, user_path):
        """
        An toàn join path và kiểm tra path traversal
        Ngăn chặn các tấn công dùng ../ để truy cập file ngoài thư mục
        """
        # Normalize và resolve path
        full_path = os.path.normpath(os.path.join(base_path, user_path))
        
        # Kiểm tra path có nằm trong base_path không
        if not full_path.startswith(os.path.normpath(base_path)):
            raise ValueError("Path traversal attack detected!")
        
        return full_path
    
    @staticmethod
    def save_assignment_file(file, teacher_id):
        """
        Lưu file bài tập của giáo viên
        Returns: (file_path, filename) hoặc (None, error_message)
        """
        if not file or file.filename == '':
            return None, 'Không có file được chọn'
        
        if not FileService.allowed_file(file.filename):
            return None, f'File không hợp lệ. Chỉ chấp nhận: {", ".join(current_app.config["ALLOWED_EXTENSIONS"])}'
        
        # Tạo tên file an toàn
        filename = secure_filename(file.filename)
        
        # Tạo tên file unique với timestamp và teacher_id
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        name, ext = os.path.splitext(filename)
        unique_filename = f"teacher_{teacher_id}_{timestamp}_{name}{ext}"
        
        # Tạo thư mục nếu chưa có
        upload_folder = os.path.join(current_app.config['UPLOAD_FOLDER'], 'assignments')
        os.makedirs(upload_folder, exist_ok=True)
        
        # Lưu file
        file_path = os.path.join(upload_folder, unique_filename)
        try:
            file.save(file_path)
            # Trả về đường dẫn tương đối (dùng để lưu vào DB)
            relative_path = os.path.join('assignments', unique_filename)
            return relative_path, filename
        except Exception as e:
            return None, f'Lỗi khi lưu file: {str(e)}'
    
    @staticmethod
    def save_submission_file(file, student_id, assignment_id):
        """
        Lưu file bài nộp của sinh viên
        Returns: (file_path, filename) hoặc (None, error_message)
        """
        if not file or file.filename == '':
            return None, 'Không có file được chọn'
        
        if not FileService.allowed_file(file.filename):
            return None, f'File không hợp lệ. Chỉ chấp nhận: {", ".join(current_app.config["ALLOWED_EXTENSIONS"])}'
        
        # Tạo tên file an toàn
        filename = secure_filename(file.filename)
        
        # Tạo tên file unique với timestamp
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        name, ext = os.path.splitext(filename)
        unique_filename = f"student_{student_id}_assignment_{assignment_id}_{timestamp}_{name}{ext}"
        
        # Tạo thư mục nếu chưa có
        upload_folder = os.path.join(current_app.config['UPLOAD_FOLDER'], 'submissions')
        os.makedirs(upload_folder, exist_ok=True)
        
        # Lưu file
        file_path = os.path.join(upload_folder, unique_filename)
        try:
            file.save(file_path)
            # Trả về đường dẫn tương đối (dùng để lưu vào DB)
            relative_path = os.path.join('submissions', unique_filename)
            return relative_path, filename
        except Exception as e:
            return None, f'Lỗi khi lưu file: {str(e)}'
    
    @staticmethod
    def get_file_path(relative_path):
        """
        Lấy đường dẫn tuyệt đối của file từ đường dẫn tương đối
        Có bảo vệ chống path traversal
        """
        base_path = current_app.config['UPLOAD_FOLDER']
        try:
            return FileService.safe_join_path(base_path, relative_path)
        except ValueError as e:
            # Log security incident
            print(f"[SECURITY] Path traversal attempt: {relative_path}")
            raise
    
    @staticmethod
    def delete_file(relative_path):
        """Xóa file"""
        try:
            file_path = FileService.get_file_path(relative_path)
            if os.path.exists(file_path):
                os.remove(file_path)
                return True
            return False
        except Exception as e:
            print(f"Error deleting file: {e}")
            return False
    
    @staticmethod
    def file_exists(relative_path):
        """Kiểm tra file có tồn tại không"""
        file_path = FileService.get_file_path(relative_path)
        return os.path.exists(file_path)
