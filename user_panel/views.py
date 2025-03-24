from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from exams.models import Exam
from results.models import Result
from django.contrib.auth import authenticate, login, logout
from .forms import RegisterForm, LoginForm, UserProfileForm
from django.contrib import messages

# Trang Đăng ký
def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])  # Mã hóa mật khẩu
            user.save()
            messages.success(request, "Đăng ký thành công! Hãy đăng nhập.")
            return redirect('login')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})

# Trang Đăng nhập
def login_view(request):
    if request.method == "POST":
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')  # Điều hướng về trang chủ user
    else:
        form = LoginForm()
    return render(request, 'login_user.html', {'form': form})

# Đăng xuất
def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def edit_profile(request):
    if request.method == "POST":
        form = UserProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Cập nhật thông tin thành công!")
            return redirect('profile')  # Chuyển hướng về trang profile
    else:
        form = UserProfileForm(instance=request.user)

    return render(request, 'edit_profile.html', {'form': form})

@login_required
def home(request):
    exams = Exam.objects.all()
    exam_count = exams.count()  # Đếm số lượng bài thi
    total_questions = sum(exam.questions.count() for exam in exams)
    return render(request, 'home.html', {'exams': exams, 'total_questions': total_questions, 'exam_count': exam_count})
   

@login_required
def profile(request):
    return render(request, "profile_info.html", {"page_title": "Thông tin cá nhân"})

@login_required
def exam_history_view(request):
    results = Result.objects.filter(user=request.user)
    return render(request, "exam_history.html", {"page_title": "Lịch sử bài kiểm tra", "results": results})

@login_required
def certificates_view(request):
    certificates = [
        {"name": "Chứng chỉ Linux Basic", "download_link": "/media/certificates/linux_basic.pdf"},
        {"name": "Chứng chỉ Linux Advanced", "download_link": "/media/certificates/linux_advanced.pdf"},
    ]
    return render(request, "certificates.html", {"page_title": "Chứng chỉ đã đạt", "certificates": certificates})

@login_required
def support_view(request):
    return render(request, "support.html", {"page_title": "Hỗ trợ"})