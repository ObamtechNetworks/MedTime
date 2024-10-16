# from datetime import timedelta
# from django.db import models
# from django.utils import timezone
# from medications.models import Medication

# class Reminder(models.Model):
#     medication = models.ForeignKey(Medication, on_delete=models.CASCADE)
#     scheduled_time = models.DateTimeField()
#     acknowledged = models.BooleanField(default=False)
#     acknowledged_at = models.DateTimeField(null=True, blank=True)
#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f'Reminder for {self.medication.drug_name} at {self.scheduled_time}'

#     def is_due(self):
#         """Check if the reminder is due."""
#         return self.scheduled_time <= timezone.now() and not self.acknowledged

#     def mark_as_missed(self):
#         """Mark all schedules as missed if not acknowledged within the time limit."""
#         if timezone.now() > self.scheduled_time + timedelta(hours=1):
#             self.medication.status = 'missed'  # Or whatever logic you need to mark it missed
#             self.medication.save()