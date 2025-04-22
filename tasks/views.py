# tasks/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from django.utils.timezone import now
from django.db.models import Q

from .models import Task
from .serializers import TaskSerializer
from users.models import User 

class TaskCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = request.data.copy()
        # data['assigned_by'] = request.user.id

        if int(data.get('assigned_to')) == request.user.id:
            return Response({"error": "You cannot assign tasks to yourself."},
                            status=status.HTTP_400_BAD_REQUEST)

        serializer = TaskSerializer(data=data)
        if serializer.is_valid():
            serializer.save(assigned_by=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TaskPagination(PageNumberPagination):
    page_size = 10  
    page_size_query_param = 'page_size'
    max_page_size = 100 

class TaskListAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        tasks = Task.objects.filter(
            Q(assigned_by=user) | Q(assigned_to=user)   
        )

        status_filter = request.query_params.get('status')
        if status_filter:
            tasks = tasks.filter(status=status_filter)

        priority_filter = request.query_params.get('priority')
        if priority_filter:
            tasks = tasks.filter(priority=priority_filter)

        due_before = request.query_params.get('due_before')
        if due_before:
            tasks = tasks.filter(due_date__lte=due_before)

        due_after = request.query_params.get('due_after')
        if due_after:
            tasks = tasks.filter(due_date__gte=due_after)

        search_term = request.query_params.get('search')
        if search_term:
            tasks = tasks.filter(
                Q(title__icontains=search_term) | Q(description__icontains=search_term)
            )

        paginator = TaskPagination()
        paginated_tasks = paginator.paginate_queryset(tasks, request)
        serializer = TaskSerializer(paginated_tasks, many=True)

        return paginator.get_paginated_response(serializer.data)


class TaskDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk, user):
        try:
            task = Task.objects.get(pk=pk)
            if task.assigned_by != user and task.assigned_to != user:
                return None
            return task
        except Task.DoesNotExist:
            return None

    def get(self, request, pk):
        task = self.get_object(pk, request.user)
        if not task:
            return Response({"error": "Task not found or permission denied."}, status=status.HTTP_404_NOT_FOUND)
        
        if task.due_date < now().date() and task.status != 4:
            task.status = 4
            task.save()

        serializer = TaskSerializer(task)
        return Response(serializer.data)

    def put(self, request, pk):
        task = self.get_object(pk, request.user)
        if not task:
            return Response({"error": "Task not found or permission denied."}, status=status.HTTP_404_NOT_FOUND)

        if task.assigned_by != request.user:
            return Response({"error": "Only the user who created the task can update it."},
                            status=status.HTTP_403_FORBIDDEN)

        serializer = TaskSerializer(task, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid():
            serializer.save(assigned_by=task.assigned_by)
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        task = self.get_object(pk, request.user)
        if not task:
            return Response({"error": "Task not found or permission denied."}, status=status.HTTP_404_NOT_FOUND)

        if task.assigned_by != request.user:
            return Response({"error": "Only the user who created the task can delete it."},
                            status=status.HTTP_403_FORBIDDEN)

        task.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
