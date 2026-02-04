from functools import wraps
from flask import redirect, url_for, flash, abort
from flask_login import current_user

def teacher_required(f):
    """Decorator yêu cầu user phải là giáo viên"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            flash('Vui lòng đăng nhập để truy cập trang này.', 'warning')
            return redirect(url_for('auth.login'))
        if not current_user.is_teacher():
            flash('Bạn không có quyền truy cập trang này. Chỉ giáo viên mới được phép.', 'danger')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

def student_required(f):
    """Decorator yêu cầu user phải là sinh viên"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            flash('Vui lòng đăng nhập để truy cập trang này.', 'warning')
            return redirect(url_for('auth.login'))
        if not current_user.is_student():
            flash('Bạn không có quyền truy cập trang này. Chỉ sinh viên mới được phép.', 'danger')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function
