

from django.urls import path, include
from .views import home
# Tạo một view nhanh để test trang chủ

urlpatterns = [
    path('admin/', include("admins.urls")),
    path('', home, name='home'),  
]
