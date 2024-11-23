"""
URL configuration for student_management_system project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)
from users.views import UserRegisterView
from users.views import LogoutView, CustomTokenObtainPairView
from students.views import StudentsAPIView, StudentProfileAPIView, StudentDetailView
from courses.views import CoursesAPIView, CoursesAPIViewEdit, CoursesAPIViewEnroll
from grades.views import GradesAPIView, GradesAPIViewPost, GradesAPIViewUpdate
from attendance.views import AttendanceAPIView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/register/', UserRegisterView.as_view(), name='register'),
    path('api/login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/login/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('api/logout/', LogoutView.as_view(), name='logout'),

    path('api/students/', StudentsAPIView.as_view(), name='students_list'),


    path('api/students/<int:pk>/', StudentDetailView.as_view(), name='student-detail'),


    path('api/student/profile/', StudentProfileAPIView.as_view(), name='student_profile'),

    path('api/courses/', CoursesAPIView.as_view(), name='courses_list'),
    path('api/courses/add/', CoursesAPIViewEdit.as_view(), name='courses_add'),
    path('api/courses/edit/<int:course_id>/', CoursesAPIViewEdit.as_view(), name='courses_edit'),
    path('api/courses/enrollment/', CoursesAPIViewEnroll.as_view(), name='courses_enroll'),

    path('api/grades/<int:course_id>/', GradesAPIView.as_view(), name='grades'),
    path('api/grades/', GradesAPIViewPost.as_view(), name='grades-post'),
    path('api/grades/update/course/<int:course_id>/student/<int:student_id>/', GradesAPIViewUpdate.as_view(), name='grades_update'),

    path('api/attendance/<int:course_id>/', AttendanceAPIView.as_view(), name='show_attendance'),
    path('api/attendance/', AttendanceAPIView.as_view(), name='create_attendance'),
]

