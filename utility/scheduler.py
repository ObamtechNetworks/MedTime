# scheduler.py from utilities.scheduler import create_next_schedule
from datetime import timedelta
from django.utils import timezone
from medications.models import Medication
# from reminders.models import Reminder
# from reminders.tasks import send_reminder
from schedules.models import Schedule


from datetime import timedelta
from django.utils import timezone


def create_next_schedule(medications, last_scheduled_time=None):
    """Create the next schedules for the provided medications, handling priority and lead time logic."""
    
    current_time = timezone.now()
    next_schedules = []

    # Ensure medications is always a list
    if not isinstance(medications, list):
        medications = [medications]

    # Determine lead time from priority medications
    priority_lead_time = 0
    for medication in medications:
        if medication.priority_flag:
            priority_lead_time = medication.priority_lead_time

    # Adjust schedules based on priority lead time and calculate next dose due time
    for medication in medications:
        next_time = medication.calculate_next_time_interval(last_scheduled_time or current_time)
        if not medication.priority_flag and priority_lead_time:
            next_time += timedelta(minutes=priority_lead_time)
        next_schedules.append((medication, next_time))

    # Save the new schedules
    for medication, next_dose_due_at in next_schedules:
        if next_dose_due_at:  # Avoid scheduling for completed medications
            Schedule.objects.create(
                medication=medication,
                next_dose_due_at=next_dose_due_at
            )

    # Create a reminder for the user
    # reminder_instance = Reminder.objects.create(
    #     medication=medication,
    #     scheduled_time=scheduled_time - timedelta(minutes=5)  # Schedule reminder 5 minutes earlier
    # )

    # # Schedule the reminder email to be sent
    # send_reminder.apply_async((reminder_instance.id,), eta=reminder_instance.scheduled_time)

    return next_schedules
