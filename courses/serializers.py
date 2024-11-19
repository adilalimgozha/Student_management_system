from rest_framework import serializers
from .models import Course, Enrollment

class CoursesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Course
        fields = ('name', 'description', 'instructor')

    
class EnrollmentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Enrollment
        fields = ('student', 'course')
        
