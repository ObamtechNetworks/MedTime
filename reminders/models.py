from datetime import timezone
from django.db import models

from users.models import User
from schedules.models import Schedule

# Create your models here.
class Reminder(models.Model):
    """Model to handle reminders"""
    schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    reminder_time = models.DateTimeField(auto_now_add=True)  # Time reminder was created/sent
    acknowledged = models.BooleanField(default=False)
    acknowledgement_time = models.DateTimeField(null=True, blank=True)
    missed = models.BooleanField(default=False)

    def mark_as_acknowledged(self):
        """Mark reminder as acknowledged"""
        self.acknowledged = True
        self.acknowledgement_time = timezone.now()
        self.save()

    def mark_as_missed(self):
        """Marks a reminder as missed"""
        self.missed = True
        self.save()

    def __str__(self) -> str:
        """String representation for reminder"""
        return f"Reminder for {self.user} on schedule {self.schedule}"
