from pyexpat.errors import messages
from rest_framework import viewsets
from questions.models import Question
from .models import Exam
from django.contrib.auth.decorators import login_required
from .serializers import QuestionSerializer, ExamSerializer
from django.shortcuts import render, get_object_or_404 ,redirect

class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer

class ExamViewSet(viewsets.ModelViewSet):
    queryset = Exam.objects.all()
    serializer_class = ExamSerializer

def exam_list(request):
    exams = Exam.objects.all()
    total_duration = sum(exam.duration for exam in exams)  # Tính tổng thời gian
    exam_count = exams.count()  # Đếm số lượng bài thi

    # Tính thời gian trung bình, tránh lỗi chia cho 0
    average_duration = total_duration / exam_count if exam_count > 0 else 0
    # Tính tổng số câu hỏi trong tất cả các bài thi
    total_questions = sum(exam.questions.count() for exam in exams)

    return render(request, 'exam_list.html', {
        'exams': exams,
        'average_duration': round(average_duration, 2),  # Làm tròn 2 chữ số
        'total_questions': total_questions,
    })

def add_exam(request):
    questions = Question.objects.all()
    
    if request.method == "POST":
        title = request.POST["title"]
        description = request.POST.get("description", "")
        duration = request.POST["duration"]
        selected_questions = request.POST.getlist("questions")

        exam = Exam.objects.create(title=title, description=description, duration=duration)
        exam.questions.set(selected_questions)
        exam.save()
        
        return redirect("manage_exams")

    return render(request, "add_exam.html", {"questions": questions})

def edit_exam(request, exam_id):
    exam = get_object_or_404(Exam, id=exam_id)
    questions = Question.objects.all()

    if request.method == "POST":
        exam.title = request.POST["title"]
        exam.description = request.POST.get("description", "")
        exam.duration = request.POST["duration"]
        selected_questions = request.POST.getlist("questions")
        
        exam.questions.set(selected_questions)
        exam.save()
        return redirect("manage_exams")

    return render(request, "edit_exam.html", {"exam": exam, "questions": questions})

def delete_exam(request, exam_id):
    exam = get_object_or_404(Exam, id=exam_id)
    exam.delete()
    return redirect("manage_exams")

