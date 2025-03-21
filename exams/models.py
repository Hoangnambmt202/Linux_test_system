from django.db import models
from django.apps import apps

class Exam(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True, default="Không có mô tả")
    duration = models.IntegerField(default=60, help_text="Thời gian thi (phút)")  # minutes
    questions = models.ManyToManyField("questions.Question")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
