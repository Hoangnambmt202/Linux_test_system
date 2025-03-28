from pyexpat.errors import messages
from rest_framework import viewsets
from questions.models import Question
from results.models import Result
from .models import Exam
from certificates.models import Certificate
from django.contrib.auth.decorators import login_required
from .serializers import QuestionSerializer, ExamSerializer
from django.shortcuts import render, get_object_or_404 ,redirect
from django.utils import timezone

class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer

class ExamViewSet(viewsets.ModelViewSet):
    queryset = Exam.objects.all()
    serializer_class = ExamSerializer


def exam_list(request):
    exams = Exam.objects.all()
    return render(request, 'exam_list.html', {'exams': exams})

def manage_exams(request):
    exams = Exam.objects.all()
    total_duration = sum(exam.duration for exam in exams)  # Tính tổng thời gian
    exam_count = exams.count()  # Đếm số lượng bài thi

    # Tính thời gian trung bình, tránh lỗi chia cho 0
    average_duration = total_duration / exam_count if exam_count > 0 else 0
    # Tính tổng số câu hỏi trong tất cả các bài thi
    total_questions = sum(exam.questions.count() for exam in exams)
    # Tính tổng số câu hỏi trong một bài thi
    total_questions_in_exam = [exam.questions.count() for exam in exams]

    return render(request, 'manage_exams.html', {
        'exams': exams,
        'average_duration': round(average_duration, 2),  # Làm tròn 2 chữ số
        'total_questions_in_exam': total_questions_in_exam,
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
        exam.date = request.POST["date"]
        exam.questions.set(selected_questions)
        exam.save()
        return redirect("manage_exams")

    return render(request, "edit_exam.html", {"exam": exam, "questions": questions})

def delete_exam(request, exam_id):
    exam = get_object_or_404(Exam, id=exam_id)
    exam.delete()
    return redirect("manage_exams")

@login_required
def take_exam(request, exam_id):
    exam = get_object_or_404(Exam, id=exam_id)
    questions = exam.questions.all().order_by('?')  # Trộn câu hỏi
    
    # Kiểm tra xem user đã làm bài này chưa
    existing_result = Result.objects.filter(user=request.user, exam=exam).exists()
    result = Result.objects.filter(user=request.user, exam=exam).first()
    # answers = result.answers.all()
    certificate = Certificate.objects.filter(result=result).first()  # Lấy chứng chỉ nếu có
    if existing_result:
        return render(request, "result_detail_user.html", {
        "result": result,
        # "answers": answers,
        "certificate": certificate
    })
    
    return render(request, "take_exam.html", {
        "exam": exam,
        "questions": questions,
        "duration_minutes": exam.duration,
    })
