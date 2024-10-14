from rest_framework import serializers
from school.models import CustomUser, Group1, Student, Subject, Grade

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'role']

class StudentSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer(read_only=True)
    full_name = serializers.SerializerMethodField()

    class Meta:
        model = Student
        fields = ['id', 'full_name', 'user']

    def get_full_name(self, obj):
        return f"{obj.last_name} {obj.first_name} {obj.patronymic}"

class Group1Serializer(serializers.ModelSerializer):
    students = StudentSerializer(source='student', many=True, read_only=True)
    teacher = CustomUserSerializer(read_only=True)

    class Meta:
        model = Group1
        fields = ['id', 'name', 'students', 'teacher']

class SubjectSerializer(serializers.ModelSerializer):
    teacher = CustomUserSerializer(read_only=True)
    groups = Group1Serializer(many=True, read_only=True)

    class Meta:
        model = Subject
        fields = ['id', 'name', 'teacher', 'groups']

class GradeSerializer(serializers.ModelSerializer):
    student = StudentSerializer(read_only=True)
    subject = SubjectSerializer(read_only=True)

    class Meta:
        model = Grade
        fields = ['id', 'student', 'subject', 'grade']