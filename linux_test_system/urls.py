

from django.urls import path, include
from user_panel import views  # Import views của user_panel

urlpatterns = [
    path('admin/', include("admins.urls")),
    path('', views.home, name='home'),  # Trỏ URL gốc vào trang chủ user
    path('', include('user_panel.urls')),  # Load tất cả route của user_panel
]
