from rest_framework import serializers
from .models import Attendance
from courses.serializers import CoursesSerializer

from rest_framework import serializers
from .models import Attendance  # Import your Attendance model
from courses.serializers import CoursesSerializer  # Import CoursesSerializer

class AttendanceSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Attendance
        fields = ('student', 'course', 'date', 'status')




