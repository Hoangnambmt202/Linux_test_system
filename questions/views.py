from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from questions.models import Question

def manage_questions(request):
    query = request.GET.get('q', '')  
    if query:
        questions = Question.objects.filter(text__icontains=query)
    else:
        questions = Question.objects.all()

    return render(request, "manage_questions.html", {"questions": questions, "query": query})

def add_question(request):
    if request.method == "POST":
        text = request.POST.get("text")
        option_a = request.POST.get("option_a")
        option_b = request.POST.get("option_b")
        option_c = request.POST.get("option_c")
        option_d = request.POST.get("option_d")
        correct_answer = request.POST.get("correct_answer")
        difficulty = request.POST.get("difficulty")

        Question.objects.create(
            text=text, option_a=option_a, option_b=option_b, option_c=option_c,
            option_d=option_d, correct_answer=correct_answer, difficulty=difficulty
        )
        messages.success(request, "Thêm câu hỏi thành công!")
        return redirect("manage_questions")

    return render(request, "add_question.html")

def edit_question(request, question_id):
    question = get_object_or_404(Question, id=question_id)

    if request.method == "POST":
        question.text = request.POST.get("text")
        question.option_a = request.POST.get("option_a")
        question.option_b = request.POST.get("option_b")
        question.option_c = request.POST.get("option_c")
        question.option_d = request.POST.get("option_d")
        question.correct_answer = request.POST.get("correct_answer")
        question.difficulty = request.POST.get("difficulty")
        question.save()

        messages.success(request, "Cập nhật câu hỏi thành công!")
        return redirect("manage_questions")

    return render(request, "edit_question.html", {"question": question})

def delete_question(request, question_id):
    question = get_object_or_404(Question, id=question_id)
    question.delete()
    messages.success(request, "Xóa câu hỏi thành công!")
    return redirect("manage_questions")
