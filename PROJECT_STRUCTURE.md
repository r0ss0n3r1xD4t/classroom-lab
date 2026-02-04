# Classroom Management System - Project Structure (MVC Pattern)

```
classroom-lab/
│
├── app/
│   ├── __init__.py                 # Flask app factory, khởi tạo extensions
│   ├── config.py                   # Cấu hình ứng dụng (development, production)
│   │
│   ├── models/                     # MODEL - Định nghĩa database models
│   │   ├── __init__.py
│   │   ├── user.py                 # Model User (username, password, fullname, email, phone, role)
│   │   ├── assignment.py           # Model Assignment (bài tập được giao)
│   │   ├── submission.py           # Model Submission (bài nộp của sinh viên)
│   │   └── challenge.py            # Model Challenge (trò chơi giải đố)
│   │
│   ├── views/                      # VIEW - Templates HTML
│   │   ├── base.html               # Template base layout
│   │   ├── auth/
│   │   │   ├── login.html          # Trang đăng nhập
│   │   │   └── register.html       # Trang đăng ký
│   │   ├── user/
│   │   │   ├── list.html           # Danh sách người dùng
│   │   │   ├── detail.html         # Chi tiết người dùng
│   │   │   ├── edit.html           # Chỉnh sửa thông tin
│   │   │   └── create.html         # Tạo người dùng mới (giáo viên)
│   │   ├── assignment/
│   │   │   ├── list.html           # Danh sách bài tập
│   │   │   ├── upload.html         # Upload bài tập (giáo viên)
│   │   │   ├── submit.html         # Nộp bài (sinh viên)
│   │   │   └── submissions.html    # Xem danh sách bài nộp (giáo viên)
│   │   └── challenge/
│   │       ├── list.html           # Danh sách challenge
│   │       ├── create.html         # Tạo challenge (giáo viên)
│   │       ├── play.html           # Chơi challenge (sinh viên)
│   │       └── result.html         # Kết quả challenge
│   │
│   ├── controllers/                # CONTROLLER - Business logic & routes
│   │   ├── __init__.py
│   │   ├── auth_controller.py      # Xử lý đăng nhập, đăng ký, đăng xuất
│   │   ├── user_controller.py      # Quản lý thông tin người dùng
│   │   ├── assignment_controller.py # Quản lý giao bài, trả bài
│   │   └── challenge_controller.py  # Quản lý trò chơi giải đố
│   │
│   ├── services/                   # SERVICE - Business logic layer
│   │   ├── __init__.py
│   │   ├── auth_service.py         # Logic xác thực
│   │   ├── user_service.py         # Logic quản lý user
│   │   ├── assignment_service.py   # Logic quản lý bài tập
│   │   ├── file_service.py         # Logic xử lý file upload/download
│   │   └── challenge_service.py    # Logic xử lý challenge (không lưu đáp án)
│   │
│   ├── utils/                      # UTILITIES - Các helper functions
│   │   ├── __init__.py
│   │   ├── decorators.py           # Custom decorators (role_required, login_required)
│   │   ├── validators.py           # Validate dữ liệu đầu vào
│   │   └── helpers.py              # Các hàm tiện ích khác
│   │
│   └── static/                     # STATIC FILES
│       ├── css/
│       │   └── style.css           # Custom styles
│       ├── js/
│       │   └── main.js             # Custom JavaScript
│       └── uploads/                # Thư mục lưu file upload
│           ├── assignments/        # File bài tập (giáo viên upload)
│           ├── submissions/        # File bài nộp (sinh viên upload)
│           └── challenges/         # File challenge (txt - bài thơ, văn)
│
├── migrations/                     # Database migrations (Flask-Migrate)
│
├── tests/                          # Unit tests
│   ├── __init__.py
│   ├── test_auth.py
│   ├── test_user.py
│   ├── test_assignment.py
│   └── test_challenge.py
│
├── instance/                       # Instance-specific files
│   └── config.py                   # Secret config (không commit lên git)
│
├── run.py                          # Entry point - chạy ứng dụng
├── requirements.txt                # Python dependencies
├── .env                            # Environment variables
├── .gitignore                      # Git ignore file
└── README.md                       # Tài liệu dự án
```

## Giải thích cấu trúc theo MVC:

### 1. MODEL (`app/models/`)
- Định nghĩa cấu trúc database
- Các entity: User, Assignment, Submission, Challenge

### 2. VIEW (`app/views/`)
- Templates HTML sử dụng Jinja2
- Giao diện người dùng cho từng chức năng

### 3. CONTROLLER (`app/controllers/`)
- Xử lý request/response
- Điều hướng logic giữa Model và View

### 4. SERVICE (`app/services/`)
- Business logic tách biệt khỏi controller
- Dễ test và maintain

## Roles và Permissions:

| Chức năng | Giáo viên | Sinh viên |
|-----------|-----------|-----------|
| Xem danh sách người dùng | ✓ | ✓ |
| Xem chi tiết người dùng | ✓ | ✓ |
| Thêm/Sửa/Xóa sinh viên | ✓ | ✗ |
| Sửa thông tin cá nhân | ✓ | ✓ (trừ tên, username) |
| Upload bài tập | ✓ | ✗ |
| Download bài tập | ✓ | ✓ |
| Nộp bài | ✗ | ✓ |
| Xem danh sách bài nộp | ✓ | ✗ |
| Tạo Challenge | ✓ | ✗ |
| Chơi Challenge | ✗ | ✓ |


Phase 2: Quản lý User
Công việc:
Tạo controllers/user_controller.py
Tạo services/user_service.py
Tạo views/user/list.html - Danh sách người dùng
Tạo views/user/detail.html - Chi tiết 1 người
Tạo views/user/edit.html - Sửa thông tin
Tạo views/user/create.html - Tạo user mới (teacher only)
Output Phase 2:
✓ Xem danh sách tất cả users
✓ Xem chi tiết 1 user
✓ Giáo viên: thêm/sửa/xóa sinh viên
✓ Sinh viên: sửa thông tin cá nhân (trừ tên, username)
Phase 3: Giao bài - Trả bài
Công việc:
Tạo models/assignment.py + models/submission.py
Tạo controllers/assignment_controller.py
Tạo services/assignment_service.py
Tạo services/file_service.py
Tạo views/assignment/list.html
Tạo views/assignment/upload.html (teacher)
Tạo views/assignment/submit.html (student)
Tạo views/assignment/submissions.html (teacher)
Output Phase 3:
✓ Giáo viên upload bài tập
✓ Sinh viên xem và download bài tập
✓ Sinh viên nộp bài
✓ Giáo viên xem danh sách bài nộp
Phase 4: Challenge (Giải đố)
Công việc:
Tạo models/challenge.py
Tạo controllers/challenge_controller.py
Tạo services/challenge_service.py
Tạo views/challenge/list.html
Tạo views/challenge/create.html (teacher)
Tạo views/challenge/play.html (student)
Tạo views/challenge/result.html
Output Phase 4:
✓ Giáo viên tạo challenge (upload file txt)
✓ Sinh viên gợi ý và nhập đáp án
✓ Check đáp án = tên file (không lưu DB)
