from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from exams.models import Exam
from .models import Result, Answer
from certificates.models import Certificate
from certificates.views import issue_certificate
from django.utils import timezone
from django.contrib import messages

import json
from django.utils import timezone

@login_required    
def submit_exam(request, exam_id):
    exam = get_object_or_404(Exam, id=exam_id)
    questions = exam.questions.all()

    if request.method == "POST":
        correct_count = 0
        total_questions = questions.count()
        start_time = timezone.now() - timezone.timedelta(minutes=exam.duration)
        end_time = timezone.now()

        # Tạo bản ghi kết quả
        result = Result.objects.create(
            user=request.user,
            exam=exam,
            score=0,
            total_questions=total_questions,
            correct_answers=0,
            start_time=start_time,
            end_time=end_time
        )

        for question in questions:
            selected_option = request.POST.getlist(f"question_{question.id}") if question.question_type == 'multiple' else request.POST.get(f"question_{question.id}")
            is_correct = False

            if question.question_type == 'multiple':
                correct_keys = [opt.key for opt in question.correct_answers.all()]
                is_correct = set(selected_option) == set(correct_keys)

                Answer.objects.create(
                    result=result,
                    question=question,
                    selected_option=json.dumps(selected_option),
                    is_correct=is_correct
                )

            elif question.question_type == 'single':
                correct_option = question.correct_answers.first()
                is_correct = correct_option and selected_option == correct_option.key

                Answer.objects.create(
                    result=result,
                    question=question,
                    selected_option=selected_option,
                    is_correct=is_correct
                )

            elif question.question_type in ['true_false', 'fill_blank']:
                correct_text = question.correct_answer_text.strip().lower() if question.correct_answer_text else ""
                is_correct = selected_option.strip().lower() == correct_text

                Answer.objects.create(
                    result=result,
                    question=question,
                    selected_option=selected_option,
                    is_correct=is_correct
                )

            if is_correct:
                correct_count += 1

        # Cập nhật điểm số
        result.correct_answers = correct_count
        result.score = (correct_count / total_questions) * 100
        result.save()

        # Cấp chứng chỉ nếu đạt
        if result.score >= 80:
            user = request.user
             # Kiểm tra nếu tên không đầy đủ
            if not user.first_name or not user.last_name:
                messages.warning(request, "Tên không được để trống. Vui lòng cập nhật thông tin cá nhân.")
                return redirect('profile')
            
            issue_certificate(request.user, result.id)

        return redirect("view_result_user", result_id=result.id )

    return redirect("take_exam", exam_id=exam_id)


@login_required
def view_result_user(request, result_id):
    result = get_object_or_404(Result, id=result_id, user=request.user)
    answers = result.answers.select_related("question").all()
    certificate = Certificate.objects.filter(result=result).first()

    for answer in answers:
        q = answer.question
        answer.user_answer_list = []
        answer.correct_answers_list = []

        if q.question_type == 'multiple':
            try:
                answer.user_answer_list = json.loads(answer.selected_option) if answer.selected_option else []
            except json.JSONDecodeError:
                answer.user_answer_list = []

            answer.correct_answers_list = [opt.key for opt in q.correct_answers.all()]

        elif q.question_type == 'single':
            answer.user_answer_list = [answer.selected_option] if answer.selected_option else []
            correct_option = q.correct_answers.first()
            answer.correct_answers_list = [correct_option.key] if correct_option else []

        elif q.question_type in ['true_false', 'fill_blank']:
            answer.user_answer_list = [answer.selected_option] if answer.selected_option else []
            answer.correct_answers_list = [q.correct_answer_text] if q.correct_answer_text else []

        # Thêm option hiển thị
        if q.question_type in ['single', 'multiple']:
            answer.options_dict = {opt.key: opt.text for opt in q.options.all()}

    # Tính thời gian làm bài
    if result.end_time and result.start_time:
        result.duration_minutes = (result.end_time - result.start_time).total_seconds() // 60
    else:
        result.duration_minutes = 0  # Hoặc một giá trị mặc định khác

    return render(request, "result_detail_user.html", {
        "result": result,
        "answers": answers,
        "certificate": certificate
    })

@login_required
def manage_results(request):
    results = Result.objects.all()
    return render(request, "result_list.html", {"results": results})
