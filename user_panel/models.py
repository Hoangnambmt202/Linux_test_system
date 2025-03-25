from django.db import models
from django.contrib.auth.models import User

class SupportRequest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    message = models.TextField()
    response = models.TextField(blank=True, null=True)  # Phản hồi từ admin
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=20, 
        choices=[('pending', 'Chờ xử lý'), ('resolved', 'Đã xử lý')],
        default='pending'
    )

    def __str__(self):
        return f"{self.name} - {self.status}"
    
class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)  # Kiểm tra nếu user đã đọc

    def __str__(self):
        return f"Thông báo cho {self.user.username}"
