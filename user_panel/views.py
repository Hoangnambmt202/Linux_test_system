from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from exams.models import Exam
from results.models import Result
from .models import Notification
from django.contrib.auth import authenticate, login, logout
from .forms import RegisterForm, LoginForm, UserProfileForm , SupportForm
from django.contrib import messages
from django.db.models import Count
from certificates.models import Certificate

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
    exams = Exam.objects.annotate(total_questions=Count('questions'))  # Đếm số câu hỏi ngay trong SQL
    return render(request, 'home.html', {'exams': exams,  'exam_count': exam_count})
   

@login_required
def profile(request):
    return render(request, "profile_info.html")

@login_required
def exam_history_view(request):
    results = Result.objects.filter(user=request.user)
    return render(request, "exam_history.html", {"results": results})

@login_required
def certificates_view(request):
    certificates = Certificate.objects.filter(user=request.user)
    return render(request, "certificates.html", { "certificates": certificates})

@login_required
def support_view(request):
    if request.method == "POST":
        form = SupportForm(request.POST)
        if form.is_valid():
            support_request = form.save(commit=False)
            if request.user.is_authenticated:
                support_request.user = request.user  # Liên kết với tài khoản nếu đã đăng nhập
            support_request.save()
            messages.success(request, "Yêu cầu hỗ trợ của bạn đã được gửi thành công!")
            return redirect("support")
    else:
        form = SupportForm()
    return render(request, "support.html", {"form": form})

@login_required
def notifications_view(request):
    notifications = Notification.objects.filter(user=request.user, is_read=False)
    return render(request, "notifications.html", {"notifications": notifications})
