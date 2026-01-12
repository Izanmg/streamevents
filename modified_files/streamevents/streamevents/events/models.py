from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Event(models.Model):
    name = models.CharField(max_length=255)
    status = models.CharField(max_length=50, default='live') # 'live', 'upcoming', 'finished'
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_events')

    def __str__(self):
        return self.name
