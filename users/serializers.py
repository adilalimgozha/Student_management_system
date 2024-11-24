from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from students.models import Student

User = get_user_model()

class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'password2', 'email', 'role')

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Passwords do not match."})
        return attrs
    
    def create(self, validated_data):
        role = validated_data.get('role', 'student')  # Если роль не передана, использовать 'student' по умолчанию
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            email=validated_data['email'],
            role=role  # Устанавливаем роль, переданную в запросе
        )
        if role == 'student':
            student = Student.objects.create(
                student=user
            )


        return user
    

class LogoutSerializer(serializers.Serializer):
    refresh_token = serializers.CharField(required=True)
