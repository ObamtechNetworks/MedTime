from django.utils import timezone
from medications.models import Medication
from schedules.models import Schedule


def generate_schedules():
    # Get current time
    now = timezone.now()

    # Query for all active medications
    active_medications = Medication.objects.filter(status='active')

    for medication in active_medications:
        # Check if medication is already completed
        if medication.is_completed():
            continue

        # Calculate the next dose time
        next_dose_time = medication.calculate_next_dose_time()

        # Check if a schedule for this next dose already exists
        existing_schedule = Schedule.objects.filter(
            medication=medication,
            start_time=next_dose_time
        ).first()

        if not existing_schedule:
            # Create the next dose schedule
            Schedule.objects.create(
                medication=medication,
                start_time=next_dose_time,
                status='scheduled'
            )

if __name__ == "__main__":
    generate_schedules()
