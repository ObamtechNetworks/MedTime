import pytest
from datetime import timedelta
from django.utils import timezone
from medications.models import Medication
from schedules.models import Schedule
from tests.factories import MedicationFactory, ScheduleFactory

@pytest.mark.django_db
def test_priority_lead_time_check():
    """Test that priority medications delay other non-priority medications."""
    # Create a priority medication
    priority_medication = MedicationFactory(priority_flag=True, priority_lead_time=30)
    priority_medication.last_intake_time = timezone.now() - timedelta(minutes=20)  # Less than lead time
    priority_medication.save()

    # Assert lead time is not passed yet
    lead_time_passed, next_allowed_time = priority_medication.priority_lead_time_check()
    assert lead_time_passed is False
    assert next_allowed_time is not None

    # After 30 minutes, the lead time should have passed
    priority_medication.last_intake_time = timezone.now() - timedelta(minutes=40)  # More than lead time
    priority_medication.save()

    lead_time_passed, next_allowed_time = priority_medication.priority_lead_time_check()
    assert lead_time_passed is True
    assert next_allowed_time is None

@pytest.mark.django_db
def test_schedule_next_dose_calculation():
    """Test the calculation of next dose considering priority medications."""
    # Create a priority medication and a related schedule
    priority_medication = MedicationFactory(priority_flag=True, time_interval=6)
    schedule = ScheduleFactory(medication=priority_medication, start_time=timezone.now())

    # Test initial next dose time
    schedule.calculate_next_dose()
    assert schedule.next_dose is not None

    # Update medication last intake to simulate dose taken
    priority_medication.last_intake_time = timezone.now() - timedelta(hours=5)
    priority_medication.save()

    # Lead time is passed, so next dose should be calculated
    schedule.calculate_next_dose()
    assert schedule.next_dose > timezone.now()

@pytest.mark.django_db
def test_expected_end_time_calculation():
    """Test the calculation of expected end time for a medication."""
    # Create a medication with a known quantity and dosage
    medication = MedicationFactory(total_quantity=20, dosage_per_intake=2, time_interval=4)
    schedule = ScheduleFactory(medication=medication, start_time=timezone.now())

    # Calculate expected end time
    schedule.calculate_expected_end_time()
    
    # Check if the expected end time is correct based on doses left and interval
    doses_left = medication.total_left // medication.dosage_per_intake
    expected_end_time = schedule.start_time + timedelta(hours=medication.time_interval * doses_left)
    
    assert schedule.expected_end_time == expected_end_time

@pytest.mark.django_db
def test_reminder_cycle_end_handling():
    """Test handling the end of the reminder cycle and updating statuses."""
    # Create a medication that will soon be exhausted
    medication = MedicationFactory(total_quantity=2, dosage_per_intake=2)
    schedule = ScheduleFactory(medication=medication, start_time=timezone.now())

    # Simulate taking the final dose
    medication.take_dose()

    # Assert medication is exhausted
    assert medication.is_exhausted() is True
    print(f'Medication Status: {medication.status}, Total Left: {medication.total_left}')

    # Call calculate_expected_end_time to ensure it’s set before checking the end
    schedule.calculate_expected_end_time()

    # Handle end of reminder
    schedule.handle_end_of_reminder()

    print(f'Schedule Status: {schedule.status}')
    
    # Now assert the status should be 'completed'
    assert schedule.status == 'completed'

