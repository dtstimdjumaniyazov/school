from django.contrib import admin
from django.contrib.auth.models import Group
from .models import CustomUser, Group1, Student, Subject, Grade

class CustomUserAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        if request.user.role == 'director':
            return qs
        elif request.user.role == 'teacher':
            return qs.filter(role='teacher')
        elif request.user.role == 'student':
            return qs.filter(id=request.user.id)
        return qs.none()

    def has_add_permission(self, request):
        if request.user.is_superuser:
            return True
        if request.user.role == 'director':
            return True
        return False

    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser or request.user.role == 'director':
            return True
        return False

    def has_delete_permission(self, request, obj=None):
        if request.user.is_superuser or request.user.role == 'director':
            return True
        return False

class Group1Admin(admin.ModelAdmin):
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        if request.user.role == 'director':
            return qs
        elif request.user.role == 'teacher':
            return qs.filter(teacher=request.user)
        return qs.none()

    def has_add_permission(self, request):
        if request.user.is_superuser or request.user.role == 'director':
            return True
        return False

    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser or request.user.role == 'director':
            return True
        return False

class StudentAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        if request.user.role == 'director':
            return qs
        elif request.user.role == 'teacher':
            return qs.filter(group1__teacher=request.user)
        elif request.user.role == 'student':
            return qs.filter(user=request.user)
        return qs.none()

    def has_add_permission(self, request):
        if request.user.is_superuser or request.user.role == 'director':
            return True
        return False

    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser or request.user.role == 'director':
            return True
        return False

    def has_delete_permission(self, request, obj=None):
        if request.user.is_superuser or request.user.role == 'director':
            return True
        return False

class GradeAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        if request.user.role == 'director':
            return qs
        elif request.user.role == 'teacher':
            return qs
        elif request.user.role == 'student':
            return qs.filter(student__user=request.user)
        return qs.none()

    def has_add_permission(self, request):
        if request.user.is_superuser or request.user.role == 'teacher':
            return True
        return False

    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser or request.user.role == 'teacher':
            return True
        return False

    def has_delete_permission(self, request, obj=None):
        if request.user.is_superuser or request.user.role == 'teacher':
            return True
        return False


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Group1, Group1Admin)
admin.site.register(Student, StudentAdmin)
admin.site.register(Subject)
admin.site.register(Grade, GradeAdmin)

admin.site.unregister(Group)