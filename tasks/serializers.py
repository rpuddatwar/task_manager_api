# tasks/serializers.py
from rest_framework import serializers
from .models import Task
from users.models import User
from django.utils import timezone


class TaskSerializer(serializers.ModelSerializer):
    assigned_by = serializers.PrimaryKeyRelatedField(read_only=True)
    assigned_to = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'status', 'priority', 'due_date', 'created_at', 'assigned_by', 'assigned_to']
        read_only_fields = ['created_at', 'assigned_by']

    def validate(self, data):
        if self.context['request'].user == data.get('assigned_to'):
            raise serializers.ValidationError("You cannot assign a task to yourself.")
        return data

    def update(self, instance, validated_data):
        """
        Override the update method to recheck the task's status when updating.  
        The status will be set to 'Overdue' (status=4) if the due date has passed.
        """
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)
        instance.status = validated_data.get('status', instance.status)
        instance.priority = validated_data.get('priority', instance.priority)
        instance.due_date = validated_data.get('due_date', instance.due_date)
        instance.assigned_by = validated_data.get('assigned_by', instance.assigned_by)
        instance.assigned_to = validated_data.get('assigned_to', instance.assigned_to)

        # Check if the due date is in the past and update status accordingly
        if instance.due_date < timezone.now().date() and instance.status != 4:
            instance.status = 4  # Mark the task as Overdue

        instance.save()
        return instance
