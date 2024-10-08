from datetime import timedelta
from django.utils import timezone
from django.core.mail import send_mail
from .models import Reminder
from celery import shared_task
from schedules.models import Schedule

def send_reminder(schedule):
    # Create a reminder
    reminder = Reminder.objects.create(schedule=schedule, user=schedule.medication.user)

    # Send the email (or other notifications)
    send_mail(
        subject="Medication Reminder",
        message=f"Dear {schedule.medication.user.first_name}, it's time to take your medication: {schedule.medication.name}.",
        from_email="reminder@medtime.com",
        recipient_list=[schedule.medication.user.email],
    )

def check_reminder_acknowledgment(reminder, time_window_minutes=30):
    """Check if the reminder is acknowledged within a time window."""
    if reminder.acknowledged:
        return True
    elif timezone.now() > reminder.reminder_time + timedelta(minutes=time_window_minutes):
        # Mark as missed if acknowledgment time passed
        reminder.mark_as_missed()
        
        # Use the schedule and medication variables to adjust tracking
        schedule = reminder.schedule
        medication = schedule.medication
        
        # Here you would adjust the medication and schedule accordingly
        # For example:
        medication.total_left -= medication.dosage_per_intake  # Reduce the total_left of the medication
        medication.save()

        # Optionally, mark the schedule as missed or update status
        schedule.status = 'missed'  # Assuming you have a 'missed' status
        schedule.save()

        return False
    return None  # Still within the window



@shared_task
def check_and_send_reminders():
    schedules = Schedule.objects.filter(status='scheduled')
    for schedule in schedules:
        if timezone.now() >= schedule.start_time:
            send_reminder(schedule)

@shared_task
def check_missed_reminders():
    reminders = Reminder.objects.filter(acknowledged=False, missed=False)
    for reminder in reminders:
        check_reminder_acknowledgment(reminder)