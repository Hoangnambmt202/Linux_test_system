from django.db import models
from django.contrib.auth.models import User
from questions.models import  Question

class Result(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    exam = models.ForeignKey("exams.Exam", on_delete=models.CASCADE)
    score = models.FloatField()
    total_questions = models.IntegerField()
    correct_answers = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

class Answer(models.Model):
    result = models.ForeignKey(Result, on_delete=models.CASCADE, related_name="answers")
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    selected_option = models.CharField(max_length=10, null=True, blank=True)
    is_correct = models.BooleanField()
