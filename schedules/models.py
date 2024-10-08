from django.db import models
from django.forms import ValidationError
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
        time_between_doses = self.medication.calculate_time_between_doses()

        if not time_between_doses:
            raise ValidationError('Cannot calculate next dose without valid frequency or time interval.')

        # Set the next dose based on the time interval or frequency per day
        if self.medication.priority_flag:
            # Priority medication logic
            lead_time_passed, next_allowed_time = self.medication.priority_lead_time_check()
            if not lead_time_passed:
                self.next_dose = next_allowed_time
            else:
                self.next_dose = timezone.now() + time_between_doses
        else:
            # Regular medication: calculate next dose based on frequency per day or time interval
            self.next_dose = timezone.now() + time_between_doses
        
        self.save()

    def calculate_expected_end_time(self):
        """Calculate the expected end time for all doses to be completed."""
        if self.medication.total_left <= 0:
            # Medication exhausted
            self.expected_end_time = timezone.now()
            self.status = 'completed'
            self.medication.status = 'exhausted'
            self.medication.save()
        else:
            # Calculate remaining doses and expected end time
            doses_remaining = self.medication.total_left // self.medication.dosage_per_intake
            time_between_doses = self.medication.calculate_time_between_doses()
            print('TIME BETWEEN DOSES: ', time_between_doses)

            self.expected_end_time = self.start_time + timedelta(hours=time_between_doses.total_seconds() / 3600 * doses_remaining)
        self.save()


    def handle_end_of_reminder(self):
        """Check if the schedule has reached its end and perform necessary updates."""
        
        # If the medication has been stopped, update status accordingly
        if self.medication.status == 'stopped':
            self.status = 'stopped'
            self.stopped_time = timezone.now()  # TODO: TIME SHOULD COME FROM THE ENDPOINT ACTION
            self.save()
            return

        # If the current time has reached or passed the expected end time
        if timezone.now() >= self.expected_end_time:
            # Check if the medication is exhausted
            if self.medication.is_exhausted():
                self.status = 'completed'
                self.medication.status = 'exhausted'
                self.medication.save()
            else:
                # If the medication is still active but past its reminder
                self.status = 'completed'
            self.save()
        else:
            # If schedule hasn't ended, calculate the next dose
            self.calculate_next_dose()
        
        # Optionally: Handle missed doses (if applicable)
        if self.status == 'missed':
            MissedDose.objects.create(medication=self.medication, schedule=self)
            self.medication.total_left -= self.medication.dosage_per_intake
            self.medication.save()
            self.save()


    def generate_recurring_schedules(self):
        """
        Generate recurring schedule entries based on the medication's frequency and interval.
        Handles edge cases where the medication is paused or stopped.
        """
        total_doses = self.medication.total_quantity // self.medication.dosage_per_intake
        for i in range(total_doses):
            # Check if the medication is still active, or break the loop if stopped
            if self.medication.status not in ['active', 'completed']:
                break

            next_dose_time = self.start_time + timezone.timedelta(hours=self.medication.time_interval * i)
            Schedule.objects.create(
                medication=self.medication,
                start_time=next_dose_time,
                status='scheduled',
            )

    def __str__(self):
        return f'Schedule for {self.medication.user.email}'

class MissedDose(models.Model):
    medication = models.ForeignKey(Medication, on_delete=models.CASCADE)
    schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE)
    missed_at = models.DateTimeField(auto_now_add=True)

    def adjust_medication_quantity(self):

        """Automatically reduce medication quantity when a dose is missed."""
        if self.medication.total_left > 0:
            self.medication.total_left -= self.medication.dosage_per_intake
            self.medication.save()

    def mark_schedule_as_missed(self):
        """Mark the associated schedule as missed and adjust the medication quantity."""
        self.schedule.status = 'missed'
        self.schedule.save()
        self.adjust_medication_quantity()


