from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timesince
from django.utils.translation import gettext_lazy as _
from events.models import Event

User = get_user_model()

class ChatMessage(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="messages")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    is_deleted = models.BooleanField(default=False)
    is_highlighted = models.BooleanField(default=False)

    class Meta:
        ordering = ["created_at"]
        verbose_name = "Missatge de Xat"
        verbose_name_plural = "Missatges de Xat"

    def __str__(self):
        return f"{self.user.username}: {self.message[:50]}"

    def can_delete(self, user):
        # Asumiendo que el modelo Event tiene un campo 'creator'
        return self.user == user or user.is_staff or (hasattr(self.event, 'creator') and self.event.creator == user)

    def get_user_display_name(self):
        return self.user.display_name if hasattr(self.user, "display_name") and self.user.display_name else self.user.username

    def get_time_since(self):
        return timesince.timesince(self.created_at)
