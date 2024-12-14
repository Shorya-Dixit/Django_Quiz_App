from django.core.management.base import BaseCommand
from quiz.models import Question

class Command(BaseCommand):
    help = "Seed the database with sample quiz questions"

    def handle(self, *args, **kwargs):
        questions = [
            {
                "question_text": "What is the capital of France?",
                "options": ["Paris", "London", "Rome", "Berlin"],
                "correct_option": 0,
            },
            {
                "question_text": "Which planet is known as the Red Planet?",
                "options": ["Earth", "Mars", "Venus", "Jupiter"],
                "correct_option": 1,
            },
            {
                "question_text": "Who wrote 'Hamlet'?",
                "options": ["Charles Dickens", "J.K. Rowling", "William Shakespeare", "Mark Twain"],
                "correct_option": 2,
            },
        ]

        for question in questions:
            Question.objects.create(**question)

        self.stdout.write("Database seeded successfully!")
