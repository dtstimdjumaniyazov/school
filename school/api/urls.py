from django.urls import path, include
from school.api.views import (
    CustomUserListCreateView, CustomUserDetailView,
    GroupListCreateView, Group1DetailView,
    StudentListCreateView, StudentDetailView,
    SubjectListCreateView, SubjectDetailView,
    GradeListCreateView, GradeDetailView,
    GroupAverageGradeView
    )

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    #JWT tokens
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    #For Users CRUD
    path('users/', CustomUserListCreateView.as_view(), name='user-list-create'),
    path('users/<int:pk>/', CustomUserDetailView.as_view(), name='user-detail'),

    #For Group1
    path('groups/', GroupListCreateView.as_view(), name='group-list-create'),
    path('groups/<int:pk>/', Group1DetailView.as_view(), name='group-detail'),

    #For Students
    path('students/', StudentListCreateView.as_view(), name='students-list-create'),
    path('students/<int:pk>/', StudentDetailView.as_view(), name='student-detail'),

    #For Subject
    path('subjects/', SubjectListCreateView.as_view(), name='subject-list-create'),
    path('subjects/<int:pk>/', SubjectDetailView.as_view(), name='subject-detail'),

    #For Grade
    path('grades/', GradeListCreateView.as_view(), name='grade-list-create'),
    path('grades/<int:pk>/', GradeDetailView.as_view(), name='grade-detail'),

    #For average grade for each subject at define group
    path('groups/<int:group_id>/average-grades/', GroupAverageGradeView.as_view(), name='group-average-grades'),
]