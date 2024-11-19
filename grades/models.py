from django.db import models
from django.contrib.auth import get_user_model
from courses.models import Course

User = get_user_model()

class Grades(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'student'},  related_name='grades_student')
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    grade = models.DecimalField(max_digits=5, decimal_places=2)
    date = models.DateField(auto_now_add=True)  # Sets the date when the object is first created
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'teacher'}, related_name='grades_teacher')
