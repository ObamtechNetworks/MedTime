from django.db import models
from django.utils import timezone

from users.models import User

# Create your models here.

class Medication(models.Model):
    """Class for each medication added by user"""
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('completed', 'Completed'),
        ('exhausted', 'Exhausted'),
        ('missed', 'Missed'),
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

    def save(self, *args, **kwargs):
        """ Custom save method to ensure total_left starts with total_quantity """
        if not self.pk:  # On creation of a new medication
            self.total_left = self.total_quantity
        super().save(*args, **kwargs)
    
    def is_exhausted(self):
        """Check if the medication is fully consumed."""
        return self.total_left <= 0

    def take_dose(self):
        """Reduces the total_left based on dosage_per_intake and updates last intake time."""
        if self.total_left > 0:
            self.total_left = max(self.total_left - self.dosage_per_intake, 0)
            self.last_intake_time = timezone.now()  # Update last intake time when a dose is taken
            if self.is_exhausted():
                self.status = 'exhausted'
            self.save()
            return True
        return False

    def time_until_next_dose(self):
        """Calculates the time left until the next dose should be taken."""
        if self.last_intake_time:
            next_dose_time = self.last_intake_time + timezone.timedelta(hours=self.time_interval)
            return next_dose_time - timezone.now()
        return None
