from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from flask_login import login_required, current_user
from app.services.challenge_service import ChallengeService
from app.utils.decorators import teacher_required

challenge_bp = Blueprint('challenge', __name__, url_prefix='/challenges')


@challenge_bp.route('/')
@login_required
def list_challenges():
    """Hiển thị danh sách challenges"""
    if current_user.is_teacher():
        # Giáo viên thấy tất cả challenges (kể cả đã deactivate)
        challenges = ChallengeService.get_all_challenges_for_teacher()
    else:
        # Sinh viên chỉ thấy challenges đang hoạt động
        challenges = ChallengeService.get_all_challenges()
    
    return render_template('challenge/list.html', challenges=challenges)


@challenge_bp.route('/create', methods=['GET', 'POST'])
@login_required
@teacher_required
def create():
    """Tạo challenge mới (chỉ giáo viên)"""
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        hint = request.form.get('hint')
        file = request.files.get('file')
        
        # Validate
        if not title:
            flash('Vui lòng nhập tiêu đề challenge', 'danger')
            return render_template('challenge/create.html')
        
        if not file or not file.filename:
            flash('Vui lòng upload file .txt', 'danger')
            return render_template('challenge/create.html')
        
        # Lưu file và lấy tên file (đây sẽ là đáp án)
        file_path, result = ChallengeService.save_challenge_file(file, current_user.id)
        if file_path is None:
            flash(f'Lỗi upload file: {result}', 'danger')
            return render_template('challenge/create.html')
        
        filename_without_ext = result
        
        # Tạo challenge
        challenge, error = ChallengeService.create_challenge(
            title=title,
            description=description,
            teacher_id=current_user.id,
            file_path=file_path,
            filename=filename_without_ext,
            hint=hint
        )
        
        if error:
            flash(f'Lỗi: {error}', 'danger')
            # Xóa file đã upload nếu tạo challenge thất bại
            ChallengeService.delete_challenge_file(file_path)
            return render_template('challenge/create.html')
        
        flash(f'Tạo challenge thành công! Đáp án là: {filename_without_ext}', 'success')
        return redirect(url_for('challenge.list_challenges'))
    
    return render_template('challenge/create.html')


@challenge_bp.route('/<int:challenge_id>/play', methods=['GET', 'POST'])
@login_required
def play(challenge_id):
    if not current_user.is_student():
        flash('Chỉ sinh viên mới có thể chơi challenge', 'danger')
        return redirect(url_for('challenge.list_challenges'))
    
    challenge = ChallengeService.get_challenge_by_id(challenge_id)
    if not challenge:
        flash('Không tìm thấy challenge', 'danger')
        return redirect(url_for('challenge.list_challenges'))
    
    if not challenge.is_active:
        flash('Challenge này đã bị vô hiệu hóa', 'warning')
        return redirect(url_for('challenge.list_challenges'))
    
    if request.method == 'POST':
        user_answer = request.form.get('answer')
        
        if not user_answer:
            flash('Vui lòng nhập đáp án', 'warning')
            return render_template('challenge/play.html', challenge=challenge)
        
        is_correct = challenge.check_answer(user_answer)
        
        content = None
        if is_correct:
            content, error = ChallengeService.read_challenge_content(challenge)
            if error:
                flash(f'Lỗi khi đọc nội dung: {error}', 'danger')
        
        session['challenge_result'] = {
            'challenge_id': challenge.id,
            'challenge_title': challenge.title,
            'user_answer': user_answer,
            'correct_answer': challenge.get_answer(),
            'is_correct': is_correct,
            'content': content
        }
        
        return redirect(url_for('challenge.result'))
    
    return render_template('challenge/play.html', challenge=challenge)


@challenge_bp.route('/result')
@login_required
def result():
    result_data = session.pop('challenge_result', None)
    
    if not result_data:
        flash('Không có kết quả để hiển thị', 'warning')
        return redirect(url_for('challenge.list_challenges'))
    
    content = result_data.get('content')
    return render_template('challenge/result.html', result=result_data, content=content)


@challenge_bp.route('/<int:challenge_id>/deactivate', methods=['POST'])
@login_required
@teacher_required
def deactivate(challenge_id):
    """Vô hiệu hóa challenge (giáo viên)"""
    challenge = ChallengeService.get_challenge_by_id(challenge_id)
    if not challenge:
        flash('Không tìm thấy challenge', 'danger')
        return redirect(url_for('challenge.list_challenges'))
    
    # IDOR Fix: Chỉ giáo viên tạo challenge mới được deactivate
    if challenge.teacher_id != current_user.id:
        flash('Bạn không có quyền vô hiệu hóa challenge này', 'danger')
        return redirect(url_for('challenge.list_challenges'))
    
    success, error = ChallengeService.deactivate_challenge(challenge_id)
    if not success:
        flash(f'Lỗi: {error}', 'danger')
    else:
        flash('Vô hiệu hóa challenge thành công!', 'success')
    
    return redirect(url_for('challenge.list_challenges'))


@challenge_bp.route('/<int:challenge_id>/delete', methods=['POST'])
@login_required
@teacher_required
def delete(challenge_id):
    """Xóa challenge hoàn toàn (giáo viên)"""
    challenge = ChallengeService.get_challenge_by_id(challenge_id)
    if not challenge:
        flash('Không tìm thấy challenge', 'danger')
        return redirect(url_for('challenge.list_challenges'))
    
    # IDOR Fix: Chỉ giáo viên tạo challenge mới được xóa
    if challenge.teacher_id != current_user.id:
        flash('Bạn không có quyền xóa challenge này', 'danger')
        return redirect(url_for('challenge.list_challenges'))
    
    # Xóa file
    ChallengeService.delete_challenge_file(challenge.file_path)
    
    # Xóa challenge
    success, error = ChallengeService.delete_challenge(challenge_id)
    if not success:
        flash(f'Lỗi: {error}', 'danger')
    else:
        flash('Xóa challenge thành công!', 'success')
    
    return redirect(url_for('challenge.list_challenges'))


@challenge_bp.route('/<int:challenge_id>/view')
@login_required
@teacher_required
def view(challenge_id):
    challenge = ChallengeService.get_challenge_by_id(challenge_id)
    if not challenge:
        flash('Không tìm thấy challenge', 'danger')
        return redirect(url_for('challenge.list_challenges'))
    
    content, error = ChallengeService.read_challenge_content(challenge)
    if error:
        flash(f'Lỗi: {error}', 'danger')
        return redirect(url_for('challenge.list_challenges'))
    
    return render_template('challenge/detail.html', 
                         challenge=challenge, 
                         content=content)
