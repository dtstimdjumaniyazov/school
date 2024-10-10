from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('director', 'director'),
        ('teacher', 'teacher'),
        ('student', 'student'),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)


class Group1(models.Model):
    name = models.CharField(max_length=100)
    student = models.ManyToManyField('Student', related_name='groups')
    teacher = models.ForeignKey('CustomUser', limit_choices_to={'role': 'teacher'}, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Student(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    patronymic = models.CharField(max_length=100)
    user = models.OneToOneField(CustomUser, limit_choices_to={'role': 'student'}, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.first_name} {self.last_name} {self.patronymic}"


class Subject(models.Model):
    name = models.CharField(max_length=100)
    teacher = models.ForeignKey(CustomUser, limit_choices_to={'role': 'teacher'}, on_delete=models.CASCADE)
    groups = models.ManyToManyField(Group1, related_name='subjects')

    def __str__(self):
        return self.name
    
    


class Grade(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    grade = models.IntegerField()

    def __str__(self):
        return f"{self.student} - {self.subject} - {self.grade}"