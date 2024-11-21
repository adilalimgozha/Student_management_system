from django.db import models
from django.contrib.auth import get_user_model
from students.models import Student

User = get_user_model()

class Course(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=1024)
    instructor = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'teacher'})

class Enrollment(models.Model):

    student = models.ManyToManyField(Student, related_name='enrollments')
    course = models.ManyToManyField(Course)


