from datetime import timedelta, timezone
from schedules.models import MissedDose
from reminders.models import Reminder

def handle_missed_doses():
    # Get the current time and calculate the cutoff for missed reminders (1 hour ago)
    now = timezone.now()
    missed_cutoff = now - timedelta(hours=1)

    # Query reminders that were sent more than 1 hour ago and are not acknowledged
    overdue_reminders = Reminder.objects.filter(
        reminder_time__lte=missed_cutoff,
        acknowledged=False,
        missed=False
    )

    for reminder in overdue_reminders:
        # Mark the reminder as missed
        reminder.mark_as_missed()

        # Create a MissedDose entry and adjust medication quantity
        missed_dose = MissedDose.objects.create(
            medication=reminder.schedule.medication,
            schedule=reminder.schedule
        )
        missed_dose.adjust_medication_quantity()

        # Mark the schedule as missed
        missed_dose.mark_schedule_as_missed()

        # Generate the next schedule for the medication (if applicable)
        reminder.schedule.generate_next_schedule()

if __name__ == "__main__":
    handle_missed_doses()
