# quiz/views.py
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import random
from .models import Question

def home(request):
    """Render the home page with the Start Quiz button."""
    return render(request, "home.html")

def start_quiz(request):
    """Start the quiz and shuffle questions."""
    questions = Question.objects.all()

    # Check if there are any questions in the database
    if not questions:
        return JsonResponse({"error": "No questions found in the database"}, status=400)

    # Get all question IDs
    question_ids = [q.id for q in questions]
    
    # Shuffle the question IDs
    random.shuffle(question_ids)

    # Select only 5 random questions
    question_ids = random.sample(question_ids, 5)

    # Debugging output: check the question IDs
    print(f"Shuffled question_ids: {question_ids}") 

    # Initialize quiz session data
    request.session['quiz_data'] = {
        'question_ids': question_ids,  # Store the shuffled question IDs
        'current_index': 0,             # Start from the first question
        'answers': []                   # Empty list to store answers
    }
    request.session.save()
    print(f"Quiz Data (question_ids): {request.session['quiz_data']['question_ids']}")
    return render(request, "quiz.html")

def get_question(request):
    """Fetch the current question for the quiz."""
    quiz_data = request.session.get('quiz_data')
    if not quiz_data:
        return JsonResponse({"error": "No active quiz session"}, status=400)

    current_index = quiz_data['current_index']
    if current_index >= len(quiz_data['question_ids']):
        return JsonResponse({"error": "No more questions"}, status=400)

    question_id = quiz_data['question_ids'][current_index]
    question = Question.objects.filter(id=question_id).first()

    if not question:
        return JsonResponse({"error": "Question not found"}, status=404)

    # Return the question data
    return JsonResponse({
        'question': question.question_text,
        'options': question.options,
        'current_index': current_index,  # Send the 0-based index to the frontend
        'total_questions': len(quiz_data['question_ids'])
    })




@csrf_exempt
def submit_answer(request):
    """Submit the answer for the current question."""
    if request.method != "POST":
        return JsonResponse({"error": "Invalid request method"}, status=405)

    quiz_data = request.session.get('quiz_data')
    if not quiz_data:
        return JsonResponse({"error": "No active quiz session"}, status=400)

    # Validate the user's answer
    try:
        user_answer = int(request.POST.get('answer'))  # User answer as an index
    except (TypeError, ValueError):
        return JsonResponse({"error": "Invalid answer format"}, status=400)

    current_index = quiz_data['current_index']

    if current_index >= len(quiz_data['question_ids']):
        return JsonResponse({"error": "All questions have been answered"}, status=400)

    # Fetch the current question
    question_id = quiz_data['question_ids'][current_index]
    question = Question.objects.filter(id=question_id).first()

    if not question:
        return JsonResponse({"error": "Question not found"}, status=404)

    # Ensure the answer is within the valid options range
    if user_answer < 0 or user_answer >= len(question.options):
        return JsonResponse({"error": "Answer is out of range"}, status=400)

    # Check if the answer is correct
    is_correct = user_answer == question.correct_option

    # Store the result for the current question
    quiz_data['answers'].append({
        'question': question.question_text,
        'user_answer': user_answer,
        'correct_answer': question.correct_option,
        'options': question.options,
        'is_correct': is_correct
    })
    
    # Update the current question index for the next question
    quiz_data['current_index'] += 1
    request.session['quiz_data'] = quiz_data
    request.session.save()  # Make sure the session is saved correctly

    # If all questions have been answered, show the summary
    if quiz_data['current_index'] >= len(quiz_data['question_ids']):
        # Clear the quiz session data after the quiz is finished
        del request.session['quiz_data']
        return JsonResponse({
            "message": "Quiz completed",
            "next_action": "summary"  # Indicate that the next action should show the summary
        })

    # Otherwise, return the next question
    return JsonResponse({
        "message": "Answer submitted",
        "is_correct": is_correct,
        "next_action": "next"  # Indicate the next action should get the next question
    })






def get_summary(request):
    """Fetch the summary of the quiz."""
    quiz_data = request.session.get('quiz_data')
    
    if not quiz_data or quiz_data['current_index'] < len(quiz_data['question_ids']):
        return JsonResponse({"error": "Quiz not completed"}, status=400)
    
    # Calculate correct and incorrect answers
    correct_answers = sum(1 for answer in quiz_data['answers'] if answer['is_correct'])
    incorrect_answers = len(quiz_data['answers']) - correct_answers

    summary = {
        "total_questions": len(quiz_data['question_ids']),
        "answered_questions": len(quiz_data['answers']),
        "correct_answers": correct_answers,
        "incorrect_answers": incorrect_answers,
        "answers": quiz_data['answers']
    }

    return JsonResponse(summary)


