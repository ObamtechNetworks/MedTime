from django.db import models
from django.utils import timezone
from medications.models import Medication
from datetime import timedelta

class Schedule(models.Model):
    STATUS_CHOICES = [
        ('scheduled', 'Scheduled'),
        ('taken', 'Taken'),
        ('missed', 'Missed'),
        ('stopped', 'Stopped'),
        ('completed', 'Completed'),
        ('deleted', 'Deleted'),
    ]

    medication = models.ForeignKey(Medication, on_delete=models.CASCADE)
    start_time = models.DateTimeField()  # Start time for the dose
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='scheduled')
    fulfilled_time = models.DateTimeField(null=True, blank=True)  # Time dose was taken
    next_dose = models.DateTimeField(null=True, blank=True)  # Time for next dose
    expected_end_time = models.DateTimeField(null=True, blank=True)  # When all doses are expected to be completed
    stopped_time = models.DateTimeField(null=True, blank=True)
    deleted_time = models.DateTimeField(null=True, blank=True)

    def calculate_next_dose(self):
        """Calculate the next dose time, considering priority medications."""
        # Check if the medication is priority
        if self.medication.priority_flag:
            lead_time_passed, next_allowed_time = self.medication.priority_lead_time_check()
            if not lead_time_passed:
                # If the priority lead time has not passed, set the next dose after lead time
                self.next_dose = next_allowed_time
            else:
                # Set next dose based on medication's time interval
                self.next_dose = timezone.now() + timedelta(hours=self.medication.time_interval)
        else:
            # Non-priority case: calculate next dose based on the time interval
            self.next_dose = timezone.now() + timedelta(hours=self.medication.time_interval)
        self.save()

    def calculate_expected_end_time(self):
        """Calculate when all doses should be completed for the current medication."""
        # Only calculate if total_quantity and dosage_per_intake are valid
        if self.medication.total_left > 0 and self.medication.dosage_per_intake > 0:
            doses_remaining = self.medication.total_left // self.medication.dosage_per_intake
            self.expected_end_time = self.start_time + timedelta(hours=self.medication.time_interval * doses_remaining)
        else:
            self.expected_end_time = None
        self.save()

    def handle_end_of_reminder(self):
        """Check if the schedule has reached its end and perform necessary updates."""
        if timezone.now() >= self.expected_end_time:
            # If the medication is exhausted, update status accordingly
            if self.medication.is_exhausted():
                self.status = 'completed'
                self.medication.status = 'exhausted'
                self.medication.save()
            else:
                # If the medication is still active but past its reminder, mark it completed
                self.status = 'completed'
            self.save()
        else:
            self.calculate_next_dose()

    def generate_recurring_schedules(self):
        """
        Generate recurring schedule entries based on the medication's frequency and interval.
        This method will generate multiple `Schedule` entries for the same medication.
        """
        total_doses = self.medication.total_quantity // self.medication.dosage_per_intake
        for i in range(total_doses):
            next_dose_time = self.start_time + timezone.timedelta(hours=self.medication.time_interval * i)
            Schedule.objects.create(
                medication=self.medication,
                start_time=next_dose_time,
                status='scheduled',
            )


class MissedDose(models.Model):
    medication = models.ForeignKey(Medication, on_delete=models.CASCADE)
    schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE)
    missed_at = models.DateTimeField(auto_now_add=True)

    def adjust_medication_quantity(self):
        """Automatically reduce medication quantity when a dose is missed."""
        self.medication.total_left -= self.medication.dosage_per_intake
        self.medication.save()

    def mark_schedule_as_missed(self):
        """Mark the associated schedule as missed."""
        self.schedule.status = 'missed'
        self.schedule.save()

