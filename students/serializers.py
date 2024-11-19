from rest_framework import serializers
from students.models import Student

class StudentsSerializer(serializers.ModelSerializer):

    username = serializers.CharField(source='student.username')  # Access username from related user
    email = serializers.EmailField(source='student.email')  # Access email from related user
    first_name = serializers.CharField(source='student.first_name')  # Access first name from related user
    last_name = serializers.CharField(source='student.last_name')

    class Meta:
        model = Student
        fields = ('username', 'email', 'first_name', 'last_name', 'description')
