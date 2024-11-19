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
    
class IsTeacherOrAdmin(BasePermission):
    def has_permission(self, request, view):
        # Разрешить доступ, если пользователь является преподавателем или администратором
        return request.user.role in ['teacher', 'admin']
    
class IsStudentOrAdmin(BasePermission):
    def has_permission(self, request, view):
        # Разрешить доступ, если пользователь является преподавателем или администратором
        return request.user.role in ['student', 'admin']