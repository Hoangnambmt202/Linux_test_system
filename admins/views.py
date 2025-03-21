from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib import messages
from django.views.decorators.csrf import csrf_protect
from django.urls import reverse
from django.shortcuts import render
from django.contrib.auth.models import User

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

    context = {
        "total_exams": 10,  # Thống kê giả định
        "total_users": 200,
        "total_certificates": 50,
    }
    return render(request, "dashboard.html", context)

def manage_users(request):
    query = request.GET.get('q', '')  # Lấy từ khóa tìm kiếm
    if query:
        users = User.objects.filter(username__icontains=query)
    else:
        users = User.objects.all()
    
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
def logout_view(request):
    logout(request)
    return redirect('login')  # Điều hướng về trang đăng nhập sau khi đăng xuất