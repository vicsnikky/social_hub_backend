from django.db import models

# Create your models here.
from django.conf import settings

class Event(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    location = models.CharField(max_length=255)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    interested_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='interested_events', blank=True)

    def __str__(self):
        return self.title
