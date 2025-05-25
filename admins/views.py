from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib import messages
from django.views.decorators.csrf import csrf_protect
from django.urls import reverse
from django.shortcuts import render
from django.contrib.auth.models import User
from user_panel.models import SupportRequest, Notification
from .forms import SupportResponseForm
from exams.models import Exam
from certificates.models import Result




@csrf_protect
def admin_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        
        if user is not None and user.is_staff:  # Chỉ cho phép admin đăng nhập
            login(request, user)
            return redirect(reverse("admin_dashboard"))  # Chuyển hướng sau khi đăng nhập thành công
        else:
            messages.error(request, "Tên đăng nhập hoặc mật khẩu không đúng.")

    return render(request, "login.html")


@login_required
def admin_dashboard(request):
    if not request.user.is_staff:  # Chỉ cho phép admin truy cập
        return redirect("admin_login")
    total_exams = Exam.objects.count()
    total_users = User.objects.exclude(is_superuser=True).count()  # Loại bỏ admin
    total_certificates = Result.objects.count()
    context = {
        "total_exams": total_exams,
        "total_users": total_users,
        "total_certificates": total_certificates,   
        
 
    }
    return render(request, "dashboard.html", context)

def manage_users(request):
    query = request.GET.get('q', '')  # Lấy từ khóa tìm kiếm
    if query:
        users = User.objects.filter(username__icontains=query)
    else:
        users = User.objects.exclude(is_superuser=True)  # Loại bỏ admin
    
    return render(request, 'manage_users.html', {'users': users, 'query': query})
def delete_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if user:
        user.delete()
        messages.success(request, "Xóa người dùng thành công!")
    return redirect('manage_users')

def edit_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')

        user.username = username
        user.email = email
        user.save()

        messages.success(request, "Cập nhật thông tin thành công!")
        return redirect('manage_users')

    return render(request, 'edit_user.html', {'user': user})
def manage_exams(request):
    return render(request, 'manage_exams.html')

def manage_questions(request):
    return render(request, 'manage_questions.html')

@login_required
def manage_support_requests(request):
    if not request.user.is_staff:
        return redirect("login")

    support_requests = SupportRequest.objects.all().order_by("-created_at")
    return render(request, "manage_support.html", {"support_requests": support_requests})

@login_required
def resolve_support_request(request, request_id):
    if not request.user.is_staff:
        return redirect("login")

    support_request = get_object_or_404(SupportRequest, id=request_id)

    if request.method == "POST":
        form = SupportResponseForm(request.POST, instance=support_request)
        if form.is_valid():
            support_request.status = "resolved"
            support_request.save()

            # Gửi thông báo đến user
            if support_request.user:
                Notification.objects.create(
                    user=support_request.user,
                    message=f"Yêu cầu hỗ trợ của bạn đã được xử lý: {support_request.response}"
                )

            messages.success(request, "Yêu cầu hỗ trợ đã được xử lý và thông báo đã gửi đến người dùng.")
            return redirect("manage_support_requests")
    else:
        form = SupportResponseForm(instance=support_request)

    return render(request, "resolve_support.html", {"form": form, "support_request": support_request})

def logout_view(request):
    logout(request)
    return redirect('login')  # Điều hướng về trang đăng nhập sau khi đăng xuất