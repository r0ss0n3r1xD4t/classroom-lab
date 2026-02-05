from app import db
from app.models.assignment import Assignment
from app.models.submission import Submission
from app.models.user import User
from datetime import datetime


class AssignmentService:
    """Service layer cho quản lý assignments"""
    
    @staticmethod
    def get_all_assignments():
        """Lấy tất cả bài tập, sắp xếp theo ngày tạo mới nhất"""
        return Assignment.query.order_by(Assignment.created_at.desc()).all()
    
    @staticmethod
    def get_assignment_by_id(assignment_id):
        """Lấy bài tập theo ID"""
        return Assignment.query.get(assignment_id)
    
    @staticmethod
    def create_assignment(title, description, teacher_id, file_path=None, filename=None, deadline=None):
        """
        Tạo bài tập mới
        Returns: (assignment, error_message)
        """
        if not title:
            return None, "Tiêu đề không được để trống"
        
        # Tạo assignment mới
        assignment = Assignment(
            title=title,
            description=description,
            teacher_id=teacher_id,
            file_path=file_path,
            filename=filename,
            deadline=deadline
        )
        
        try:
            db.session.add(assignment)
            db.session.commit()
            return assignment, None
        except Exception as e:
            db.session.rollback()
            return None, f"Lỗi khi tạo bài tập: {str(e)}"
    
    @staticmethod
    def update_assignment(assignment_id, title, description, deadline=None):
        """Cập nhật thông tin bài tập"""
        assignment = Assignment.query.get(assignment_id)
        if not assignment:
            return None, "Không tìm thấy bài tập"
        
        assignment.title = title
        assignment.description = description
        assignment.deadline = deadline
        
        try:
            db.session.commit()
            return assignment, None
        except Exception as e:
            db.session.rollback()
            return None, f"Lỗi khi cập nhật bài tập: {str(e)}"
    
    @staticmethod
    def delete_assignment(assignment_id):
        """Xóa bài tập"""
        assignment = Assignment.query.get(assignment_id)
        if not assignment:
            return False, "Không tìm thấy bài tập"
        
        try:
            db.session.delete(assignment)
            db.session.commit()
            return True, None
        except Exception as e:
            db.session.rollback()
            return False, f"Lỗi khi xóa bài tập: {str(e)}"
    
    # === SUBMISSION METHODS ===
    
    @staticmethod
    def get_submissions_by_assignment(assignment_id):
        """Lấy tất cả bài nộp của một assignment"""
        return Submission.query.filter_by(assignment_id=assignment_id).order_by(Submission.submitted_at.desc()).all()
    
    @staticmethod
    def get_submission_by_student_and_assignment(student_id, assignment_id):
        """Kiểm tra sinh viên đã nộp bài chưa"""
        return Submission.query.filter_by(
            student_id=student_id,
            assignment_id=assignment_id
        ).first()
    
    @staticmethod
    def create_submission(student_id, assignment_id, file_path, filename, note=None):
        """
        Tạo bài nộp mới
        Returns: (submission, error_message)
        """
        # Kiểm tra đã nộp bài chưa
        existing = AssignmentService.get_submission_by_student_and_assignment(student_id, assignment_id)
        if existing:
            return None, "Bạn đã nộp bài cho assignment này rồi"
        
        # Tạo submission mới
        submission = Submission(
            student_id=student_id,
            assignment_id=assignment_id,
            file_path=file_path,
            filename=filename,
            note=note
        )
        
        try:
            db.session.add(submission)
            db.session.commit()
            return submission, None
        except Exception as e:
            db.session.rollback()
            return None, f"Lỗi khi nộp bài: {str(e)}"
    
    @staticmethod
    def get_all_submissions():
        """Lấy tất cả bài nộp (cho giáo viên)"""
        return Submission.query.order_by(Submission.submitted_at.desc()).all()
    
    @staticmethod
    def get_submissions_by_student(student_id):
        """Lấy tất cả bài nộp của một sinh viên"""
        return Submission.query.filter_by(student_id=student_id).order_by(Submission.submitted_at.desc()).all()
    
    @staticmethod
    def get_submission_stats(assignment_id):
        """Lấy thống kê bài nộp cho một assignment"""
        total_students = User.query.filter_by(role='student').count()
        submitted_count = Submission.query.filter_by(assignment_id=assignment_id).count()
        return {
            'total_students': total_students,
            'submitted_count': submitted_count,
            'not_submitted_count': total_students - submitted_count
        }
