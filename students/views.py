from django.shortcuts import render

# Create your views here.
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from users.permissions import IsTeacher
from .serializers import StudentsSerializer
from .models import Student

class StudentsAPIView(APIView):
    permission_classes = [IsAuthenticated, IsTeacher]

    def get(self, request):
        students = Student.objects.all()
        for student in students:
            print(student.student.username) 
        return Response({'students': StudentsSerializer(students, many=True).data}, status=status.HTTP_200_OK)