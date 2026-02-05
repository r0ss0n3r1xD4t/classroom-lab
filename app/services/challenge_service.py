from app import db
from app.models.challenge import Challenge
from flask import current_app
import os
from werkzeug.utils import secure_filename
from datetime import datetime


class ChallengeService:
    
    @staticmethod
    def get_all_challenges():
        return Challenge.query.filter_by(is_active=True).order_by(Challenge.created_at.desc()).all()
    
    @staticmethod
    def get_all_challenges_for_teacher():
        return Challenge.query.order_by(Challenge.created_at.desc()).all()
    
    @staticmethod
    def get_challenge_by_id(challenge_id):
        return Challenge.query.get(challenge_id)
    
    @staticmethod
    def save_challenge_file(file, teacher_id):
        if not file or file.filename == '':
            return None, 'Không có file được chọn'
        
        if not file.filename.lower().endswith('.txt'):
            return None, 'Chỉ chấp nhận file .txt'
        
        original_filename = secure_filename(file.filename)
        
        filename_without_ext = os.path.splitext(original_filename)[0]
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        unique_filename = f"teacher_{teacher_id}_{timestamp}_{original_filename}"
        
        upload_folder = os.path.join(current_app.config['UPLOAD_FOLDER'], 'challenges')
        os.makedirs(upload_folder, exist_ok=True)
        
        file_path = os.path.join(upload_folder, unique_filename)
        try:
            file.save(file_path)
            relative_path = os.path.join('challenges', unique_filename)
            return relative_path, filename_without_ext
        except Exception as e:
            return None, f'Lỗi khi lưu file: {str(e)}'
    
    @staticmethod
    def create_challenge(title, description, teacher_id, file_path, filename, hint=None):
        if not title:
            return None, "Tiêu đề không được để trống"
        
        if not file_path or not filename:
            return None, "File challenge là bắt buộc"
        
        challenge = Challenge(
            title=title,
            description=description,
            teacher_id=teacher_id,
            file_path=file_path,
            filename=filename,
            hint=hint
        )
        
        try:
            db.session.add(challenge)
            db.session.commit()
            return challenge, None
        except Exception as e:
            db.session.rollback()
            return None, f"Lỗi khi tạo challenge: {str(e)}"
    
    @staticmethod
    def update_challenge(challenge_id, title, description, hint=None):
        challenge = Challenge.query.get(challenge_id)
        if not challenge:
            return None, "Không tìm thấy challenge"
        
        challenge.title = title
        challenge.description = description
        challenge.hint = hint
        
        try:
            db.session.commit()
            return challenge, None
        except Exception as e:
            db.session.rollback()
            return None, f"Lỗi khi cập nhật challenge: {str(e)}"
    
    @staticmethod
    def deactivate_challenge(challenge_id):
        challenge = Challenge.query.get(challenge_id)
        if not challenge:
            return False, "Không tìm thấy challenge"
        
        challenge.is_active = False
        
        try:
            db.session.commit()
            return True, None
        except Exception as e:
            db.session.rollback()
            return False, f"Lỗi khi vô hiệu hóa challenge: {str(e)}"
    
    @staticmethod
    def delete_challenge(challenge_id):
        challenge = Challenge.query.get(challenge_id)
        if not challenge:
            return False, "Không tìm thấy challenge"
        
        try:
            db.session.delete(challenge)
            db.session.commit()
            return True, None
        except Exception as e:
            db.session.rollback()
            return False, f"Lỗi khi xóa challenge: {str(e)}"
    
    @staticmethod
    def get_file_path(relative_path):
        base_path = current_app.config['UPLOAD_FOLDER']
        full_path = os.path.normpath(os.path.join(base_path, relative_path))
        
        if not full_path.startswith(os.path.normpath(base_path)):
            print(f"[SECURITY] Path traversal attempt in challenge: {relative_path}")
            raise ValueError("Path traversal attack detected!")
        
        return full_path
    
    @staticmethod
    def read_challenge_content(challenge):
        try:
            file_path = ChallengeService.get_file_path(challenge.file_path)
            
            if not os.path.exists(file_path):
                return None, "File không tồn tại"
            
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            return content, None
        except UnicodeDecodeError:
            try:
                with open(file_path, 'r', encoding='latin-1') as f:
                    content = f.read()
                return content, None
            except Exception as e:
                return None, f"Lỗi khi đọc file: {str(e)}"
        except Exception as e:
            return None, f"Lỗi khi đọc file: {str(e)}"
    
    @staticmethod
    def delete_challenge_file(relative_path):
        try:
            file_path = ChallengeService.get_file_path(relative_path)
            if os.path.exists(file_path):
                os.remove(file_path)
                return True
            return False
        except Exception as e:
            print(f"Error deleting file: {e}")
            return False
