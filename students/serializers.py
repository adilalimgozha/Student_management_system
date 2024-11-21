from rest_framework import serializers
from students.models import Student

class StudentsSerializer(serializers.ModelSerializer):

    username = serializers.CharField(source='student.username')  # Извлекаем имя пользователя через связь с CustomUser
    email = serializers.EmailField(source='student.email')  # Извлекаем email через связь с CustomUser
    first_name = serializers.CharField(source='student.first_name')  # Извлекаем имя через связь с CustomUser
    last_name = serializers.CharField(source='student.last_name')  # Извлекаем фамилию через связь с CustomUser

    

    class Meta:
        model = Student  # Используем модель Student
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

        
