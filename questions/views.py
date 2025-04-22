from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.db import transaction
import os
from .models import Question, Option, Topic
from .forms import TopicForm


@login_required
def add_question(request):
        topics = Topic.objects.all()
        if request.method == 'POST':
            try:
                with transaction.atomic():
                    question = Question(
                        text=request.POST.get('text'),
                        content_type=request.POST.get('content_type'),
                        question_type=request.POST.get('question_type'),
                        difficulty=request.POST.get('difficulty'),
                    )
                    # ✅ Gán chủ đề nếu có
                    topic_id = request.POST.get('topic_id')
                    if topic_id:
                        topic = Topic.objects.get(id=topic_id)
                        question.topic = topic
                    # Xử lý media
                    if question.content_type == 'image':
                        question.image = request.FILES.get('image')
                    elif question.content_type == 'video':
                        question.video = request.FILES.get('video')

                    question.save()

                    # Xử lý các loại câu hỏi
                    if question.question_type in ['single', 'multiple']:
                        options_data = {
                            'A': request.POST.get('option_a'),
                            'B': request.POST.get('option_b'),
                            'C': request.POST.get('option_c'),
                            'D': request.POST.get('option_d'),
                        }

                        if not all(options_data.values()):
                            raise ValidationError('Tất cả các đáp án A, B, C, D là bắt buộc.')

                        for key, text in options_data.items():
                            Option.objects.create(question=question, key=key, text=text)

                        if question.question_type == 'single':
                            correct_key = request.POST.get('correct_answer_single')
                            if not correct_key or correct_key not in ['A', 'B', 'C', 'D']:
                                raise ValidationError("Đáp án đúng không hợp lệ.")
                            correct_option = Option.objects.get(question=question, key=correct_key)
                            question.correct_answers.set([correct_option])

                        else:  # multiple
                            correct_keys = request.POST.getlist('correct_answers')
                            if not correct_keys:
                                raise ValidationError("Phải chọn ít nhất một đáp án đúng.")
                            correct_options = Option.objects.filter(question=question, key__in=correct_keys)
                            question.correct_answers.set(correct_options)

                    elif question.question_type == 'true_false':
                        correct_answer = request.POST.get('correct_answer_tf')
                        if correct_answer not in ['true', 'false']:
                            raise ValidationError('Câu hỏi đúng/sai phải chọn "Đúng" hoặc "Sai".')
                        question.correct_answer_text = correct_answer
                        question.save()

                    elif question.question_type == 'fill_blank':
                        correct_answer = request.POST.get('correct_answer_text')
                        if not correct_answer:
                            raise ValidationError('Phải nhập đáp án đúng cho câu hỏi điền khuyết.')
                        question.correct_answer_text = correct_answer
                        question.save()

                    messages.success(request, 'Thêm câu hỏi thành công!')
                    return redirect('manage_questions')

            except ValidationError as ve:
                messages.error(request, f'Lỗi: {ve}')
            except Exception as e:
                messages.error(request, f'Lỗi hệ thống: {e}')

        return render(request, 'add_question.html', {'topics': topics})

@login_required
def edit_question(request, question_id):
    question = get_object_or_404(Question, id=question_id)  
    topics = Topic.objects.all()  
    if request.method == 'POST':
        try:
            with transaction.atomic():
                # Update basic fields
                question.text = request.POST.get('text')
                question.content_type = request.POST.get('content_type')
                question.question_type = request.POST.get('question_type')
                question.difficulty = request.POST.get('difficulty')

                # Handle media content
                if question.content_type == 'image':
                    if request.FILES.get('image'):
                        if question.image:
                            question.image.delete()
                        question.image = request.FILES['image']
                        question.video = None
                elif question.content_type == 'video':
                    if request.FILES.get('video'):
                        if question.video:
                            question.video.delete()
                        question.video = request.FILES['video']
                        question.image = None
                else:
                    question.image = None
                    question.video = None

                question.save()
                # ✅ Gán chủ đề nếu có
                topic_id = request.POST.get('topic_id')
                if topic_id:
                    question.topic = Topic.objects.get(id=topic_id)
                # Handle different question types
                if question.question_type in ['single', 'multiple']:
                    # Delete existing options
                    question.options.all().delete()
                    
                    # Create new options
                    options_data = {
                        'A': request.POST.get('option_a'),
                        'B': request.POST.get('option_b'),
                        'C': request.POST.get('option_c'),
                        'D': request.POST.get('option_d'),
                    }

                    if not all(options_data.values()):
                        raise ValidationError('Tất cả các đáp án A, B, C, D là bắt buộc.')

                    for key, text in options_data.items():
                        Option.objects.create(question=question, key=key, text=text)

                    # Handle correct answers
                    if question.question_type == 'single':
                        correct_key = request.POST.get('correct_answer_single')
                        if not correct_key or correct_key not in ['A', 'B', 'C', 'D']:
                            raise ValidationError("Đáp án đúng không hợp lệ.")
                        correct_option = Option.objects.get(question=question, key=correct_key)
                        question.correct_answers.set([correct_option])
                    else:  # multiple
                        correct_keys = request.POST.getlist('correct_answers')
                        if not correct_keys:
                            raise ValidationError("Phải chọn ít nhất một đáp án đúng.")
                        correct_options = Option.objects.filter(question=question, key__in=correct_keys)
                        question.correct_answers.set(correct_options)

                elif question.question_type == 'true_false':
                    correct_answer = request.POST.get('correct_answer_tf')
                    if correct_answer not in ['true', 'false']:
                        raise ValidationError('Câu hỏi đúng/sai phải chọn "Đúng" hoặc "Sai".')
                    question.correct_answer_text = correct_answer
                    question.save()

                elif question.question_type == 'fill_blank':
                    correct_answer = request.POST.get('correct_answer_text')
                    if not correct_answer:
                        raise ValidationError('Phải nhập đáp án đúng cho câu hỏi điền khuyết.')
                    question.correct_answer_text = correct_answer
                    question.save()

                messages.success(request, 'Cập nhật câu hỏi thành công!')
                return redirect('manage_questions')

        except ValidationError as ve:
            messages.error(request, f'Lỗi: {ve}')
        except Exception as e:
            messages.error(request, f'Lỗi hệ thống: {e}')
            
    options = question.options.all().order_by('key')
    return render(request, 'edit_question.html', {'question': question, 'options': options,'topics': topics })
      
@login_required
def manage_questions(request):
        query = request.GET.get('q', '')  
        topic_id = request.GET.get('topic', '')
        topics = Topic.objects.all()
        questions = Question.objects.all()
        if query:
            questions = Question.objects.filter(text__icontains=query)
        if topic_id:
            questions = questions.filter(topic__id=topic_id)
        
           

        # Generate diagnostic report for questions
        if request.GET.get('debug', '') == '1':
            print("\n===== QUESTIONS DIAGNOSTIC REPORT =====")
            print(f"Total questions: {questions.count()}")
            
            # Group questions by type
            question_types = {}
            for q_type, _ in Question.QUESTION_TYPES:
                count = questions.filter(question_type=q_type).count()
                question_types[q_type] = count
            
            print("\nQuestion counts by type:")
            for q_type, count in question_types.items():
                print(f"  {q_type}: {count}")
            
            # Check for potential data issues
            print("\nPotential data issues:")
            
            # Single choice questions without exactly one correct answer
            single_issues = Question.objects.filter(question_type='single').exclude(correct_answers=None)
            for q in single_issues:
                count = q.correct_answers.count()
                if count != 1:
                    print(f"  ID {q.id}: Single choice question with {count} correct answers")
            
            # Multiple choice questions without any correct answers
            multiple_issues = Question.objects.filter(question_type='multiple').exclude(correct_answers=None)
            for q in multiple_issues:
                count = q.correct_answers.count()
                if count == 0:
                    print(f"  ID {q.id}: Multiple choice question with no correct answers")
            
            # True/False questions with invalid correct_answer_text
            tf_issues = Question.objects.filter(question_type='true_false')
            for q in tf_issues:
                if q.correct_answer_text not in ['true', 'false']:
                    print(f"  ID {q.id}: True/False question with invalid answer: '{q.correct_answer_text}'")
            
            # Fill in the blank questions without correct_answer_text
            fb_issues = Question.objects.filter(question_type='fill_blank', correct_answer_text='')
            for q in fb_issues:
                print(f"  ID {q.id}: Fill in the blank question without an answer")
            
            # Questions with options not matching their type
            for q in Question.objects.all():
                if q.question_type in ['single', 'multiple']:
                    if q.options.count() != 4:
                        print(f"  ID {q.id}: {q.question_type} choice question with {q.options.count()} options (should be 4)")
                elif q.question_type in ['true_false', 'fill_blank']:
                    if q.options.exists():
                        print(f"  ID {q.id}: {q.question_type} question with options (should have none)")
            
            print("=======================================\n")

        return render(request, "manage_questions.html", {"questions": questions, "query": query,"topics": topics,
        "selected_topic": int(topic_id) if topic_id else None,})

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

@login_required
def question_detail(request, question_id):
    question = get_object_or_404(Question, id=question_id)

    options = list(question.options.all().order_by('key'))
    correct_answers = list(question.correct_answers.all())
    topic = question.topic.name if question.topic else "Chưa có chủ đề"

    print("\n--- DEBUG QUESTION ---")
    print(f"ID: {question.id}, Type: {question.question_type}")
    print(f"Correct Answer Text: {question.correct_answer_text}")
    print(f"Options: {[f'{o.key}: {o.text}' for o in options]}")
    print(f"Correct Answers: {[a.key for a in correct_answers]}")

    context = {
        'question': question,
        'options': options,
        'correct_answers': correct_answers,
        'topic': topic,
    }
    return render(request, 'question_detail.html', context)

def manage_topics(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        if name:
            Topic.objects.create(name=name)
            messages.success(request, 'Đã thêm chủ đề thành công.')
            return redirect('manage_topics')

    topics = Topic.objects.all()
    return render(request, 'manage_topics.html', {'topics': topics})

def edit_topic(request, topic_id):
    topic = get_object_or_404(Topic, id=topic_id)
    if request.method == 'POST':
        topic.name = request.POST.get('name')
        topic.save()
        messages.success(request, 'Đã cập nhật chủ đề.')
        return redirect('manage_topics')
    return render(request, 'edit_topic.html', {'topic': topic})

def delete_topic(request, topic_id):
    topic = get_object_or_404(Topic, id=topic_id)
    topic.delete()
    messages.success(request, 'Đã xóa chủ đề.')
    return redirect('manage_topics')
