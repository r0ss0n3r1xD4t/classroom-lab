# Hướng dẫn Deploy Web Classroom lên Internet

## 🚀 Cách 1: Deploy lên Render.com (Khuyên dùng - Miễn phí)

### Bước 1: Chuẩn bị
1. Tạo tài khoản tại https://render.com
2. Push code lên GitHub

### Bước 2: Tạo Git Repository
```bash
cd classroom-lab
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin <your-github-repo-url>
git push -u origin main
```

### Bước 3: Deploy trên Render
1. Đăng nhập Render.com
2. Click **"New +"** → **"Web Service"**
3. Kết nối GitHub repository của bạn
4. Cấu hình:
   - **Name**: `classroom-app` (hoặc tên bạn thích)
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn run:app`
   - **Plan**: Chọn **Free**

5. Thêm Environment Variables:
   - `SECRET_KEY` = `your-super-secret-key-change-this`
   - `FLASK_ENV` = `production`
   - `PYTHON_VERSION` = `3.11.0`

6. Click **"Create Web Service"**
7. Đợi 5-10 phút để deploy xong

### Bước 4: Truy cập
- URL sẽ có dạng: `https://classroom-app.onrender.com`

---

## 🚀 Cách 2: Deploy lên Railway.app (Đơn giản hơn)

### Bước 1: Chuẩn bị
1. Tạo tài khoản tại https://railway.app
2. Push code lên GitHub

### Bước 2: Deploy
1. Đăng nhập Railway
2. Click **"New Project"** → **"Deploy from GitHub repo"**
3. Chọn repository của bạn
4. Railway tự động detect Flask app
5. Thêm Environment Variables:
   - `SECRET_KEY` = `your-super-secret-key`
   - `FLASK_ENV` = `production`

6. Deploy tự động hoàn tất

---

## 🚀 Cách 3: Deploy lên PythonAnywhere (Dễ nhất)

### Bước 1: Đăng ký
1. Tạo tài khoản miễn phí tại https://www.pythonanywhere.com

### Bước 2: Upload Code
1. Vào **"Files"** → Upload toàn bộ project
2. Hoặc dùng Git:
```bash
git clone <your-repo-url>
```

### Bước 3: Cấu hình Web App
1. Vào **"Web"** → **"Add a new web app"**
2. Chọn **"Flask"** → Python 3.11
3. Cấu hình WSGI file:

```python
import sys
import os

# Thêm đường dẫn project
project_home = '/home/yourusername/classroom-lab'
if project_home not in sys.path:
    sys.path = [project_home] + sys.path

# Set environment variables
os.environ['SECRET_KEY'] = 'your-secret-key'
os.environ['FLASK_ENV'] = 'production'

from run import app as application
```

4. Reload web app
5. Truy cập: `http://yourusername.pythonanywhere.com`

---

## ⚙️ Lưu ý quan trọng

### 1. Database
- SQLite không phù hợp cho production
- Nên dùng PostgreSQL (miễn phí trên Render/Railway)
- Hoặc giữ SQLite nếu chỉ demo nhỏ

### 2. File Upload
- Upload folder cần persistent storage
- Render: Dùng S3, Cloudinary
- Railway: Volume mounting
- PythonAnywhere: Built-in storage

### 3. Security
- Đổi `SECRET_KEY` thành giá trị ngẫu nhiên mạnh
- Bật HTTPS (tự động trên Render/Railway)
- Set `SESSION_COOKIE_SECURE = True`

### 4. Performance
- Free tier có giới hạn: 512MB RAM, sleep sau 15 phút không dùng
- Upgrade nếu cần nhiều người dùng

---

## 🔧 Troubleshooting

### Lỗi Database
```python
# Nếu dùng PostgreSQL, cài thêm:
pip install psycopg2-binary

# Thêm vào requirements.txt:
psycopg2-binary==2.9.9
```

### Lỗi CSRF
```python
# Đảm bảo tất cả form có:
<input type="hidden" name="csrf_token" value="{{ csrf_token() }}"/>
```

### Lỗi Static Files
```python
# Đảm bảo trong config:
STATIC_FOLDER = 'static'
STATIC_URL_PATH = '/static'
```

---

## 📝 Checklist trước khi Deploy

- [x] `requirements.txt` đầy đủ
- [x] `Procfile` đã tạo
- [x] `.gitignore` loại trừ `instance/`, `__pycache__/`
- [x] `SECRET_KEY` từ environment variable
- [x] CSRF protection enabled
- [ ] Database backup (nếu có data)
- [ ] Test local với `gunicorn run:app`

---

## 🎯 Khuyến nghị

**Cho người mới bắt đầu**: Dùng **Railway.app** - Dễ nhất, tự động hóa nhiều

**Cho project thực tế**: Dùng **Render.com** - Stable, nhiều tính năng

**Cho demo/test**: Dùng **PythonAnywhere** - Không cần Git, upload trực tiếp

Chúc bạn deploy thành công! 🚀
