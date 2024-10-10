from django.db import models
from django.db import transaction  # for atomicity
from django.forms import ValidationError
from django.utils import timezone
from medications.models import Medication
from datetime import datetime, timedelta

class Schedule(models.Model):
    STATUS_CHOICES = [
        ('scheduled', 'Scheduled'),
        ('fulfilled', 'Fulfilled'),
        ('missed', 'Missed'),
        ('stopped', 'Stopped'),
        ('deleted', 'Deleted'),
    ]

    medication = models.ForeignKey(Medication, on_delete=models.CASCADE)
    scheduled_time = models.DateTimeField()  # Start time for the dose
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='scheduled')
    fulfilled_time = models.DateTimeField(null=True, blank=True)  # Time dose was taken
    missed_time = models.DateTimeField(null=True, blank=True)  # When all doses are expected to be completed
    next_dose_schedule = models.DateTimeField(null=True, blank=True)  # Time for next dose
    stopped_time = models.DateTimeField(null=True, blank=True)
    deleted_time = models.DateTimeField(null=True, blank=True)

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


    # def create_next_schedule(medications, last_scheduled_time):
    #     """Create the next schedules for all medications and handle priority logic."""
    #     #TODO???
    #     pass



    def is_due(self):
        """Check if this schedule is due."""
        return self.scheduled_time <= timezone.now() and self.status == 'scheduled'


    def __str__(self):
        return f'Schedule for {self.medication.user.email}, \
            Medication: {self.medication.drug_name}, Start: {self.scheduled_time}'


class MissedDose(models.Model):
    medication = models.ForeignKey(Medication, on_delete=models.CASCADE)
    schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE)
    missed_at = models.DateTimeField(auto_now_add=True)

    def adjust_medication_quantity(self):

        """Automatically reduce medication quantity when a dose is missed."""
        self.medication.update_quantity(dose_taken=False)
