from django.shortcuts import render

# Create your views here.
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from users.permissions import IsTeacher, IsStudent, IsAdmin, IsTeacherOrAdmin
from .serializers import CoursesSerializer
from rest_framework.exceptions import NotFound
from .models import Course

class CoursesAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        courses = Course.objects.all()

        serializer = CoursesSerializer(courses, many=True)
        return Response({'courses': serializer.data}, status=status.HTTP_200_OK)