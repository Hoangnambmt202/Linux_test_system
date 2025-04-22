from django.db import models
from django.contrib.auth.models import User
from questions.models import  Question
from django.utils import timezone

class Result(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    exam = models.ForeignKey("exams.Exam", on_delete=models.CASCADE)
    score = models.FloatField()
    total_questions = models.IntegerField()
    correct_answers = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    start_time = models.DateTimeField(default=timezone.now)
    end_time = models.DateTimeField(null=True, blank=True)

class Answer(models.Model):
    result = models.ForeignKey(Result, on_delete=models.CASCADE, related_name="answers")
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    selected_option = models.TextField(null=True, blank=True)  # ✅ sửa ở đây
    is_correct = models.BooleanField()
