from django.shortcuts import render

# Create your views here.
from rest_framework import status
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from users.permissions import IsTeacher, IsStudent, IsAdmin, IsTeacherOrAdmin
from .serializers import CoursesSerializer, EnrollmentSerializer
from rest_framework.exceptions import NotFound
from .models import Course, Enrollment
import django_filters
from django_filters.rest_framework import DjangoFilterBackend

class CoursesAPIListPagination(PageNumberPagination):
    page_size = 2
    page_query_param = 'page_size'
    max_page_size = 100

class EnrollmentsAPIListPagination(PageNumberPagination):
    page_size = 2
    page_query_param = 'page_size'
    max_page_size = 100


class CoursesFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')
    description = django_filters.CharFilter(lookup_expr='icontains')
    instructor = django_filters.NumberFilter(lookup_expr='exact')

    class Meta:
        model = Course
        fields = ['name', 'description', 'instructor']

class EnrollmentsFilter(django_filters.FilterSet):
    student = django_filters.CharFilter(lookup_expr='exact')
    course = django_filters.NumberFilter(lookup_expr='exact')

    class Meta:
        model = Enrollment
        fields = ['student', 'course'] 

class CoursesAPIView(APIView):
    permission_classes = [IsAuthenticated]
    pagination_class = CoursesAPIListPagination

    filter_backends = (DjangoFilterBackend,)
    filterset_class = CoursesFilter 

    def get(self, request):
        courses = Course.objects.all()

        serializer = CoursesSerializer(courses, many=True)

        filterset = self.filterset_class(request.GET, queryset=courses)
        if filterset.is_valid():
            courses = filterset.qs
        else:
            courses = courses.none()

        paginator = CoursesAPIListPagination()
        paginated_students = paginator.paginate_queryset(courses, request)
        if paginated_students is not None:
            return paginator.get_paginated_response(CoursesSerializer(paginated_students, many=True).data)
        
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

    filter_backends = (DjangoFilterBackend,)
    filterset_class = EnrollmentsFilter 


    def get(self, request):
        enrollments = Enrollment.objects.all()

        serializer = EnrollmentSerializer(enrollments, many=True)

        filterset = self.filterset_class(request.GET, queryset=enrollments)
        if filterset.is_valid():
            enrollments = filterset.qs
        else:
            enrollments = enrollments.none()

        paginator = EnrollmentsAPIListPagination()
        paginated_students = paginator.paginate_queryset(enrollments, request)
        if paginated_students is not None:
            return paginator.get_paginated_response(EnrollmentSerializer(paginated_students, many=True).data)

        return Response({'enrollments': serializer.data}, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = EnrollmentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"msg": "Student enrolled to the course successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)