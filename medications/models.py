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
    # time_interval = models.PositiveIntegerField(null=True, blank=True)  # Optional, interval between doses in hours
    last_intake_time = models.DateTimeField(null=True, blank=True)  # Last time this medication was taken
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

    def calculate_schedule_time(self, last_scheduled_time):
        """Calculate the next schedule based on the medication properties."""

        # Check if medication is completed
        if self.total_left <= 0:
            self.status = 'completed'
            self.save()
            return None  # No next time if medication is finished

        if self.priority_flag and self.priority_lead_time:
            next_time = last_scheduled_time + timedelta(minutes=self.priority_lead_time)
        elif self.time_interval:
            next_time = last_scheduled_time + timedelta(hours=self.time_interval)
        else:
            # Calculate based on frequency per day
            next_time = last_scheduled_time + timedelta(hours=24 // self.frequency_per_day)
        return next_time

    
    def update_quantity(self, dose_taken=True):
        """Update the total left quantity and check for completion."""
        
        # If no doses remain, mark medication as completed
        if self.is_completed():
            self.status = 'completed'
            return None
        else:
            self.total_left -= 1  # Decrement quantity for both taken and missed doses
        
        self.save()

    def is_completed(self):
        """Check if the medication is fully consumed."""
        return self.total_left <= 0
