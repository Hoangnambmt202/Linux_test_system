from pyexpat.errors import messages
from rest_framework import viewsets
from questions.models import Question
from results.models import Result, Answer
from .models import Exam
from certificates.models import Certificate
from django.contrib.auth.decorators import login_required
from .serializers import QuestionSerializer, ExamSerializer
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
import json

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
    certificate = Certificate.objects.filter(result=result).first()  # Lấy chứng chỉ nếu có
    if existing_result:
        answers = result.answers.all()
        return render(request, "result_detail_user.html", {
        "result": result,
        "answers": answers,
        "certificate": certificate
    })
    
    # Xử lý JSON options cho mỗi câu hỏi
    for question in questions:
        if question.options:
            try:
                question.option_dict = json.loads(question.options)
            except json.JSONDecodeError:
                question.option_dict = {}
        else:
            question.option_dict = {}
    
    return render(request, "take_exam.html", {
        "exam": exam,
        "questions": questions,
        "duration_minutes": exam.duration,
    })

@login_required
def submit_exam(request, exam_id):
    if request.method != "POST":
        return redirect("exam_list")
    
    exam = get_object_or_404(Exam, id=exam_id)
    questions = exam.questions.all()
    end_time = timezone.now()
    
    # Tạo Result mới
    result = Result.objects.create(
        user=request.user,
        exam=exam,
        start_time=end_time - timezone.timedelta(minutes=exam.duration),
        end_time=end_time
    )
    
    # Biến đếm các câu trả lời đúng
    correct_answers = 0
    
    # Xử lý từng câu hỏi
    for question in questions:
        user_answer = request.POST.get(f"question_{question.id}", "")
        
        # Xử lý các loại câu hỏi khác nhau
        is_correct = False
        
        if question.question_type == "multiple":
            # Với câu hỏi nhiều đáp án, lấy tất cả các giá trị đã chọn
            user_answer_list = request.POST.getlist(f"question_{question.id}", [])
            import json
            try:
                correct_answers_list = json.loads(question.correct_answer)
                # So sánh 2 danh sách, bất kể thứ tự
                is_correct = set(user_answer_list) == set(correct_answers_list)
            except json.JSONDecodeError:
                is_correct = False
                
        elif question.question_type in ["single", "true_false", "fill_blank"]:
            # Với câu hỏi một đáp án, so sánh trực tiếp
            is_correct = user_answer == question.correct_answer
        
        # Tạo Answer mới
        answer = Answer.objects.create(
            result=result,
            question=question,
            user_answer=user_answer if question.question_type != "multiple" else json.dumps(user_answer_list),
            is_correct=is_correct
        )
        
        if is_correct:
            correct_answers += 1
    
    # Tính điểm
    total_questions = questions.count()
    if total_questions > 0:
        score = (correct_answers / total_questions) * 100
        result.score = score
        result.save()
        
        # Kiểm tra điểm để cấp chứng chỉ
        if score >= 70:  # Ngưỡng để đạt
            certificate = Certificate.objects.create(
                result=result,
                issue_date=timezone.now()
            )
    
    # Chuyển hướng đến trang kết quả
    return redirect("result_detail", result_id=result.id)
