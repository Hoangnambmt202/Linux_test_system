from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from exams.models import Exam
from .models import Result, Answer
from certificates.models import Certificate

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
            issue_certificate(request.user, exam)

        return redirect("view_result", result_id=result.id)
    
    return redirect("take_exam", exam_id=exam_id)


@login_required
def view_result(request, result_id):
    result = get_object_or_404(Result, id=result_id, user=request.user)
    answers = result.answers.all()
    return render(request, "result_detail.html", {"result": result, "answers": answers})

    from django.shortcuts import get_object_or_404
from certificates.models import Certificate

@login_required
def view_result_user(request, result_id):
    result = get_object_or_404(Result, id=result_id, user=request.user)  # Chỉ user mới xem được kết quả của mình
    answers = result.answers.all()
    certificate = Certificate.objects.filter(result=result).first()  # Lấy chứng chỉ nếu có
    
    return render(request, "result_detail_user.html", {
        "result": result,
        "answers": answers,
        "certificate": certificate
    })
@login_required
def manage_results(request):
    results = Result.objects.all()
    return render(request, "result_list.html", {"results": results})

def issue_certificate(user, exam):
    Certificate.objects.create(student=user, exam=exam)
