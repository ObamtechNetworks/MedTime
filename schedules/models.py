from django.db import models
from django.db import transaction  # for atomicity
from django.forms import ValidationError
from django.utils import timezone
from medications.models import Medication
from datetime import timedelta

class Schedule(models.Model):
    STATUS_CHOICES = [
        ('scheduled', 'Scheduled'),
        ('fulfilled', 'Fulfilled'),
        ('missed', 'Missed'),
        ('stopped', 'Stopped'),
        ('deleted', 'Deleted'),
    ]

    medication = models.ForeignKey(Medication, on_delete=models.CASCADE)
    start_time = models.DateTimeField()  # Start time for the dose
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='scheduled')
    fulfilled_time = models.DateTimeField(null=True, blank=True)  # Time dose was taken
    next_dose_schedule = models.DateTimeField(null=True, blank=True)  # Time for next dose
    expected_end_time = models.DateTimeField(null=True, blank=True)  # When all doses are expected to be completed
    stopped_time = models.DateTimeField(null=True, blank=True)
    deleted_time = models.DateTimeField(null=True, blank=True)

    def calculate_next_dose(self):
        """Calculate the next dose time, considering priority medications."""
        # check if medication is still active:
        if self.medication.status == 'active':
            time_between_doses = self.medication.calculate_time_between_doses()
            
            if not time_between_doses:
                raise ValidationError('Cannot calculate next dose without valid frequency or time interval.')

            # Directly use the medication's next dose calculation
            next_dose_time = self.medication.calculate_next_dose_time()
            self.next_dose_schedule = next_dose_time  # Update with the medication's calculated next dose time
        else:
            if self.medication.status in ['completed', 'stopped', 'deleted']:
                return None  # No next dose for non-active medications
        self.save()

    @transaction.atomic
    def calculate_expected_end_time(self):
        """Calculate the expected end time for all doses to be completed."""
        if self.medication.is_completed():
            self.expected_end_time = timezone.now()
            self.status = 'fulfilled'
            self.medication.status = 'completed'
            self.medication.save()
            self.save()
            return None
        else:
            # calc rem. dose and expected end time
            doses_remaining = self.medication.total_left // self.medication.dosage_per_intake
            time_between_doses = self.medication.calculate_time_between_doses()
            self.expected_end_time = self.start_time + timedelta(hours=(time_between_doses.total_seconds() / 3600 * doses_remaining))
            self.save()
            return self.expected_end_time

    def generate_next_schedule(self):
        """Generate only the next schedule after a dose is fulfilled."""
        next_dose_time = self.calculate_next_dose()
        if next_dose_time:
            Schedule.objects.create(
                medication=self.medication,
                start_time=next_dose_time,
                status='scheduled'
            )

    def mark_as_missed(self):
        """
        Mark the schedule as missed, log it in the MissedDose model, 
        and adjust medication quantity accordingly.
        """
        if self.status == 'missed':
            return  # Avoid marking an already missed dose

        self.status = 'missed'
        self.save()

        try:
            missed_dose = MissedDose.objects.create(medication=self.medication, schedule=self)
            missed_dose.adjust_medication_quantity()
        except Exception as e:
            # Handle the exception, log it, or re-raise it as necessary
            raise ValidationError(f"Failed to mark missed dose: {str(e)}")


    def __str__(self):
        return f'Schedule for {self.medication.user.email}, Medication: {self.medication.name}, Start: {self.start_time}'


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


