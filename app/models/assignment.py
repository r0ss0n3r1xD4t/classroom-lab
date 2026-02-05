from app import db
from datetime import datetime


class Assignment(db.Model):
    """Model cho bài tập được giao bởi giáo viên"""
    __tablename__ = 'assignments'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    file_path = db.Column(db.String(500))  # Đường dẫn file bài tập
    filename = db.Column(db.String(200))  # Tên file gốc
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    deadline = db.Column(db.DateTime)  # Hạn nộp bài
    
    # Foreign key tới User (giáo viên)
    teacher_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # Relationship
    teacher = db.relationship('User', backref=db.backref('assignments', lazy=True))
    submissions = db.relationship('Submission', backref='assignment', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Assignment {self.title}>'
    
    def has_file(self):
        """Kiểm tra bài tập có file đính kèm không"""
        return self.file_path is not None and self.file_path != ''
    
    def is_overdue(self):
        """Kiểm tra đã quá hạn nộp chưa"""
        if self.deadline:
            return datetime.utcnow() > self.deadline
        return False
