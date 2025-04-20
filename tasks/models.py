# tasks/models.py
from django.db import models
from users.models import User
from django.utils import timezone

class Task(models.Model):
    STATUS_CHOICES = [
        (1, 'Open'),
        (2, 'In Progress'),
        (3, 'Done'),
        (4, 'Overdue'),
    ]

    PRIORITY_CHOICES = [
        (1, 'Low'),
        (2, 'High'),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField()
    status = models.IntegerField(choices=STATUS_CHOICES, default=1)
    priority = models.IntegerField(choices=PRIORITY_CHOICES, default=1)
    due_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    assigned_by = models.ForeignKey(User, related_name='tasks_created', on_delete=models.CASCADE)
    assigned_to = models.ForeignKey(User, related_name='tasks_assigned', on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if self.due_date < timezone.now().date() and self.status != 4:
            self.status = 4
        super().save(*args, **kwargs)
