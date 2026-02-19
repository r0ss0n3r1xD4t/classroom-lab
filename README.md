# Classroom Management System

Hệ thống quản lý lớp học với 2 role: Giáo viên và Sinh viên.

## Công nghệ

- **Backend**: Python + Flask
- **Database**: SQLite
- **Architecture**: MVC Pattern

## Cấu trúc dự án

```
classroom-lab/
├── app/                    # Mã nguồn chính
│   ├── models/            # Database models
│   ├── views/             # HTML templates
│   ├── controllers/       # Routes & logic
│   ├── services/          # Business logic
│   ├── utils/             # Helper functions
│   └── static/            # CSS, JS, uploads
├── instance/              # Config & database
└── run.py                 # Entry point
```

## Chức năng

### Giáo viên
- ✓ Quản lý thông tin sinh viên (CRUD)
- ✓ Upload bài tập
- ✓ Xem danh sách bài nộp
- ✓ Tạo trò chơi giải đố

### Sinh viên
- ✓ Xem và sửa thông tin cá nhân
- ✓ Download bài tập
- ✓ Nộp bài làm
- ✓ Chơi trò chơi giải đố

## Cài đặt

```bash
# Clone project
cd classroom-lab

# Tạo virtual environment
python -m venv venv
venv\Scripts\activate  # Windows

# Cài đặt dependencies
pip install -r requirements.txt

# Chạy ứng dụng
python run.py
```

## Database Schema

- **User**: username, password, fullname, email, phone, role
- **Assignment**: title, description, file_path, created_by, created_at
- **Submission**: assignment_id, student_id, file_path, submitted_at
- **Challenge**: title, content_file, created_by, created_at
