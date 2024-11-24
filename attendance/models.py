from django.db import models
from django.contrib.auth import get_user_model
from courses.models import Course


User = get_user_model()

class Attendance(models.Model):#student берется из User БД в идеале надо со Student БД
    student = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'student'},  related_name='attendance_student')
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)  # Sets the date when the object is first created
    STATUS_CHOICES = [
        ('attend', 'Attend'),
        ('absent', 'Absent'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
