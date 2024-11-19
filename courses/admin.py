from django.contrib import admin
from .models import Course, Enrollment  # Замените на вашу модель

admin.site.register(Course)

admin.site.register(Enrollment)