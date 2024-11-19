from django.shortcuts import render

# Create your views here.
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from users.permissions import IsTeacher, IsStudent, IsAdmin, IsTeacherOrAdmin
from .serializers import CoursesSerializer, EnrollmentSerializer
from rest_framework.exceptions import NotFound
from .models import Course, Enrollment

class CoursesAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        courses = Course.objects.all()

        serializer = CoursesSerializer(courses, many=True)
        return Response({'courses': serializer.data}, status=status.HTTP_200_OK)
    

class CoursesAPIViewEdit(APIView):
    permission_classes = [IsAuthenticated, IsTeacherOrAdmin]
    
    def put(self, request, course_id):
        try:
            # Get the authenticated student profile
            course = Course.objects.get(id=course_id)
        except Course.DoesNotExist:
            raise NotFound("Course not found")
        
        serializer = CoursesSerializer(course, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def post(self, request):
        serializer = CoursesSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"msg": "Course added successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class CoursesAPIViewEnroll(APIView):
    permission_classes = [IsAuthenticated, IsTeacherOrAdmin]

    def get(self, request):
        enrollments = Enrollment.objects.all()

        serializer = EnrollmentSerializer(enrollments, many=True)
        return Response({'enrollments': serializer.data}, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = EnrollmentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"msg": "Student enrolled to the course successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)