from rest_framework import serializers
from .models import Course, Enrollment
from students.models import Student
from django.contrib.auth import get_user_model
from students.serializers import StudentsSerializer

User = get_user_model()

class CoursesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ('name', 'description', 'instructor')

    
class EnrollmentSerializer(serializers.ModelSerializer):
    # Вложенные сериализаторы для отображения данных
    student = StudentsSerializer(read_only=True, many=True)
    course = CoursesSerializer(read_only=True, many=True)

    # Поля для записи ID студентов и курсов
    student_id = serializers.PrimaryKeyRelatedField(queryset=Student.objects.all(), write_only=True, many=True)
    course_id = serializers.PrimaryKeyRelatedField(queryset=Course.objects.all(), write_only=True, many=True)

    class Meta:
        model = Enrollment
        fields = ('student', 'course', 'student_id', 'course_id')

    def create(self, validated_data):
        # Извлекаем ID студентов и курсов из данных
        student_ids = validated_data.pop('student_id')
        course_ids = validated_data.pop('course_id')

        # Создаем объект Enrollment
        enrollment = Enrollment.objects.create(**validated_data)

        # Устанавливаем связи для студентов и курсов
        enrollment.student.set(student_ids)  # Множественное присваивание через set
        enrollment.course.set(course_ids)    # Множественное присваивание через set

        return enrollment

