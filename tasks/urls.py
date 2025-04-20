# tasks/urls.py
from django.urls import path
from .views import TaskCreateAPIView, TaskListAPIView, TaskDetailAPIView

urlpatterns = [
    path('create/', TaskCreateAPIView.as_view(), name='task_create'),
    path('list/', TaskListAPIView.as_view(), name='task_list'),
    path('<int:pk>/', TaskDetailAPIView.as_view(), name='task_detail'),
]
