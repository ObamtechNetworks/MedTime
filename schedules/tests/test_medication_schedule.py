import pytest
from datetime import timedelta
from django.utils import timezone
from medications.models import Medication
from schedules.models import Schedule

@pytest.mark.django_db
def test_priority_lead_time_check(medication_factory):
    """Test that priority medications delay other non-priority medications."""
    # Create a priority medication
    priority_medication = medication_factory(priority_flag=True, priority_lead_time=30)
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
def test_schedule_next_dose_calculation(medication_factory, schedule_factory):
    """Test the calculation of next dose considering priority medications."""
    # Create a priority medication and a related schedule
    priority_medication = medication_factory(priority_flag=True, time_interval=6)
    schedule = schedule_factory(medication=priority_medication, start_time=timezone.now())

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
def test_expected_end_time_calculation(medication_factory, schedule_factory):
    """Test the calculation of expected end time for a medication."""
    # Create a medication with a known quantity and dosage
    medication = medication_factory(total_quantity=20, dosage_per_intake=2, time_interval=4)
    schedule = schedule_factory(medication=medication, start_time=timezone.now())

    # Calculate expected end time
    schedule.calculate_expected_end_time()
    
    # Check if the expected end time is correct based on doses left and interval
    doses_left = medication.total_left // medication.dosage_per_intake
    expected_end_time = schedule.start_time + timedelta(hours=medication.time_interval * doses_left)
    
    assert schedule.expected_end_time == expected_end_time

@pytest.mark.django_db
def test_reminder_cycle_end_handling(medication_factory, schedule_factory):
    """Test handling the end of the reminder cycle and updating statuses."""
    # Create a medication that will soon be exhausted
    medication = medication_factory(total_quantity=2, dosage_per_intake=2)
    schedule = schedule_factory(medication=medication, start_time=timezone.now())

    # Simulate taking the final dose
    medication.take_dose()
    
    # Check if the medication is exhausted and if schedule status is updated
    assert medication.is_exhausted() is True
    schedule.handle_end_of_reminder()
    
    assert schedule.status == 'completed'
    assert medication.status == 'exhausted'
