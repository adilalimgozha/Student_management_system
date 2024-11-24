from django.shortcuts import render

# Create your views here.
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from .serializers import UserRegisterSerializer
from rest_framework_simplejwt.tokens import RefreshToken
import logging
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth import get_user_model
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


User = get_user_model()


logger = logging.getLogger('user_actions')

class UserRegisterView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        request_body=UserRegisterSerializer  # Link to the serializer for the body
    )

    def post(self, request):
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()

            logger.info(f'User registered: {user.username} (ID: {user.id})')
            return Response({"msg": "User registered successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CustomTokenObtainPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):

        response = super().post(request, *args, **kwargs)

        # If login was successful, log the event
        if response.status_code == 200:
            username = request.data.get('username')
            logger.info(f'Attempting to get user: {username}') 
             # Получаем объект пользователя по username
            try:
                user = User.objects.get(username=username)
                logger.info(f'User {user.username} (ID: {user.id}) logged in successfully.')
            except User.DoesNotExist:
                logger.warning(f'Login attempt with invalid username: {username}')

        return response

    
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            logger.info(f'User logged out: {request.user.username} (ID: {request.user.id})')

            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            logger.error(f'Logout failed: {str(e)}')
            return Response(status=status.HTTP_400_BAD_REQUEST)
