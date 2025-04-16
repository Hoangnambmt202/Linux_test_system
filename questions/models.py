from django.db import models
from django.core.validators import FileExtensionValidator
from django.utils import timezone

class Question(models.Model):
    # Loại nội dung câu hỏi
    CONTENT_TYPES = [
        ('text', 'Text Only'),
        ('image', 'Image'),
        ('video', 'Video'),
    ]

    # Loại câu hỏi
    QUESTION_TYPES = [
        ('single', 'Single Answer'),
        ('multiple', 'Multiple Answers'),
        ('true_false', 'True/False'),
        ('fill_blank', 'Fill in the Blank'),
    ]

    # Độ khó
    DIFFICULTY_LEVELS = [
        ('easy', 'Easy'),
        ('medium', 'Medium'),
        ('hard', 'Hard'),
    ]

    # Thông tin cơ bản
    text = models.TextField(verbose_name='Question Text', null=True, blank=True, default='')
    content_type = models.CharField(max_length=10, choices=CONTENT_TYPES, default='text')
    question_type = models.CharField(max_length=20, choices=QUESTION_TYPES)
    difficulty = models.CharField(max_length=10, choices=DIFFICULTY_LEVELS, default='medium')

    # Media fields
    image = models.ImageField(
        upload_to='question_images/',
        null=True,
        blank=True,
        validators=[FileExtensionValidator(['jpg', 'jpeg', 'png', 'gif'])]
    )
    video = models.FileField(
        upload_to='question_videos/',
        null=True,
        blank=True,
        validators=[FileExtensionValidator(['mp4', 'webm', 'ogg'])]
    )

    # Các đáp án - sử dụng TextField thay vì JSONField cho MySQL
    options = models.TextField(null=True, blank=True, help_text='JSON string containing answer options')
    correct_answer = models.TextField(help_text='Correct answer(s) - JSON string for multiple choice')

    # Thời gian tạo và cập nhật
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.get_question_type_display()} - {self.text[:50]}..."

    def get_correct_answers(self):
        """Trả về danh sách các đáp án đúng dựa vào loại câu hỏi"""
        import json
        if self.question_type == 'multiple':
            try:
                return json.loads(self.correct_answer)
            except json.JSONDecodeError:
                return []
        return self.correct_answer

    def check_answer(self, user_answer):
        """Kiểm tra câu trả lời của người dùng"""
        import json
        if self.question_type == 'multiple':
            try:
                correct_answers = set(json.loads(self.correct_answer))
                user_answers = set(json.loads(user_answer) if isinstance(user_answer, str) else user_answer)
                return correct_answers == user_answers
            except json.JSONDecodeError:
                return False
        elif self.question_type == 'true_false':
            return str(user_answer).lower() == self.correct_answer.lower()
        elif self.question_type == 'fill_blank':
            return user_answer.strip().lower() == self.correct_answer.strip().lower()
        else:  # single choice
            return user_answer == self.correct_answer

    def clean(self):
        from django.core.exceptions import ValidationError
        import json
        
        # Validate content type and associated files
        if self.content_type == 'image' and not self.image:
            raise ValidationError('Image file is required for image questions')
        if self.content_type == 'video' and not self.video:
            raise ValidationError('Video file is required for video questions')
            
        # Validate options and correct answers based on question type
        if self.question_type in ['single', 'multiple']:
            if not self.options:
                raise ValidationError('Options are required for single/multiple choice questions')
            try:
                options_dict = json.loads(self.options) if isinstance(self.options, str) else self.options
                if not all(key in options_dict for key in ['A', 'B', 'C', 'D']):
                    raise ValidationError('Options must contain choices A, B, C, and D')
            except json.JSONDecodeError:
                raise ValidationError('Invalid options format')
                
            if self.question_type == 'multiple':
                try:
                    correct_answers = json.loads(self.correct_answer)
                    if not isinstance(correct_answers, list):
                        raise ValidationError('Correct answers must be a JSON array for multiple choice questions')
                    if not all(ans in ['A', 'B', 'C', 'D'] for ans in correct_answers):
                        raise ValidationError('Invalid correct answers')
                except json.JSONDecodeError:
                    raise ValidationError('Invalid correct answers format')
            else:  # single choice
                if self.correct_answer not in ['A', 'B', 'C', 'D']:
                    raise ValidationError('Correct answer must be A, B, C, or D for single choice questions')
                    
        elif self.question_type == 'true_false':
            if self.correct_answer not in ['true', 'false']:
                raise ValidationError('Correct answer must be true or false')
                
        # For fill_blank, any non-empty correct_answer is valid
