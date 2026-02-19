from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app.services.user_service import UserService
from app.utils.decorators import teacher_required

user_bp = Blueprint('user', __name__, url_prefix='/users')


@user_bp.route('/')
@login_required
def list_users():
    users = UserService.get_all_users()
    return render_template('user/list.html', users=users)


@user_bp.route('/<int:user_id>')
@login_required
def detail(user_id):
    user = UserService.get_user_by_id(user_id)
    if not user:
        flash('Không tìm thấy người dùng', 'danger')
        return redirect(url_for('user.list_users'))
    return render_template('user/detail.html', user=user)


@user_bp.route('/create', methods=['GET', 'POST'])
@login_required
@teacher_required
def create():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        fullname = request.form.get('fullname')
        email = request.form.get('email')
        phone = request.form.get('phone')
        role = request.form.get('role')
        
        if not all([username, password, fullname, email, role]):
            flash('Vui lòng điền đầy đủ thông tin bắt buộc', 'danger')
            return render_template('user/create.html')
        
        user, error = UserService.create_user(username, password, fullname, email, phone, role)
        if error:
            flash(f'Lỗi: {error}', 'danger')
            return render_template('user/create.html')
        
        flash(f'Tạo user {username} thành công!', 'success')
        return redirect(url_for('user.list_users'))
    
    return render_template('user/create.html')


@user_bp.route('/edit/<int:user_id>', methods=['GET', 'POST'])
@login_required
def edit(user_id):
    user = UserService.get_user_by_id(user_id)
    if not user:
        flash('Không tìm thấy người dùng', 'danger')
        if current_user.is_teacher():
            return redirect(url_for('user.list_users'))
        else:
            return redirect(url_for('auth.home'))
    
    if not current_user.is_teacher() and current_user.id != user_id:
        flash('Bạn không có quyền sửa thông tin người dùng này', 'danger')
        return redirect(url_for('auth.home'))
    
    if request.method == 'POST':
        fullname = request.form.get('fullname')
        email = request.form.get('email')
        phone = request.form.get('phone')
        password = request.form.get('password')
        
        if current_user.is_student() and fullname != user.fullname:
            flash('Sinh viên không được phép thay đổi tên', 'danger')
            return render_template('user/edit.html', user=user)
        
        updated_user, error = UserService.update_user(
            user_id, 
            fullname=fullname, 
            email=email, 
            phone=phone,
            password=password if password else None
        )
        
        if error:
            flash(f'Lỗi: {error}', 'danger')
            return render_template('user/edit.html', user=user)
        
        flash('Cập nhật thông tin thành công!', 'success')
        return redirect(url_for('user.detail', user_id=user_id))
    
    return render_template('user/edit.html', user=user)


@user_bp.route('/delete/<int:user_id>', methods=['POST'])
@login_required
@teacher_required
def delete(user_id):
    if current_user.id == user_id:
        flash('Bạn không thể xóa chính mình', 'danger')
        return redirect(url_for('user.list_users'))
    
    success, error = UserService.delete_user(user_id)
    if error:
        flash(f'Lỗi: {error}', 'danger')
    else:
        flash('Xóa người dùng thành công!', 'success')
    
    return redirect(url_for('user.list_users'))
