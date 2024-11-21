from rest_framework import serializers
from .models import Course, Enrollment
from django.contrib.auth import get_user_model
from students.serializers import StudentsSerializer

User = get_user_model()

class CoursesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ('name', 'description', 'instructor')

    
class EnrollmentSerializer(serializers.ModelSerializer):
    course = CoursesSerializer(many=True)  # Вложенные курсы
    student = StudentsSerializer(many=True)  # Вложенные студенты

    class Meta:
        model = Enrollment
        fields = ('student', 'course')
