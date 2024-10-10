from django.db.models import Avg
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework import generics
from school.models import CustomUser, Group1, Student, Subject, Grade
from school.api.serializers import CustomUserSerializer, Group1Serializer, StudentSerializer, SubjectSerializer, GradeSerializer
from school.api.permissions import RoleBasePermission
# from django.db import connection


#list of object and create object
class CustomUserListCreateView(generics.ListCreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [RoleBasePermission]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # Save the user but without committing to the database yet
        user = serializer.save()

        # Hash the password before saving the user and then save the user with hashed password
        user.set_password(serializer.validated_data['password'])
        user.save()
        
        refresh = RefreshToken.for_user(user)
        tokens = {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }

        return Response({
            "user": CustomUserSerializer(user).data,
            'tokens': tokens
        }, status=status.HTTP_201_CREATED)


#detail, update, delete of object with PK
class CustomUserDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [RoleBasePermission]


class GroupListCreateView(generics.ListCreateAPIView):
    queryset = Group1.objects.all()
    serializer_class = Group1Serializer
    permission_classes = [RoleBasePermission]


class Group1DetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Group1.objects.all()
    serializer_class = Group1Serializer
    permission_classes = [RoleBasePermission]


class StudentListCreateView(generics.ListCreateAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = [RoleBasePermission]


class StudentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = [RoleBasePermission]


class SubjectListCreateView(generics.ListCreateAPIView):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer
    permission_classes = [RoleBasePermission]


class SubjectDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer
    permission_classes = [RoleBasePermission]


class GradeListCreateView(generics.ListCreateAPIView):
    queryset = Grade.objects.all()
    serializer_class = GradeSerializer
    permission_classes = [RoleBasePermission]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'student':
            student = Student.objects.get(user=user)
            return Grade.objects.filter(student=student)
        return Grade.objects.all()


class GradeDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Grade.objects.all()
    serializer_class = GradeSerializer
    permission_classes = [RoleBasePermission]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'student':
            student = Student.objects.get(user=user)
            return Grade.objects.filter(student=student)
        return Grade.objects.all()


class GroupAverageGradeView(APIView):
    def get(self, request, group_id):
        group = Group1.objects.get(id=group_id)
        students_in_group = Student.objects.filter(groups=group)
        avg_grades = Grade.objects.filter(student__in=students_in_group).values('subject__name').annotate(average_grade=Avg('grade'))
        return Response(avg_grades)
    
    """
    Uncomment the following block and comment out the `get` method at the top to use RAW SQL for querying.
    """
    # def get(self, request, group_id):
    #     with connection.cursor() as cursor:
    #         cursor.execute('''
    #             SELECT subject.name, AVG(grade.grade) 
    #             FROM grade 
    #             JOIN student ON grade.student_id = student.id 
    #             JOIN subject ON grade.subject_id = subject.id
    #             JOIN student_groups ON student.id = student_groups.student_id 
    #             WHERE student_groups.group1_id = %s 
    #             GROUP BY subject.name
    #         ''', [group_id])
    #         rows = cursor.fetchall()

    #     return Response({'average_grades': rows})