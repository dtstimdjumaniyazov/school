from rest_framework.permissions import BasePermission, SAFE_METHODS
from school.models import CustomUser, Group1, Student, Grade

class RoleBasePermission(BasePermission):

    def has_permission(self, request, view):
        user = request.user
        print(f"Checking permission for user: {user.username if user.is_authenticated else 'Anonymous'}, role: {getattr(user, 'role', 'No role')}, method: {request.method}")

        if not user.is_authenticated:
            print("User is not authenticated. Access denied.")
            return False
        
        if user.is_superuser:
            print(f"Access granted: Superuser {user.username}")
            return True

        view_name = view.__class__.__name__

        if user.role == 'director':
            if view_name in ['CustomUserListCreateView', 'CustomUserDetailView', 'GroupListCreateView', 'Group1DetailView', 'StudentListCreateView', 'StudentDetailView', 'SubjectListCreateView', 'SubjectDetailView']:
                print(f"Access granted: Director {user.username} for {view_name}")
                return True
            if view_name == 'GradeListCreateView' and request.method in SAFE_METHODS:
                print(f"Access granted: Director {user.username} for GradeListCreateView (read-only)")
                return True
            print(f"Access denied: Director {user.username} for {view_name}")
            return False

        # Teacher can see groups, subjects, students, and manage grades
        elif user.role == 'teacher':
            if view_name == 'CustomUserDetailView':
                if request.user.id == view.kwargs.get('pk'):
                    print(f"Access granted: Teacher {user.username} viewing their own details")
                    return True
                print(f"Access denied: Teacher {user.username} trying to view another user's details")
                return False
            
            if view_name == 'GradeListCreateView' and request.method in ['GET', 'POST', 'PUT', 'DELETE']:
                print(f"Access granted: Teacher {user.username} for GradeListCreateView")
                return True
            elif view_name in ['GroupListCreateView', 'StudentListCreateView', 'SubjectListCreateView'] and request.method in SAFE_METHODS:
                print(f"Access granted: Teacher {user.username} for {view_name}")
                return True
            print(f"Access denied: Teacher {user.username} for {view_name}")
            return False

        # Student permissions
        elif user.role == 'student':
            if view_name == 'CustomUserDetailView':
                if request.user.id == view.kwargs.get('pk'):
                    print(f"Access granted: Student {user.username} viewing their own details")
                    return True
                print(f"Access denied: Student {user.username} trying to view another user's details")
                return False
            if view_name in ['StudentListCreateView', 'StudentDetailView', 'SubjectListCreateView', 'SubjectDetailView'] and request.method in SAFE_METHODS:
                print(f"Access granted: Student {user.username} for {view_name}")
                return True
            if view_name in ['GradeDetailView', 'GradeListCreateView'] and request.method in SAFE_METHODS:
                print(f"Access granted: Student {user.username} for grades")
                return True
            print(f"Access denied: Student {user.username} for {view_name}")
            return False

        print(f"Access denied: {user.username} ({user.role}) for {view_name}")
        return False

    def has_object_permission(self, request, view, obj):
        user = request.user

        if user.is_superuser:
            print(f"Object permission granted: Superuser {user.username}")
            return True

        if user.role == 'director':
            print(f"Object permission granted: Director {user.username}")
            return True
        
        # Teachers can only view their own user details
        if user.role == 'teacher':
            if isinstance(obj, CustomUser):
                is_owner = obj.id == request.user.id
                print(f"Teacher access to own data: {is_owner}")
                return is_owner
            elif isinstance(obj, Student):
                is_student_in_teacher_group = Group1.objects.filter(teacher=user, student=obj).exists()
                print(f"Teacher access to student: {is_student_in_teacher_group}")
                return is_student_in_teacher_group
            elif isinstance(obj, Grade):
                is_grade_in_teacher_subject = obj.subject.teacher == user
                print(f"Teacher access to grade: {is_grade_in_teacher_subject}")
                return is_grade_in_teacher_subject

        # Students can only see their own user details
        if user.role == 'student':
            if isinstance(obj, CustomUser):
                is_owner = obj.id == request.user.id
                print(f"Student access to own data: {is_owner}")
                return is_owner
            elif isinstance(obj, Student):
                is_owner = obj == user.student
                print(f"Student access to own data: {is_owner}")
                return is_owner
            elif isinstance(obj, Grade):
                is_owner = obj.student == user.student
                print(f"Student access to own grade: {is_owner}")
                return is_owner

        return False