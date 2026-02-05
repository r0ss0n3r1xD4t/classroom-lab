from app import db
from app.models.user import User


class UserService:
    
    @staticmethod
    def get_all_users():
        return User.query.order_by(User.created_at.desc()).all()
    
    @staticmethod
    def get_user_by_id(user_id):
        return User.query.get(user_id)
    
    @staticmethod
    def get_user_by_username(username):
        return User.query.filter_by(username=username).first()
    
    @staticmethod
    def get_user_by_email(email):
        return User.query.filter_by(email=email).first()
    
    @staticmethod
    def create_user(username, password, fullname, email, phone, role):
        if UserService.get_user_by_username(username):
            return None, "Username đã tồn tại"
        
        if UserService.get_user_by_email(email):
            return None, "Email đã tồn tại"
        
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
        user = UserService.get_user_by_id(user_id)
        if not user:
            return None, "User không tồn tại"
        
        if email and email != user.email:
            existing_user = UserService.get_user_by_email(email)
            if existing_user:
                return None, "Email đã được sử dụng"
        
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
        return User.query.filter_by(role='student').order_by(User.created_at.desc()).all()
    
    @staticmethod
    def get_all_teachers():
        return User.query.filter_by(role='teacher').order_by(User.created_at.desc()).all()
