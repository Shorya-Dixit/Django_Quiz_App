from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),  # Main page with the Start Quiz button
    path('start/', views.start_quiz, name='start_quiz'),
    path('question/', views.get_question, name='get_question'),
    path('submit/', views.submit_answer, name='submit_answer'),
    path('summary/', views.get_summary, name='get_summary'),
]
