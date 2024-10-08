from django.test import TestCase
from users.models import User
from medications.models import Medication
from schedules.models import Schedule
from datetime import timedelta
from django.utils import timezone

class ScheduleModelTest(TestCase):
    def setUp(self):
        """Setup objects for testing"""
        self.user = User.objects.create(email="testuser@example.com",
                                        first_name="John",
                                        last_name="Doe",
                                        password='securepass',
                                        is_verified=True)
        self.medication = Medication.objects.create(
            user=self.user,
            name="Test Medication",
            total_quantity=10,
            total_left=10,
            dosage_per_intake=1,
            frequency_per_day=2,
            time_interval=12,  # 12-hour interval
            priority_flag=False
        )
        self.schedule = Schedule.objects.create(
            medication=self.medication,
            start_time=timezone.now(),
            status='scheduled',
        )

    def test_calculate_next_dose(self):
        """Test the next dose calculation with print statements"""
        # Calculate the next dose and expected next dose time
        self.schedule.calculate_next_dose()
        expected_next_dose_time = self.schedule.start_time + timedelta(hours=12)  # Based on time_interval

        # Print for debugging
        print(f"Start time: {self.schedule.start_time}")
        print(f"Expected next dose time: {expected_next_dose_time}")
        print(f"Calculated next dose time: {self.schedule.next_dose}")
        
        # Strip microseconds before comparing
        self.assertEqual(
            self.schedule.next_dose.replace(microsecond=0),
            expected_next_dose_time.replace(microsecond=0)
        )

    def test_non_priority_medication_schedule(self):
        """Test the schedule for a non-priority medication"""
        # Create a non-priority medication
        non_priority_medication = Medication.objects.create(
            user=self.user,
            name="Non-Priority Medication",
            total_quantity=20,
            total_left=20,
            dosage_per_intake=1,
            frequency_per_day=2,
            time_interval=12,  # 12-hour interval
            priority_flag=False
        )
        # Create a schedule for the non-priority medication
        schedule = Schedule.objects.create(
            medication=non_priority_medication,
            start_time=timezone.now(),
            status='scheduled',
        )
        
        # Calculate the next dose
        schedule.calculate_next_dose()
        expected_next_dose_time = schedule.start_time + timedelta(hours=12)

        # Print for debugging
        print(f"Start time (Non-priority): {schedule.start_time}")
        print(f"Expected next dose time (Non-priority): {expected_next_dose_time}")
        print(f"Calculated next dose time (Non-priority): {schedule.next_dose}")
        
        # Ensure the calculated next dose time matches the expected time
        self.assertEqual(
            schedule.next_dose.replace(microsecond=0),
            expected_next_dose_time.replace(microsecond=0)
        )
