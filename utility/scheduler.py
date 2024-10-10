from datetime import timedelta
from django.utils import timezone
from medications.models import Medication
from schedules.models import Schedule


from datetime import timedelta
from django.utils import timezone


def create_next_schedule(user, last_scheduled_time=None):
    """Create the next schedules for all medications of a user and handle priority logic."""
    
    # Get all medications for the user
    medications = Medication.objects.filter(user=user).order_by('-priority_flag')

    current_time = last_scheduled_time or timezone.now()
    next_schedules = []

    # Determine the lead time from priority medications
    priority_lead_time = 0
    for medication in medications:
        if medication.priority_flag:
            priority_lead_time = medication.priority_lead_time

    # Adjust schedules based on priority lead time
    for medication in medications:
        if medication.priority_flag:
            next_time = medication.calculate_next_time_interval(current_time)
            next_schedules.append((medication, next_time))
        else:
            next_time = medication.calculate_next_time_interval(current_time)
            next_time += timedelta(minutes=priority_lead_time)  # Add lead time for non-priority drugs
            next_schedules.append((medication, next_time))

    # Save the new schedules
    for medication, scheduled_time in next_schedules:
        Schedule.objects.create(
            medication=medication,
            scheduled_time=scheduled_time,
            status='scheduled'
        )
        medication.last_scheduled_time = scheduled_time
        medication.save()

    return next_schedules



# if __name__ == "__main__":
#     create_next_schedule()
