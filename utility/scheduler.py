# scheduler.py from utilities.scheduler import create_next_schedule
from datetime import timedelta
from django.utils import timezone
from medications.models import Medication
# from reminders.models import Reminder
# from reminders.tasks import send_reminder
from schedules.models import Schedule


from datetime import timedelta
from django.utils import timezone
from dateutil import parser


def initial_schedule(medications, start_time):
    """Schedule the first doses based on the user's specified start time."""
    current_time = timezone.now()
    next_schedules = []
    
    # Ensure start_time is a datetime object
    if isinstance(start_time, str):
        start_time = parser.isoparse(start_time)

    # Determine lead time from priority medications
    priority_lead_time = 0
    for medication in medications:
        if medication.priority_flag:
            priority_lead_time = medication.priority_lead_time

    # Schedule the first dose for each medication
    for medication in medications:
        if medication.priority_flag:
            next_time = start_time  # Priority drug starts at user-defined time
        else:
            next_time = start_time + timedelta(minutes=priority_lead_time)  # Non-priority drug

        # Avoid scheduling for completed medications
        if not medication.is_completed():
            next_schedules.append((medication, next_time))

    # Save the initial schedules
    for medication, next_dose_due_at in next_schedules:
        Schedule.objects.create(
            medication=medication,
            next_dose_due_at=next_dose_due_at
        )
    
    return next_schedules


# to be used for triggering next schedules creations
def create_next_schedule(medications):
    """Calculate and create next schedules for the provided medications."""
    current_time = timezone.now()
    next_schedules = []

    for medication in medications:
        # Fetch the last schedule
        last_schedule = Schedule.objects.filter(medication=medication).order_by('-next_dose_due_at').first()
        if last_schedule:
            last_dose_time = last_schedule.next_dose_due_at
        else:
            continue  # No previous schedule found, skip this medication

        # Calculate the next dose time based on medication properties
        next_time = medication.calculate_next_time_interval(last_dose_time)
        
        # Avoid scheduling for completed medications
        if next_time and not medication.is_completed():
            next_schedules.append((medication, next_time))

    # Save the new schedules
    for medication, next_dose_due_at in next_schedules:
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
