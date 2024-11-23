from django.shortcuts import render

# Create your views here.
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from users.permissions import IsTeacher, IsStudent, IsAdmin, IsTeacherOrAdmin
from .serializers import GradesSerializer
from rest_framework.exceptions import NotFound
from .models import Grades
import logging

logger = logging.getLogger('user_actions')

class GradesAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, course_id):
        grades = Grades.objects.filter(course=course_id)

        serializer = GradesSerializer(grades, many=True)
        return Response({'grades': serializer.data}, status=status.HTTP_200_OK)
    

class GradesAPIViewUpdate(APIView):
    permission_classes = [IsAuthenticated, IsTeacherOrAdmin]
    def put(self, request, course_id, student_id):
        try:
            # Retrieve the grade entry for the specific course and student
            grade = Grades.objects.get(course=course_id, student=student_id)
        except Grades.DoesNotExist:
            raise NotFound("Grade for this course and student not found")
        
        # Update the grade with partial data from the request
        serializer = GradesSerializer(grade, data=request.data, partial=True)
        if serializer.is_valid():
            grades = serializer.save()

            logger.info(f'Updated grade of Student: {grades.student.id} in Course: {grades.course.id}, Grade: {grades.grade} successfully.')

            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GradesAPIViewPost(APIView):
    permission_classes = [IsAuthenticated, IsTeacherOrAdmin]
    def post(self, request):
        serializer = GradesSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"msg": "Grade added successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)