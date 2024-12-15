# sensor/models.py

from django.db import models
from django.contrib.auth.models import User

class SensorReading(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)  # Allow null for ESP data
    timestamp = models.DateTimeField(auto_now_add=True)
    water_level = models.FloatField()
    vibration = models.FloatField()

    def __str__(self):
        user_str = self.user.username if self.user else "ESP Device"
        return f"{user_str} - {self.timestamp} - Water Level: {self.water_level}, Vibration: {self.vibration}"


class Notification(models.Model):
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    subject = models.CharField(max_length=255)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification to {self.recipient.username} at {self.timestamp}"


class EmailNotification(models.Model):
    subject = models.CharField(max_length=255)
    recipient = models.EmailField()
    message = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Email to {self.recipient} at {self.sent_at}"
    


class SafetyLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='safety_logs')
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Safety log by {self.user.username} at {self.timestamp}"
