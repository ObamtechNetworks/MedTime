# from datetime import timedelta
# from celery import shared_task
# from django.utils import timezone

# from schedules.models import Schedule
# from .models import Reminder
# from django.core.mail import send_mail  # Adjust as needed for your email setup

# @shared_task
# def send_reminder(reminder_id):
#     # Get the reminder and its scheduled time
#     reminder = Reminder.objects.get(id=reminder_id)
#     scheduled_time = reminder.scheduled_time

#     # Prepare the email content
#     greeting = "Hello! This is your medication reminder."
#     medication_details = []

#     for rem in Reminder.objects.filter(scheduled_time=scheduled_time, acknowledged=False):
#         medication = rem.medication
#         medication_details.append(
#             f"- {medication.drug_name}: {medication.dosage_per_intake} mg, Next dose at {medication.calculate_next_time_interval(scheduled_time).strftime('%Y-%m-%d %H:%M:%S')}"
#         )

#     medication_list = "\n".join(medication_details)

#     acknowledge_url = f"http://your-domain.com/acknowledge/{reminder.id}/"  # URL for acknowledging
#     message = f"{greeting}\n\nHere are your medications due:\n{medication_list}\n\nPlease acknowledge by clicking the following link:\n{acknowledge_url}\n\nThank you!"

#     # Send email reminder
#     send_mail(
#         subject='Medication Reminder',
#         message=message,
#         from_email='your_email@example.com',  # Replace with your sender email
#         recipient_list=[reminder.medication.user.email],
#     )


# @shared_task
# def check_unacknowledged_reminders():
#     one_hour_ago = timezone.now() - timedelta(hours=1)
#     unacknowledged_reminders = Reminder.objects.filter(
#         acknowledged=False,
#         scheduled_time__lt=one_hour_ago
#     )

#     for reminder in unacknowledged_reminders:
#         # Mark the corresponding schedule as missed
#         schedule = Schedule.objects.filter(medication=reminder.medication).filter(
#             scheduled_time=reminder.scheduled_time
#         ).first()
        
#         if schedule:
#             schedule.mark_as_missed()  # Call the method to mark the schedule as missed


# @shared_task
# def check_for_missed_reminders():
#     # Get all unacknowledged reminders that are past due time
#     missed_reminders = Reminder.objects.filter(
#         acknowledged=False,
#         scheduled_time__lt=timezone.now() - timedelta(hours=1)
#     )

#     for reminder in missed_reminders:
#         reminder.mark_as_missed()  # Mark as missed, which will update the medication status