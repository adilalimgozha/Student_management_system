from rest_framework import serializers
from .models import Grades

class GradesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Grades
        fields = ('student', 'course', 'grade', 'date', 'teacher')

        
