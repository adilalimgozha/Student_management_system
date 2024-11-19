from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Student(models.Model):
    student = models.OneToOneField(User, on_delete=models.CASCADE, limit_choices_to={'role': 'student'},  related_name='student_student')
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    description = models.CharField(max_length=1024)

    def __str__(self):
        return self.student.username
