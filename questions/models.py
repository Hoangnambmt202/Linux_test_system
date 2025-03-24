from django.db import models

class Question(models.Model):
    TEXT = "text"
    IMAGE = "image"
    VIDEO = "video"
    
    QUESTION_TYPES = [
        (TEXT, "Văn bản"),
        (IMAGE, "Hình ảnh"),
        (VIDEO, "Video"),
    ]

    question_type = models.CharField(max_length=10, choices=QUESTION_TYPES, default=TEXT)
    text = models.TextField(blank=True, null=True)   # Cho phép nhập văn bản mô tả
    media = models.FileField(upload_to="questions_media/", blank=True, null=True)  # Dùng cho hình ảnh hoặc video
    option_a = models.CharField(max_length=255)
    option_b = models.CharField(max_length=255)
    option_c = models.CharField(max_length=255)
    option_d = models.CharField(max_length=255)
    correct_answer = models.CharField(max_length=1)  # A, B, C, hoặc D
    difficulty = models.CharField(max_length=10, choices=[("easy", "Dễ"), ("medium", "Trung bình"), ("hard", "Khó")])

    def __str__(self):
        return self.text if self.text else f"Câu hỏi {self.id} ({self.question_type})"
