from app import db
from datetime import datetime


class Challenge(db.Model):
    """Model cho trò chơi giải đố (không lưu đáp án)"""
    __tablename__ = 'challenges'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    file_path = db.Column(db.String(500), nullable=False)  # Đường dẫn file txt (bài thơ, văn)
    filename = db.Column(db.String(200), nullable=False)  # Tên file gốc (KHÔNG lưu extension)
    hint = db.Column(db.Text)  # Gợi ý cho sinh viên
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)  # Challenge có đang hoạt động không
    
    # Foreign key tới User (giáo viên)
    teacher_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # Relationship
    teacher = db.relationship('User', backref=db.backref('challenges', lazy=True))
    
    def __repr__(self):
        return f'<Challenge {self.title}>'
    
    def get_answer(self):
        """
        Lấy đáp án (tên file không có extension)
        ĐÂY LÀ ĐIỂM QUAN TRỌNG: Đáp án = tên file
        """
        return self.filename.lower().strip()
    
    def check_answer(self, user_answer):
        """
        Kiểm tra đáp án có đúng không
        So sánh không phân biệt hoa thường và bỏ khoảng trắng thừa
        """
        if not user_answer:
            return False
        
        correct_answer = self.get_answer()
        user_answer = user_answer.lower().strip()
        
        return user_answer == correct_answer
