from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from exams.models import Exam
from .models import Result, Answer
from certificates.models import Certificate
from certificates.views import issue_certificate
import json


@login_required    
def submit_exam(request, exam_id):
    exam = get_object_or_404(Exam, id=exam_id)
    questions = exam.questions.all()
    
    if request.method == "POST":
        correct_count = 0
        total_questions = questions.count()

        # Tạo bản ghi kết quả
        result = Result.objects.create(
            user=request.user, exam=exam, score=0, total_questions=total_questions, correct_answers=0
        )
       

        for question in questions:
            selected_option = request.POST.get(f"question_{question.id}")
            is_correct = question.correct_answer == selected_option

            if is_correct:
                correct_count += 1

            # Lưu câu trả lời
            Answer.objects.create(
                result=result, question=question, selected_option=selected_option, is_correct=is_correct
            )

        
        # Cập nhật điểm số
        result.correct_answers = correct_count
        result.score = (correct_count / total_questions) * 100
        result.save()
         # Sau khi lưu kết quả
        if result.score >= 80:  # Điều kiện cấp chứng chỉ
            issue_certificate(request.user, result.id)

        return redirect("view_result_user", result_id=result.id)
    
    return redirect("take_exam", exam_id=exam_id)



@login_required
def view_result_user(request, result_id):
    result = get_object_or_404(Result, id=result_id, user=request.user)  # Chỉ user mới xem được kết quả của mình
    answers = result.answers.all()
    certificate = Certificate.objects.filter(result=result).first()  # Lấy chứng chỉ nếu có
    
    # Xử lý JSON trong câu trả lời
    for answer in answers:
        # Xử lý trường hợp multiple choice
        if answer.question.question_type == 'multiple':
            try:
                # Parse đáp án người dùng chọn
                if answer.user_answer and answer.user_answer.strip():
                    answer.user_answer_list = json.loads(answer.user_answer)
                else:
                    answer.user_answer_list = []
                    
                # Parse đáp án đúng
                if answer.question.correct_answer and answer.question.correct_answer.strip():
                    answer.correct_answers_list = json.loads(answer.question.correct_answer)
                else:
                    answer.correct_answers_list = []
            except json.JSONDecodeError:
                answer.user_answer_list = []
                answer.correct_answers_list = []
        else:
            # Đối với các loại câu hỏi khác, giữ nguyên
            answer.user_answer_list = []
            answer.correct_answers_list = []
            
        # Tính thời gian làm bài (phút)
        result.duration_minutes = (result.end_time - result.start_time).total_seconds() // 60
    
    return render(request, "result_detail_user.html", {
        "result": result,
        "answers": answers,
        "certificate": certificate
    })
@login_required
def manage_results(request):
    results = Result.objects.all()
    return render(request, "result_list.html", {"results": results})
