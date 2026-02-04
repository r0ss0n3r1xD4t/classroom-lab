from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from app import db
from app.models.user import User

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/')
def index():
    """Trang chủ - redirect về login hoặc home"""
    if current_user.is_authenticated:
        return redirect(url_for('auth.home'))
    return redirect(url_for('auth.login'))

@auth_bp.route('/auth/login', methods=['GET', 'POST'])
def login():
    """Trang đăng nhập"""
    if current_user.is_authenticated:
        return redirect(url_for('auth.home'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        # Tìm user trong database
        user = User.query.filter_by(username=username).first()
        
        # Kiểm tra user và password
        if user and user.check_password(password):
            login_user(user)
            flash(f'Chào mừng {user.fullname}!', 'success')
            return redirect(url_for('auth.home'))
        else:
            flash('Tên đăng nhập hoặc mật khẩu không đúng!', 'danger')
    
    return render_template('auth/login.html')

@auth_bp.route('/auth/register', methods=['GET', 'POST'])
def register():
    """Trang đăng ký tài khoản"""
    if current_user.is_authenticated:
        return redirect(url_for('auth.home'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        fullname = request.form.get('fullname')
        email = request.form.get('email')
        phone = request.form.get('phone')
        role = request.form.get('role', 'student')  # Mặc định là sinh viên
        
        # Kiểm tra username đã tồn tại chưa
        if User.query.filter_by(username=username).first():
            flash('Tên đăng nhập đã tồn tại!', 'danger')
            return render_template('auth/register.html')
        
        # Kiểm tra email đã tồn tại chưa
        if User.query.filter_by(email=email).first():
            flash('Email đã được sử dụng!', 'danger')
            return render_template('auth/register.html')
        
        # Tạo user mới
        new_user = User(
            username=username,
            fullname=fullname,
            email=email,
            phone=phone,
            role=role
        )
        new_user.set_password(password)
        
        # Lưu vào database
        db.session.add(new_user)
        db.session.commit()
        
        flash('Đăng ký thành công! Vui lòng đăng nhập.', 'success')
        return redirect(url_for('auth.login'))
    
    return render_template('auth/register.html')

@auth_bp.route('/auth/logout')
@login_required
def logout():
    """Đăng xuất"""
    logout_user()
    flash('Đã đăng xuất thành công!', 'info')
    return redirect(url_for('auth.login'))

@auth_bp.route('/auth/home')
@login_required
def home():
    """Trang chủ sau khi đăng nhập"""
    return render_template('home.html')
