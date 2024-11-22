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
from django.core.cache import cache

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

        filterset = self.filterset_class(request.GET, queryset=courses)
        if filterset.is_valid():
            courses = filterset.qs
        else:
            courses = courses.none()

        paginator = CoursesAPIListPagination()
        paginated_students = paginator.paginate_queryset(courses, request)
        if paginated_students is not None:
            return paginator.get_paginated_response(CoursesSerializer(paginated_students, many=True).data)
        
        return Response({'students': CoursesSerializer(courses, many=True).data}, status=status.HTTP_200_OK)
    

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

        student_id = request.GET.get('student', None)
        instructor_id = request.GET.get('instructor', None)

        cache_key = f"courses_list_student_{student_id}_instructor_{instructor_id}"
        
        cached_courses = cache.get(cache_key)
        if cached_courses:
            return Response({"cached courses enrollment": cached_courses}, status=status.HTTP_200_OK)
        

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
            serialized_data = EnrollmentSerializer(paginated_students, many=True).data
            response_data = paginator.get_paginated_response(serialized_data).data
            
            cache.set(cache_key, response_data, timeout=600)  # Cache for 10 minutes
            return Response({"courses enrollment": response_data}, status=status.HTTP_200_OK)
        
        response_data = {'courses enrollment': serializer.data}
        cache.set(cache_key, response_data, timeout=600)  # Cache for 10 minutes
        
        return Response(response_data, status=status.HTTP_200_OK)

    def post(self, request):
        student_id = request.GET.get('student', None)
        instructor_id = request.GET.get('instructor', None)
        serializer = EnrollmentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()

            cache_key = f"courses_list_student_{student_id}_instructor_{instructor_id}"
            cache.delete(cache_key)

            return Response({"msg": "Student enrolled to the course successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)