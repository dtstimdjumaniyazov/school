from rest_framework import serializers
from school.models import CustomUser, Group1, Student, Subject, Grade

class CustomUserSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'password', 'password2', 'role']
        extra_kwargs = {
            'password': {'write_only': True}
        }    
    
    def validate(self, data):
        password = data.get('password')
        password2 = data.get('password2')
        
        if password != password2:
            raise serializers.ValidationError({'error': 'Пароли не совпадают.'})
        
        data['is_staff'] = True
        data['is_active'] = True
        data.pop('password2', None)
        return data 
        

class Group1Serializer(serializers.ModelSerializer):
    student = serializers.PrimaryKeyRelatedField(queryset=Student.objects.all(), many=True)
    teacher = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.filter(role='teacher'))
    
    class Meta:
        model = Group1
        fields = ['id', 'name', 'student', 'teacher']

    def validate_name(self, value):
        if Group1.objects.filter(name=value).exists():
            raise serializers.ValidationError("Группа с таким именем уже существует.")
        return value
    
    def validate(self, data):
        students = data.get('student')
        for student in students:
            if Group1.objects.filter(student=student).exists():
                raise serializers.ValidationError(f"Студент с {student.id} уже существует в другой группе.")
        return data


class StudentSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.filter(role='student'))

    class Meta:
        model = Student
        fields = ['id', 'first_name', 'last_name', 'patronymic', 'user']


class SubjectSerializer(serializers.ModelSerializer):
    teacher = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.filter(role='teacher'))
    groups = serializers.PrimaryKeyRelatedField(many=True, queryset=Subject.objects.all())

    class Meta:
        model = Subject
        fields = ['id', 'name', 'teacher', 'groups']
    
    def validate_name(self, value):
        if Subject.objects.filter(name=value).exists():
            raise serializers.ValidationError("Предмет уже существует в базе данных.")
        return value


class GradeSerializer(serializers.ModelSerializer):
    student = serializers.PrimaryKeyRelatedField(queryset=Student.objects.all())
    subject = serializers.PrimaryKeyRelatedField(queryset=Subject.objects.all())

    class Meta:
        model = Grade
        fields = ['id', 'student', 'subject', 'grade']