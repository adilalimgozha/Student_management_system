from django.shortcuts import render

# Create your views here.
from rest_framework import status
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from users.permissions import IsTeacher, IsStudent, IsAdmin, IsTeacherOrAdmin, IsStudentOrAdmin
from .serializers import StudentsSerializer
from rest_framework.exceptions import NotFound
from .models import Student
import django_filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter

class StudentsAPIListPagination(PageNumberPagination):
    page_size = 2
    page_query_param = 'page_size'
    max_page_size = 100

class StudentFilter(django_filters.FilterSet):
    username = django_filters.CharFilter(lookup_expr='icontains', field_name='student__username')
    email = django_filters.CharFilter(lookup_expr='icontains', field_name='student__email')
    first_name = django_filters.CharFilter(lookup_expr='icontains', field_name='student__first_name')
    last_name = django_filters.CharFilter(lookup_expr='icontains', field_name='student__last_name')

    class Meta:
        model = Student
        fields = ['username', 'email', 'first_name', 'last_name'] 

class StudentsAPIView(APIView):
    permission_classes = [IsAuthenticated, IsTeacherOrAdmin]
    pagination_class = StudentsAPIListPagination

    filter_backends = (DjangoFilterBackend,)
    filterset_class = StudentFilter 

    def get(self, request):
        students = Student.objects.all()

        filterset = self.filterset_class(request.GET, queryset=students)
        if filterset.is_valid():
            students = filterset.qs
        else:
            students = students.none()

        paginator = StudentsAPIListPagination()
        paginated_students = paginator.paginate_queryset(students, request)
        if paginated_students is not None:
            return paginator.get_paginated_response(StudentsSerializer(paginated_students, many=True).data)
        
        return Response({'students': StudentsSerializer(students, many=True).data}, status=status.HTTP_200_OK)
    
class StudentDetailView(APIView):
    def get(self, request, pk):
        student = Student.objects.get(pk=pk)
        serializer = StudentsSerializer(student)
        return Response(serializer.data)
    
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

