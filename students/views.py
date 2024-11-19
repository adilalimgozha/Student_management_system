from django.shortcuts import render

# Create your views here.
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from users.permissions import IsTeacher, IsStudent, IsAdmin, IsTeacherOrAdmin, IsStudentOrAdmin
from .serializers import StudentsSerializer
from rest_framework.exceptions import NotFound
from .models import Student

class StudentsAPIView(APIView):
    permission_classes = [IsAuthenticated, IsTeacherOrAdmin]

    def get(self, request):
        students = Student.objects.all()
        for student in students:
            print(student.student.username) 
        return Response({'students': StudentsSerializer(students, many=True).data}, status=status.HTTP_200_OK)
    
class StudentProfileAPIView(APIView):
    permission_classes = [IsAuthenticated, IsStudentOrAdmin]

    def get(self, request):
        try:
            # Get the authenticated user
            student = Student.objects.get(student=request.user)
        except Student.DoesNotExist:
            raise NotFound("Student profile not found")
        
        serializer = StudentsSerializer(student)
        return Response({'student': serializer.data}, status=status.HTTP_200_OK)
    
    def put(self, request):
        try:
            # Get the authenticated student profile
            student = Student.objects.get(student=request.user)
        except Student.DoesNotExist:
            raise NotFound("Student profile not found")
        
        serializer = StudentsSerializer(student, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

