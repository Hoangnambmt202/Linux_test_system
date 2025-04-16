from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from questions.models import Question
import os
import json


@login_required
def manage_questions(request):
    query = request.GET.get('q', '')  
    if query:
        questions = Question.objects.filter(text__icontains=query)
    else:
        questions = Question.objects.all()

    return render(request, "manage_questions.html", {"questions": questions, "query": query})

@login_required
def add_question(request):
    if request.method == 'POST':
        try:
            # Get basic question data
            text = request.POST.get('text')
            content_type = request.POST.get('content_type')
            question_type = request.POST.get('question_type')
            difficulty = request.POST.get('difficulty')

            # Create new question instance
            question = Question(
                text=text,
                content_type=content_type,
                question_type=question_type,
                difficulty=difficulty
            )

            # Handle media files based on content type
            if content_type == 'image' and request.FILES.get('image'):
                question.image = request.FILES['image']
            elif content_type == 'video' and request.FILES.get('video'):
                question.video = request.FILES['video']

            # Handle answers based on question type
            if question_type in ['single', 'multiple']:
                # Prepare options dictionary
                options = {
                    'A': request.POST.get('option_a'),
                    'B': request.POST.get('option_b'),
                    'C': request.POST.get('option_c'),
                    'D': request.POST.get('option_d')
                }
                question.options = json.dumps(options)
                
                if question_type == 'single':
                    question.correct_answer = request.POST.get('correct_answer')
                else:
                    correct_answers = request.POST.getlist('correct_answers')
                    question.correct_answer = json.dumps(correct_answers)

            elif question_type == 'true_false':
                # True/False question
                question.options = None
                question.correct_answer = request.POST.get('correct_answer')

            elif question_type == 'fill_blank':
                # Fill in the blank question
                question.options = None
                question.correct_answer = request.POST.get('correct_answer')

            # Save the question
            question.save()
            messages.success(request, 'Câu hỏi đã được thêm thành công!')
            return redirect('manage_questions')

        except Exception as e:
            messages.error(request, f'Lỗi khi thêm câu hỏi: {str(e)}')
            return redirect('add_question')

    return render(request, 'add_question.html')


@login_required
def edit_question(request, question_id):
    question = get_object_or_404(Question, id=question_id)
    
    if request.method == 'POST':
        try:
            # Update basic question data
            question.text = request.POST.get('text')
            question.content_type = request.POST.get('content_type')
            question.question_type = request.POST.get('question_type')
            question.difficulty = request.POST.get('difficulty')

            # Handle media files
            if question.content_type == 'image':
                if request.FILES.get('image'):
                    if question.image:
                        if os.path.exists(question.image.path):
                            os.remove(question.image.path)
                    question.image = request.FILES['image']
                    question.video = None
            elif question.content_type == 'video':
                if request.FILES.get('video'):
                    if question.video:
                        if os.path.exists(question.video.path):
                            os.remove(question.video.path)
                    question.video = request.FILES['video']
                    question.image = None
            else:
                # Text only - clear both image and video
                if question.image:
                    if os.path.exists(question.image.path):
                        os.remove(question.image.path)
                    question.image = None
                if question.video:
                    if os.path.exists(question.video.path):
                        os.remove(question.video.path)
                    question.video = None

            # Handle answers based on question type
            if question.question_type in ['single', 'multiple']:
                options = {
                    'A': request.POST.get('option_a'),
                    'B': request.POST.get('option_b'),
                    'C': request.POST.get('option_c'),
                    'D': request.POST.get('option_d')
                }
                question.options = json.dumps(options)
                
                if question.question_type == 'single':
                    question.correct_answer = request.POST.get('correct_answer')
                else:
                    correct_answers = request.POST.getlist('correct_answers')
                    question.correct_answer = json.dumps(correct_answers)
            
            elif question.question_type == 'true_false':
                question.options = None
                question.correct_answer = request.POST.get('correct_answer')
            
            elif question.question_type == 'fill_blank':
                question.options = None
                question.correct_answer = request.POST.get('correct_answer')

            question.save()
            messages.success(request, 'Câu hỏi đã được cập nhật thành công!')
            return redirect('manage_questions')

        except Exception as e:
            messages.error(request, f'Lỗi khi cập nhật câu hỏi: {str(e)}')
            return redirect('edit_question', question_id=question_id)

    # Prepare data for template
    context = {
        'question': question,
    }
    
    # Add options to context if they exist
    if question.options:
        try:
            context['options'] = json.loads(question.options)
        except json.JSONDecodeError:
            context['options'] = None
            
    # Add correct answers to context
    if question.question_type == 'multiple':
        try:
            context['correct_answers'] = json.loads(question.correct_answer)
        except json.JSONDecodeError:
            context['correct_answers'] = []
    else:
        context['correct_answers'] = question.correct_answer
        
    return render(request, 'edit_question.html', context)


@login_required
def delete_question(request, question_id):
    question = get_object_or_404(Question, id=question_id)
    
    try:
        # Delete associated media files
        if question.image:
            if os.path.exists(question.image.path):
                os.remove(question.image.path)
        if question.video:
            if os.path.exists(question.video.path):
                os.remove(question.video.path)
        
        # Delete the question
        question.delete()
        messages.success(request, 'Câu hỏi đã được xóa thành công!')
    except Exception as e:
        messages.error(request, f'Lỗi khi xóa câu hỏi: {str(e)}')
    
    return redirect('manage_questions')
