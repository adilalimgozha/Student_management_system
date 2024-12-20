from django.shortcuts import render

# Create your views here.
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from users.permissions import IsTeacher, IsStudent, IsAdmin, IsTeacherOrAdmin
from .serializers import AttendanceSerializer
from rest_framework.exceptions import NotFound
from .models import Attendance
import logging
from notifications.tasks import send_attendance_reminder
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


swagger_jwt_auth = openapi.Parameter(
    'Authorization',  # Parameter name in the header
    in_=openapi.IN_HEADER,
    description='JWT access token',
    type=openapi.TYPE_STRING,
    required=True,
)


logger = logging.getLogger('user_actions')


class AttendanceAPIView(APIView):
    permission_classes = [IsAuthenticated, IsTeacherOrAdmin]

    @swagger_auto_schema(
        manual_parameters=[swagger_jwt_auth],
    )
    def get(self, request, course_id):
        attendance = Attendance.objects.filter(course=course_id)
        if not attendance:
            raise NotFound("No attendance records found for this course")
        serializer = AttendanceSerializer(attendance, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

class AttendanceAPIViewCreate(APIView):

    @swagger_auto_schema(
        manual_parameters=[swagger_jwt_auth],
        request_body=AttendanceSerializer  # Link to the serializer for the body
    )
    def post(self, request):
        serializer = AttendanceSerializer(data=request.data)
        if serializer.is_valid():
            att = serializer.save()

            send_attendance_reminder.delay(att.student.username, att.student.email)

            logger.info(f'Added attendance Student: {att.student.id} in Course: {att.course.id}, Status: {att.status} successfully.')
            
            return Response({"msg": "Attendance marked successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)