from rest_framework.permissions import BasePermission

class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'admin'
    
class IsStudent(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'student'
    
class IsTeacher(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'teacher'