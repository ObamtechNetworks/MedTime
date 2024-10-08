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
    time_interval = models.PositiveIntegerField()  # Interval between doses in hours
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
        """Add custom validation logic."""
        if self.priority_flag and not self.priority_lead_time:
            raise ValidationError(
                {'priority_lead_time': 'Priority lead time must be set for priority medications.'})

    def save(self, *args, **kwargs):
        """ Custom save method to ensure total_left starts with total_quantity """
        # Custom validation to ensure total_quantity and total_left are valid.
        if self.total_quantity is None or self.total_quantity <= 0:
            raise ValidationError({'total_quantity': 'Total quantity must be a positive integer.'})

        if self.total_left is None or self.total_left < 0:
            raise ValidationError({'total_left': 'Total left cannot be negative.'})
        
        self.clean()  # custom validation for priority flag
        if not self.pk:  # On creation of a new medication
            self.total_left = self.total_quantity
        
        super().save(*args, **kwargs)
    
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
        # Check if it's the first dose (no last intake time set yet)
        if not self.last_intake_time:
            if self.priority_flag:
                # For priority medication, the next dose should be after the lead time + interval (starting from now)
                return timedelta(hours=self.time_interval)  # Since this is the first dose
            else:
                # For non-priority, the next dose is just based on the time_interval from now
                return timedelta(hours=self.time_interval)
        
        # If it's not the first dose, follow the normal logic with lead time checks
        lead_time_passed, next_allowed_time = self.priority_lead_time_check()
        
        if not lead_time_passed:
            if next_allowed_time is not None:
                return next_allowed_time - timezone.now()
            else:
                return None  # No lead time to enforce
        
        # Calculate next regular dose
        next_dose_time = self.last_intake_time + timedelta(hours=self.time_interval)
        return next_dose_time - timezone.now()


    def is_exhausted(self):
        """Check if the medication is fully consumed."""
        return self.total_left <= 0
