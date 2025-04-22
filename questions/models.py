from django.db import models, transaction
from django.core.validators import FileExtensionValidator
from django.utils import timezone
from django.core.exceptions import ValidationError


class Topic(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name
    
class Question(models.Model):
    CONTENT_TYPES = [
        ('text', 'Text Only'),
        ('image', 'Image'),
        ('video', 'Video'),
    ]

    QUESTION_TYPES = [
        ('single', 'Single Answer'),
        ('multiple', 'Multiple Answers'),
        ('true_false', 'True/False'),
        ('fill_blank', 'Fill in the Blank'),
    ]

    DIFFICULTY_LEVELS = [
        ('easy', 'Easy'),
        ('medium', 'Medium'),
        ('hard', 'Hard'),
    ]

    text = models.TextField(verbose_name='Question Text', null=True, blank=True, default='')
    content_type = models.CharField(max_length=10, choices=CONTENT_TYPES, default='text')
    question_type = models.CharField(max_length=20, choices=QUESTION_TYPES)
    difficulty = models.CharField(max_length=10, choices=DIFFICULTY_LEVELS, default='medium')
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True, blank=True, related_name="questions")
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

    # Câu trả lời cho True/False hoặc Fill-in-the-blank
    correct_answer_text = models.TextField(null=True, blank=True)
    correct_answers = models.ManyToManyField('Option', blank=True, related_name='correct_for_questions')

    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.get_question_type_display()} - {self.text[:50]}..."

    @transaction.atomic
    def save(self, *args, **kwargs):
     
        is_new = self.pk is None
        super().save(*args, **kwargs)
        
        # M2M relationships need to be handled after save
        if not is_new and hasattr(self, '_clear_correct_answers'):
            self.correct_answers.clear()
            delattr(self, '_clear_correct_answers')

    def clean(self):
        if self.content_type == 'image' and not self.image:
            raise ValidationError('Phải có hình ảnh cho câu hỏi dạng hình ảnh.')
        if self.content_type == 'video' and not self.video:
            raise ValidationError('Phải có video cho câu hỏi dạng video.')

        if self.question_type == 'true_false':
            if self.correct_answer_text not in ['true', 'false']:
                raise ValidationError('Đáp án đúng cho câu hỏi đúng/sai phải là "true" hoặc "false".')

        if self.question_type == 'fill_blank':
            if not self.correct_answer_text:
                raise ValidationError('Phải cung cấp đáp án đúng cho câu hỏi điền khuyết.')

        if self.question_type in ['single', 'multiple']:
            if not self.pk:
                return  # Chỉ kiểm tra khi đã lưu và có ID

            if self.options.count() != 4:
                raise ValidationError('Câu hỏi phải có đủ 4 đáp án A, B, C, D.')

            if self.question_type == 'single' and self.correct_answers.count() != 1:
                raise ValidationError('Câu hỏi một đáp án phải có đúng 1 đáp án đúng.')

            if self.question_type == 'multiple' and self.correct_answers.count() < 1:
                raise ValidationError('Câu hỏi nhiều đáp án phải có ít nhất 1 đáp án đúng.')

class Option(models.Model):
    question = models.ForeignKey(Question, related_name='options', on_delete=models.CASCADE)
    key = models.CharField(max_length=1, choices=[('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D')])
    text = models.TextField()

    class Meta:
        unique_together = ('question', 'key')

    def __str__(self):
        return f"{self.key}: {self.text[:50]}..."

