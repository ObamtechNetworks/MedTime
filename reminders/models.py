from django.db import models
from django.utils import timezone
from medications.models import Medication

class Reminder(models.Model):
    medication = models.ForeignKey(Medication, on_delete=models.CASCADE)
    scheduled_time = models.DateTimeField()
    acknowledged = models.BooleanField(default=False)
    acknowledged_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Reminder for {self.medication.drug_name} at {self.scheduled_time}'

    def mark_as_acknowledged(self):
        self.acknowledged = True
        self.acknowledged_at = timezone.now()
        self.save()
