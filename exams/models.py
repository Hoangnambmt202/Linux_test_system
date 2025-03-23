from django.db import models


class Exam(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True, default="Không có mô tả")
    date = models.DateField(default="2025-01-01", help_text="Ngày thi")
    duration = models.IntegerField(default=60, help_text="Thời gian thi (phút)") 
    questions = models.ManyToManyField("questions.Question")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
