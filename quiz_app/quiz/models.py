from djongo import models

class Question(models.Model):
    question_text = models.TextField()
    options = models.JSONField()  # Store options as a list of strings
    correct_option = models.IntegerField()  # Index of the correct option (0-based)
    
    def __str__(self):
        return self.question_text

