from flask import Blueprint, render_template, request, redirect, url_for, flash, send_file
from flask_login import login_required, current_user
from app.services.assignment_service import AssignmentService
from app.services.file_service import FileService
from app.utils.decorators import teacher_required
from datetime import datetime

assignment_bp = Blueprint('assignment', __name__, url_prefix='/assignments')


@assignment_bp.route('/')
@login_required
def list_assignments():
    """Hiển thị danh sách tất cả bài tập"""
    assignments = AssignmentService.get_all_assignments()
    
    # Kiểm tra sinh viên đã nộp bài nào chưa
    submissions_status = {}
    if current_user.is_student():
        for assignment in assignments:
            submission = AssignmentService.get_submission_by_student_and_assignment(
                current_user.id, 
                assignment.id
            )
            submissions_status[assignment.id] = submission is not None
    
    return render_template('assignment/list.html', 
                         assignments=assignments,
                         submissions_status=submissions_status)


@assignment_bp.route('/upload', methods=['GET', 'POST'])
@login_required
@teacher_required
def upload():
    """Upload bài tập mới (chỉ giáo viên)"""
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        deadline_str = request.form.get('deadline')
        file = request.files.get('file')
        
        # Validate
        if not title:
            flash('Vui lòng nhập tiêu đề bài tập', 'danger')
            return render_template('assignment/upload.html')
        
        # Xử lý deadline
        deadline = None
        if deadline_str:
            try:
                deadline = datetime.strptime(deadline_str, '%Y-%m-%dT%H:%M')
            except ValueError:
                flash('Định dạng ngày giờ không hợp lệ', 'danger')
                return render_template('assignment/upload.html')
        
        # Xử lý file upload (optional)
        file_path = None
        filename = None
        if file and file.filename:
            file_path, result = FileService.save_assignment_file(file, current_user.id)
            if file_path is None:
                flash(f'Lỗi upload file: {result}', 'danger')
                return render_template('assignment/upload.html')
            filename = result
        
        # Tạo assignment
        assignment, error = AssignmentService.create_assignment(
            title=title,
            description=description,
            teacher_id=current_user.id,
            file_path=file_path,
            filename=filename,
            deadline=deadline
        )
        
        if error:
            flash(f'Lỗi: {error}', 'danger')
            return render_template('assignment/upload.html')
        
        flash('Upload bài tập thành công!', 'success')
        return redirect(url_for('assignment.list_assignments'))
    
    return render_template('assignment/upload.html')


@assignment_bp.route('/<int:assignment_id>/submit', methods=['GET', 'POST'])
@login_required
def submit(assignment_id):
    """Nộp bài (sinh viên)"""
    # Chỉ sinh viên mới được nộp bài
    if not current_user.is_student():
        flash('Chỉ sinh viên mới có thể nộp bài', 'danger')
        return redirect(url_for('assignment.list_assignments'))
    
    assignment = AssignmentService.get_assignment_by_id(assignment_id)
    if not assignment:
        flash('Không tìm thấy bài tập', 'danger')
        return redirect(url_for('assignment.list_assignments'))
    
    # Kiểm tra đã nộp bài chưa
    existing_submission = AssignmentService.get_submission_by_student_and_assignment(
        current_user.id, 
        assignment_id
    )
    if existing_submission:
        flash('Bạn đã nộp bài cho assignment này rồi', 'warning')
        return redirect(url_for('assignment.list_assignments'))
    
    if request.method == 'POST':
        file = request.files.get('file')
        note = request.form.get('note')
        
        # Validate file
        if not file or not file.filename:
            flash('Vui lòng chọn file để nộp', 'danger')
            return render_template('assignment/submit.html', assignment=assignment)
        
        # Lưu file
        file_path, result = FileService.save_submission_file(
            file, 
            current_user.id, 
            assignment_id
        )
        if file_path is None:
            flash(f'Lỗi upload file: {result}', 'danger')
            return render_template('assignment/submit.html', assignment=assignment)
        
        filename = result
        
        # Tạo submission
        submission, error = AssignmentService.create_submission(
            student_id=current_user.id,
            assignment_id=assignment_id,
            file_path=file_path,
            filename=filename,
            note=note
        )
        
        if error:
            flash(f'Lỗi: {error}', 'danger')
            # Xóa file đã upload nếu tạo submission thất bại
            FileService.delete_file(file_path)
            return render_template('assignment/submit.html', assignment=assignment)
        
        flash('Nộp bài thành công!', 'success')
        return redirect(url_for('assignment.list_assignments'))
    
    return render_template('assignment/submit.html', assignment=assignment)


@assignment_bp.route('/<int:assignment_id>/submissions')
@login_required
@teacher_required
def view_submissions(assignment_id):
    """Xem danh sách bài nộp của một assignment (giáo viên)"""
    assignment = AssignmentService.get_assignment_by_id(assignment_id)
    if not assignment:
        flash('Không tìm thấy bài tập', 'danger')
        return redirect(url_for('assignment.list_assignments'))
    
    # IDOR Fix: Kiểm tra giáo viên có phải là người tạo assignment này không
    if assignment.teacher_id != current_user.id:
        flash('Bạn không có quyền xem bài nộp của assignment này', 'danger')
        return redirect(url_for('assignment.list_assignments'))
    
    submissions = AssignmentService.get_submissions_by_assignment(assignment_id)
    stats = AssignmentService.get_submission_stats(assignment_id)
    
    return render_template('assignment/submissions.html', 
                         assignment=assignment,
                         submissions=submissions,
                         stats=stats)


@assignment_bp.route('/download/assignment/<int:assignment_id>')
@login_required
def download_assignment(assignment_id):
    """Download file bài tập"""
    assignment = AssignmentService.get_assignment_by_id(assignment_id)
    if not assignment:
        flash('Không tìm thấy bài tập', 'danger')
        return redirect(url_for('assignment.list_assignments'))
    
    if not assignment.has_file():
        flash('Bài tập này không có file đính kèm', 'warning')
        return redirect(url_for('assignment.list_assignments'))
    
    # Kiểm tra file có tồn tại không
    if not FileService.file_exists(assignment.file_path):
        flash('File không tồn tại', 'danger')
        return redirect(url_for('assignment.list_assignments'))
    
    file_path = FileService.get_file_path(assignment.file_path)
    return send_file(file_path, as_attachment=True, download_name=assignment.filename)


@assignment_bp.route('/download/submission/<int:submission_id>')
@login_required
@teacher_required
def download_submission(submission_id):
    """Download file bài nộp (chỉ giáo viên)"""
    from app.models.submission import Submission
    
    submission = Submission.query.get(submission_id)
    if not submission:
        flash('Không tìm thấy bài nộp', 'danger')
        return redirect(url_for('assignment.list_assignments'))
    
    # IDOR Fix: Kiểm tra giáo viên có phải là người tạo assignment không
    if submission.assignment.teacher_id != current_user.id:
        flash('Bạn không có quyền download bài nộp này', 'danger')
        return redirect(url_for('assignment.list_assignments'))
    
    # Kiểm tra file có tồn tại không
    if not FileService.file_exists(submission.file_path):
        flash('File không tồn tại', 'danger')
        return redirect(url_for('assignment.view_submissions', assignment_id=submission.assignment_id))
    
    file_path = FileService.get_file_path(submission.file_path)
    return send_file(file_path, as_attachment=True, download_name=submission.filename)


@assignment_bp.route('/<int:assignment_id>/delete', methods=['POST'])
@login_required
@teacher_required
def delete(assignment_id):
    """Xóa bài tập (chỉ giáo viên)"""
    assignment = AssignmentService.get_assignment_by_id(assignment_id)
    if not assignment:
        flash('Không tìm thấy bài tập', 'danger')
        return redirect(url_for('assignment.list_assignments'))
    
    # IDOR Fix: Chỉ cho phép giáo viên xóa assignment của chính mình
    if assignment.teacher_id != current_user.id:
        flash('Bạn không có quyền xóa assignment này', 'danger')
        return redirect(url_for('assignment.list_assignments'))
    
    # Xóa file nếu có
    if assignment.has_file():
        FileService.delete_file(assignment.file_path)
    
    # Xóa tất cả file submissions
    for submission in assignment.submissions:
        FileService.delete_file(submission.file_path)
    
    # Xóa assignment
    success, error = AssignmentService.delete_assignment(assignment_id)
    if not success:
        flash(f'Lỗi: {error}', 'danger')
    else:
        flash('Xóa bài tập thành công!', 'success')
    
    return redirect(url_for('assignment.list_assignments'))
