from datetime import timedelta
from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError


from users.models import User

# Create your models here.

class Medication(models.Model):
    """Class for each medication added by user"""
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('completed', 'Completed'),
        ('exhausted', 'Exhausted'),
        ('missed', 'Missed'),
        ('stopped', 'Stopped'),  # Add this new status to represent stopped medications
        ('deleted', 'Deleted'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='medications')
    name = models.CharField(max_length=255)  # Drug name
    total_quantity = models.PositiveIntegerField()  # Total quantity of the drug
    total_left = models.PositiveIntegerField()  # Internal use, starts equal to total_quantity
    dosage_per_intake = models.PositiveIntegerField()  # Dosage taken per intake
    frequency_per_day = models.PositiveIntegerField()  # How many times per day
    time_interval = models.PositiveIntegerField(null=True, blank=True)  # Optional, interval between doses in hours
    last_intake_time = models.DateTimeField(null=True, blank=True)  # Last time this medication was taken
    priority_flag = models.BooleanField(default=False)  # Is it a priority drug?
    priority_lead_time = models.PositiveIntegerField(null=True, blank=True)  # Gap in minutes for priority drugs
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='active')
    
    # Timestamps for creation and updates
    created_at = models.DateTimeField(auto_now_add=True)  # Auto-set on creation
    updated_at = models.DateTimeField(auto_now=True)  # Auto-updated on modification

    def __str__(self):
        return f"{self.name} for {self.user}"


    def clean(self):
        """Custom validation logic."""
        if self.priority_flag and not self.priority_lead_time:
            raise ValidationError({'priority_lead_time': 'Priority lead time must be set for priority medications.'})
        if self.priority_flag and not self.time_interval:
            raise ValidationError({'time_interval': 'Time interval must be set for priority medications.'})
        if not self.priority_flag and not (self.time_interval or self.frequency_per_day):
            raise ValidationError(
                {'time_interval': 'Either time interval or frequency per day must be set for regular medications.'}
            )

    def save(self, *args, **kwargs):
        """Ensure total_left starts with total_quantity."""
        if self.total_quantity <= 0:
            raise ValidationError({'total_quantity': 'Total quantity must be a positive integer.'})

        if self.total_left < 0:
            raise ValidationError({'total_left': 'Total left cannot be negative.'})
        
        self.clean()
        if not self.pk:  # On creation of a new medication
            self.total_left = self.total_quantity
        
        super().save(*args, **kwargs)

    def calculate_time_between_doses(self):
        """Determine time between doses based on priority flag."""
        if self.priority_flag:
            if self.time_interval:
                return timedelta(hours=self.time_interval)
            else:
                raise ValidationError("Time interval is required for priority medications.")
        elif self.frequency_per_day > 0:
            return timedelta(hours=24 // self.frequency_per_day)
        else:
            # Fallback to a default value if nothing is provided, but raise a warning
            return timedelta(hours=8)  # Example fallback to every 8 hours
    
    def take_dose(self):
        """Reduces the total_left based on dosage_per_intake, marks missed doses, and updates last intake time."""
        now = timezone.now()
        time_until_next_dose = self.time_until_next_dose()

        if time_until_next_dose and time_until_next_dose.total_seconds() < 0:  # Dose overdue
            # Mark the missed dose (you may want to log it or notify the user)
            self.status = 'missed'

        if self.total_left > 0:
            self.total_left = max(self.total_left - self.dosage_per_intake, 0)
            self.last_intake_time = now  # Update the last intake time when a dose is taken

            if self.is_exhausted():
                self.status = 'exhausted'
            self.save()
            return True
        
        return False

    def priority_lead_time_check(self):
        """
        Check and enforce the priority lead time for a priority medication.
        Returns:
            lead_time_passed (bool): True if the priority lead time has passed or if not applicable.
            next_allowed_time (datetime): The next time the user can take non-priority medications.
        """
        if self.priority_flag:
            if self.last_intake_time:
                next_allowed_time = self.last_intake_time + timedelta(minutes=self.priority_lead_time)
                if timezone.now() >= next_allowed_time:
                    return True, None  # Lead time has passed
                else:
                    return False, next_allowed_time  # Lead time not yet passed, return the next allowed time
            else:
                return False, None  # If last_intake_time is not set, priority lead time is irrelevant
        return True, None  # No priority lead time to enforce

    def time_until_next_dose(self):
        """Calculates the time left until the next dose, considering priority lead time if applicable."""
        
        # check if meds is exhausted:
        if self.is_exhausted():
            return None
        # If no last intake time is set (first dose)
        if not self.last_intake_time:
            if self.priority_flag:
                # For priority medication, enforce time_interval for the first dose
                if self.time_interval:
                    return timedelta(hours=self.time_interval)
                else:
                    raise ValidationError("Time interval must be set for priority medications.")
            else:
                # For regular medication, use time_interval if available, otherwise calculate based on frequency_per_day
                if self.time_interval:
                    return timedelta(hours=self.time_interval)
                elif self.frequency_per_day > 0:
                    return timedelta(hours=24 // self.frequency_per_day)
                else:
                    raise ValidationError("Either time_interval or frequency_per_day must be provided for regular medications.")
        
        # For subsequent doses, first check priority lead time if applicable
        lead_time_passed, next_allowed_time = self.priority_lead_time_check()
        
        if not lead_time_passed:
            # If lead time hasn't passed, return the time until the next allowed dose
            if next_allowed_time is not None:
                return next_allowed_time - timezone.now()
            else:
                raise ValidationError("Lead time check failed but no next allowed time was provided.")
        
        # For non-priority meds or if lead time passed, calculate time based on last intake time and interval
        if self.time_interval:
            next_dose_time = self.last_intake_time + timedelta(hours=self.time_interval)
        elif self.frequency_per_day > 0:
            next_dose_time = self.last_intake_time + timedelta(hours=24 // self.frequency_per_day)
        else:
            raise ValidationError("Either time_interval or frequency_per_day must be set to calculate next dose.")
        
        return next_dose_time - timezone.now()



    def is_exhausted(self):
        """Check if the medication is fully consumed."""
        return self.total_left <= 0
