from django.db import models
from django.contrib.auth.models import User
from django.db.models import Avg

class Stats(models.Model):
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    avg_wpm = models.FloatField(default=0.0)
    last_wpm = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.username.username} - Avg: {self.avg_wpm}, Last: {self.last_wpm}"

class Attempt(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    wpm = models.IntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.user.username} - {self.wpm} WPM at {self.timestamp}"
