from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from questions.models import Question
from django.core.files.storage import FileSystemStorage


def manage_questions(request):
    query = request.GET.get('q', '')  
    if query:
        questions = Question.objects.filter(text__icontains=query)
    else:
        questions = Question.objects.all()

    return render(request, "manage_questions.html", {"questions": questions, "query": query})

def add_question(request):
    if request.method == "POST":
        question_type = request.POST.get("question_type")
        text = request.POST.get("text")  # Cho phép nhập văn bản mô tả
        media = request.FILES.get("media") if question_type in ["image", "video"] else None
        option_a = request.POST.get("option_a")
        option_b = request.POST.get("option_b")
        option_c = request.POST.get("option_c")
        option_d = request.POST.get("option_d")
        correct_answer = request.POST.get("correct_answer")
        difficulty = request.POST.get("difficulty")

        if media:
            fs = FileSystemStorage()
            media_name = fs.save(media.name, media)
            media_url = fs.url(media_name)
        else:
            media_url = None

        Question.objects.create(
            question_type=question_type, text=text, media=media_url,
            option_a=option_a, option_b=option_b, option_c=option_c,
            option_d=option_d, correct_answer=correct_answer, difficulty=difficulty
        )
        
        messages.success(request, "Thêm câu hỏi thành công!")
        return redirect("manage_questions")

    return render(request, "add_question.html")


def edit_question(request, question_id):
    question = get_object_or_404(Question, id=question_id)

    if request.method == "POST":
        question_type = request.POST.get("question_type")
        text = request.POST.get("text") if question_type == "text" else None
        media = request.FILES.get("media") if question_type in ["image", "video"] else None
        option_a = request.POST.get("option_a")
        option_b = request.POST.get("option_b")
        option_c = request.POST.get("option_c")
        option_d = request.POST.get("option_d")
        correct_answer = request.POST.get("correct_answer")
        difficulty = request.POST.get("difficulty")

        # Xóa media cũ nếu người dùng upload file mới
        if media:
            if question.media:
                question.media.delete()
            fs = FileSystemStorage()
            media_name = fs.save(media.name, media)
            question.media = media_name

        # Cập nhật thông tin câu hỏi
        question.question_type = question_type
        question.text = text
        question.option_a = option_a
        question.option_b = option_b
        question.option_c = option_c
        question.option_d = option_d
        question.correct_answer = correct_answer
        question.difficulty = difficulty
        question.save()

        messages.success(request, "Cập nhật câu hỏi thành công!")
        return redirect("manage_questions")

    return render(request, "edit_question.html", {"question": question})


def delete_question(request, question_id):
    question = get_object_or_404(Question, id=question_id)
    question.delete()
    messages.success(request, "Xóa câu hỏi thành công!")
    return redirect("manage_questions")
