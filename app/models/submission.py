from app import db
from datetime import datetime


class Submission(db.Model):
    """Model cho bài nộp của sinh viên"""
    __tablename__ = 'submissions'
    
    id = db.Column(db.Integer, primary_key=True)
    file_path = db.Column(db.String(500), nullable=False)  # Đường dẫn file bài nộp
    filename = db.Column(db.String(200), nullable=False)  # Tên file gốc
    submitted_at = db.Column(db.DateTime, default=datetime.utcnow)
    note = db.Column(db.Text)  # Ghi chú của sinh viên khi nộp bài
    
    # Foreign keys
    student_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    assignment_id = db.Column(db.Integer, db.ForeignKey('assignments.id'), nullable=False)
    
    # Relationships
    student = db.relationship('User', backref=db.backref('submissions', lazy=True))
    
    # Constraint: Mỗi sinh viên chỉ nộp 1 lần cho mỗi assignment
    __table_args__ = (
        db.UniqueConstraint('student_id', 'assignment_id', name='unique_student_assignment'),
    )
    
    def __repr__(self):
        return f'<Submission {self.student.username} - Assignment {self.assignment_id}>'
    
    def is_late(self):
        """Kiểm tra nộp muộn hay không"""
        if self.assignment.deadline:
            return self.submitted_at > self.assignment.deadline
        return False
