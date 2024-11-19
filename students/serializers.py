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

    def update(self, instance, validated_data):
        # Извлекаем данные для связанных объектов
        student_data = validated_data.pop('student', {})

        # Обновляем объект Student
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # Обновляем связанные данные пользователя
        if student_data:
            user_instance = instance.student
            for attr, value in student_data.items():
                setattr(user_instance, attr, value)
            user_instance.save()

        return instance

        
