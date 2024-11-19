from rest_framework import serializers
from .models import Course

class CoursesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Course
        fields = ('name', 'description', 'instructor')

    

        
