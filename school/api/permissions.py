from rest_framework.permissions import BasePermission, SAFE_METHODS

class RoleBasePermission(BasePermission):
    
    def has_permission(self, request, view):
        user = request.user
        print(f"User: {user.username}, Role: {user.role}, Method: {request.method}")

        if user.is_superuser:
            return True

        # Define current view by its class name
        view_name = view.__class__.__name__

        # Director: CRUD for Group1, Students, Subjects
        if user.role == 'director':
            if view_name in ['GroupListCreateView', 'Group1DetailView', 'StudentListCreateView', 'StudentDetailView', 'SubjectListCreateView', 'SubjectDetailView']:
                return True

        # Teacher can view groups, subjects, students and manage grades
        elif user.role == 'teacher':
            if view_name == 'GradeListCreateView' and request.method in ['GET', 'POST', 'PUT', 'DELETE']:
                return True  # Allow CRUD operations on Grade
            elif view_name in ['GroupListCreateView', 'StudentListCreateView', 'SubjectListCreateView'] and request.method in SAFE_METHODS:
                return True  # Allow Read-Only for other resources
            return False


        # Student: Read-only for their own grades, and can view subjects, and students.
        elif user.role == 'student':
            if view_name in ['StudentListCreateView', 'StudentDetailView', 'SubjectListCreateView', 'SubjectDetailView'] and request.method in SAFE_METHODS:
                return True
            # Grades: The student can see only their own grades (object-level permission)
            elif view_name in ['GradeDetailView', 'GradeListCreateView'] and request.method in SAFE_METHODS:
                return True  # Allow basic read access, but we'll filter in `has_object_permission`.

        return False

    def has_object_permission(self, request, view, obj):
        user = request.user

        # Ensure that a student can only see their own grades
        if user.role == 'student' and hasattr(obj, 'student'):
            return obj.student == user  # Allow access only if the grade belongs to the current student
        
        return False