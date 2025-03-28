from django.db import models
from django.contrib.auth.models import User
from results.models import Result

class Certificate(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    result = models.OneToOneField(Result, on_delete=models.CASCADE)  # Chứng chỉ chỉ có 1 kết quả
    issue_date = models.DateTimeField(auto_now_add=True)
    

    def __str__(self):
        return f"Certificate for {self.user.username} - {self.result.exam.title}"
