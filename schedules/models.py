from django.db import models
from django.utils import timezone
from medications.models import Medication

class Schedule(models.Model):
    STATUS_CHOICES = [
        ('scheduled', 'Scheduled'),
        ('fulfilled', 'Fulfilled'),
        ('missed', 'Missed'),
        ('stopped', 'Stopped'),
        ('deleted', 'Deleted'),
    ]

    medication = models.ForeignKey(Medication, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    next_dose_due_at = models.DateTimeField()  # Time for next dose
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='scheduled')
    fulfilled_time = models.DateTimeField(null=True, blank=True)  # Time dose was taken
    missed_time = models.DateTimeField(null=True, blank=True)  # When dose was missed
    stopped_time = models.DateTimeField(null=True, blank=True)
    deleted_time = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    def mark_as_fulfilled(self):
        """Mark a scheduled as fulfilled and update med qty"""
        self.status = 'fulfilled'
        self.fulfilled_time = timezone.now()
        self.save()
        # update medication
        self.medication.update_quantity(dose_taken=True)

    def mark_as_missed(self):
        """mark the schedule as missed and update med qty"""
        self.status = 'missed'
        self.missed_time = timezone.now()
        self.save()
        # update the missed dose in the MissedDose model
        # Create a MissedDose record
        missed_dose = MissedDose.objects.create(
            medication=self.medication,
            schedule=self,
        )
        # adjust missed dose quantity
        missed_dose.adjust_medication_quantity()


    def is_due(self):
        """Check if this schedule is due."""
        return self.next_dose_due_at <= timezone.now() and self.status == 'scheduled'


    def __str__(self):
        return f'Schedule for {self.medication.user.email}, \
            Medication: {self.medication.drug_name}, Start: {self.next_dose_due_at}'


class MissedDose(models.Model):
    medication = models.ForeignKey(Medication, on_delete=models.CASCADE)
    schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE)
    missed_at = models.DateTimeField(auto_now_add=True)

    def adjust_medication_quantity(self):

        """Automatically reduce medication quantity when a dose is missed."""
        self.medication.update_quantity(dose_taken=False)
