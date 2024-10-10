from datetime import datetime, timedelta
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
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='medications')
    drug_name = models.CharField(max_length=255)  # Drug name
    total_quantity = models.PositiveIntegerField()  # Total quantity of the drug
    total_left = models.PositiveIntegerField(null=True, blank=True)  # Internal use, starts equal to total_quantity
    dosage_per_intake = models.PositiveIntegerField()  # Dosage taken per intake
    frequency_per_day = models.PositiveIntegerField(null=True, blank=True)  # How many times per day
    time_interval = models.PositiveIntegerField(null=True, blank=True)  # Optional, interval between doses in hours
    last_scheduled_time = models.DateTimeField(null=True, blank=True)  # Last time this medication was taken
    priority_flag = models.BooleanField(default=False)  # Is it a priority drug?
    priority_lead_time = models.PositiveIntegerField(null=True, blank=True)  # Gap in minutes for priority drugs
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='active')
    
    # Timestamps for creation and updates
    created_at = models.DateTimeField(auto_now_add=True)  # Auto-set on creation
    updated_at = models.DateTimeField(auto_now=True)  # Auto-updated on modification

    def __str__(self):
        return f"{self.drug_name} for {self.user}"


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
        
        self.clean()
        if not self.pk:  # On creation of a new medication
            self.total_left = self.total_quantity
        
        super().save(*args, **kwargs)


    def calculate_next_time_interval(self, last_scheduled_time):
        """Calculate the next schedule time based on the medication properties."""
        
        # Check if medication is completed
        if self.is_completed():
            self.status = 'completed'
            self.save()
            return None  # No next time if medication is finished

        # Handle priority drug
        if self.priority_flag:
            # For priority drugs, add the time interval to the last scheduled time
            return last_scheduled_time + timedelta(hours=self.time_interval)
        else:
            # For non-priority drugs, calculate based on the provided time interval or frequency
            if self.time_interval:
                # If time_interval is defined, calculate the next schedule based on it
                return last_scheduled_time + timedelta(hours=self.time_interval)
            elif self.frequency_per_day:
                # If frequency is defined, calculate based on frequency
                return last_scheduled_time + timedelta(hours=24 / self.frequency_per_day)

        # If no time interval or frequency is provided, return None
        return None




    
    def update_quantity(self, dose_taken=True):
        """Update the total left quantity and check for completion."""
        
        # If no doses remain, mark medication as completed
        if self.is_completed():
            self.status = 'completed'
            return None
        
        if dose_taken:
            self.total_left -= self.dosage_per_intake
        else:
            self.total_left -= self.dosage_per_intake  # Or some other rule for missed doses
        
        self.save()

    def is_completed(self):
        """Check if the medication is fully consumed."""
        return self.total_left <= 0
