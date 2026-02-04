from app import db
from app.models.user import User


class UserService:
    """Service layer cho quản lý user"""
    
    @staticmethod
    def get_all_users():
        """Lấy danh sách tất cả users"""
        return User.query.order_by(User.created_at.desc()).all()
    
    @staticmethod
    def get_user_by_id(user_id):
        """Lấy thông tin user theo ID"""
        return User.query.get(user_id)
    
    @staticmethod
    def get_user_by_username(username):
        """Lấy user theo username"""
        return User.query.filter_by(username=username).first()
    
    @staticmethod
    def get_user_by_email(email):
        """Lấy user theo email"""
        return User.query.filter_by(email=email).first()
    
    @staticmethod
    def create_user(username, password, fullname, email, phone, role):
        """Tạo user mới"""
        # Kiểm tra username đã tồn tại
        if UserService.get_user_by_username(username):
            return None, "Username đã tồn tại"
        
        # Kiểm tra email đã tồn tại
        if UserService.get_user_by_email(email):
            return None, "Email đã tồn tại"
        
        # Tạo user mới
        user = User(
            username=username,
            fullname=fullname,
            email=email,
            phone=phone,
            role=role
        )
        user.set_password(password)
        
        try:
            db.session.add(user)
            db.session.commit()
            return user, None
        except Exception as e:
            db.session.rollback()
            return None, str(e)
    
    @staticmethod
    def update_user(user_id, fullname=None, email=None, phone=None, password=None):
        """Cập nhật thông tin user (không cho phép đổi username và role)"""
        user = UserService.get_user_by_id(user_id)
        if not user:
            return None, "User không tồn tại"
        
        # Kiểm tra email nếu có thay đổi
        if email and email != user.email:
            existing_user = UserService.get_user_by_email(email)
            if existing_user:
                return None, "Email đã được sử dụng"
        
        # Cập nhật thông tin
        if fullname:
            user.fullname = fullname
        if email:
            user.email = email
        if phone:
            user.phone = phone
        if password:
            user.set_password(password)
        
        try:
            db.session.commit()
            return user, None
        except Exception as e:
            db.session.rollback()
            return None, str(e)
    
    @staticmethod
    def delete_user(user_id):
        """Xóa user"""
        user = UserService.get_user_by_id(user_id)
        if not user:
            return False, "User không tồn tại"
        
        try:
            db.session.delete(user)
            db.session.commit()
            return True, None
        except Exception as e:
            db.session.rollback()
            return False, str(e)
    
    @staticmethod
    def get_all_students():
        """Lấy danh sách tất cả sinh viên"""
        return User.query.filter_by(role='student').order_by(User.created_at.desc()).all()
    
    @staticmethod
    def get_all_teachers():
        """Lấy danh sách tất cả giáo viên"""
        return User.query.filter_by(role='teacher').order_by(User.created_at.desc()).all()
