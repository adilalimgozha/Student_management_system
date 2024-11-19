from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Course(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=1024)
    instructor = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'teacher'})

class Enrollment(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'student'})
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

