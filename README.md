# Linux Test System

## Giới thiệu
**Linux Test System** là một hệ thống kiểm tra trực tuyến được xây dựng trên nền tảng Django. Dự án cung cấp giao diện quản trị cho admin và giao diện người dùng cho học viên, hỗ trợ quản lý bài kiểm tra, câu hỏi, kết quả và chứng chỉ.

---

## Cấu trúc dự án

```
linux_test_system/
├── linux_test_system/           # Cấu hình Django
│   ├── settings.py              # Cấu hình chung (MySQL, Authentication, Static Files)
│   ├── urls.py                  # Định tuyến chính của toàn bộ hệ thống
│   ├── wsgi.py
│
├── admin_panel/                 # Ứng dụng Admin (Quản trị hệ thống)
│   ├── models.py                # Mô hình dữ liệu dành riêng cho admin (nếu cần)
│   ├── views.py                 # Các trang quản lý cho admin
│   ├── urls.py                  # Định tuyến admin
│   ├── templates/admin/         # Giao diện dành riêng cho Admin
│       ├── base.html            # Layout Admin
│       ├── dashboard.html       # Trang tổng quan
│       ├── manage_users.html    # Quản lý người dùng
│       ├── manage_exams.html    # Quản lý bài kiểm tra
│       ├── manage_questions.html# Quản lý ngân hàng câu hỏi
│
├── user_panel/                  # Ứng dụng User (Giao diện cho học viên)
│   ├── views.py                 # Xử lý giao diện user (đăng nhập, thi cử, v.v.)
│   ├── urls.py                  # Định tuyến user
│   ├── templates/user/          # Giao diện dành riêng cho User
│       ├── base.html            # Layout User
│       ├── home.html            # Trang chủ
│       ├── exam_list.html       # Danh sách bài kiểm tra
│       ├── take_exam.html       # Làm bài kiểm tra
│       ├── result.html          # Kết quả thi
│
├── questions/                   # Ứng dụng quản lý câu hỏi
│   ├── models.py                # Mô hình câu hỏi
│   ├── views.py                 # Chức năng quản lý câu hỏi
│   ├── urls.py                  # Định tuyến câu hỏi
│
├── exams/                       # Ứng dụng quản lý bài kiểm tra
│   ├── models.py                # Mô hình bài kiểm tra
│   ├── views.py                 # Chức năng tạo/làm bài kiểm tra
│   ├── urls.py                  # Định tuyến bài kiểm tra
│
├── results/                     # Ứng dụng quản lý kết quả
│   ├── models.py                # Lưu kết quả kiểm tra
│   ├── views.py                 # Chức năng chấm điểm, tạo chứng chỉ
│   ├── urls.py                  # Định tuyến kết quả
│
├── certificates/                # Ứng dụng quản lý chứng chỉ
│   ├── models.py                # Lưu chứng chỉ
│   ├── views.py                 # Chức năng tạo chứng chỉ
│   ├── urls.py                  # Định tuyến chứng chỉ
│
├── static/                      # File tĩnh (CSS, JS)
│   ├── admin/                   # CSS, JS dành cho Admin
│   ├── user/                    # CSS, JS dành cho User
│
├── templates/                   # Giao diện chung
│   ├── registration/            # Giao diện đăng nhập, đăng ký
│       ├── login.html
│       ├── register.html
│
├── manage.py                    # Django CLI
```

---

## Tính năng chính
- **Admin Panel**: Quản lý người dùng, bài kiểm tra, câu hỏi và kết quả.
- **User Panel**: Học viên có thể đăng nhập, làm bài kiểm tra và xem kết quả.
- **Quản lý câu hỏi**: Tạo và chỉnh sửa ngân hàng câu hỏi.
- **Quản lý bài kiểm tra**: Tạo bài kiểm tra và theo dõi tiến độ.
- **Chứng chỉ**: Tự động tạo chứng chỉ sau khi hoàn thành bài kiểm tra.

---

## Yêu cầu hệ thống
- Python 3.x
- Django 4.x
- MySQL

---

## Cài đặt
1. Clone repository:
    ```bash
    git clone <repository-url>
    cd linux_test_system
    python manage.py migrate
    ```
2. Cài đặt các gói phụ thuộc:
    ```bash
    pip install -r requirements.txt
    ```
3. Cấu hình cơ sở dữ liệu trong `settings.py`.
4. Chạy migrations:
    ```bash
    python manage.py migrate
    ```
5. Chạy server:
    ```bash
    python manage.py runserver
    ```

---

## Đóng góp
Mọi đóng góp đều được hoan nghênh! Vui lòng tạo pull request hoặc mở issue để thảo luận.

---

## Giấy phép
Dự án này được phát hành dưới giấy phép [MIT](LICENSE).  