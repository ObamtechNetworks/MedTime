from django.test import TestCase
from django.utils import timezone
from datetime import timedelta
from users.models import User
from medications.models import Medication
from schedules.models import Schedule
from utility.scheduler import create_next_schedule  # Adjust import based on your structure

class MedicationSchedulingTestCase(TestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(
            first_name='John',
            last_name='Doe',
            email='john.doe@example.com',
            password='testpassword',
            is_verified=True
        )

        # Create medications
        self.medication_a = Medication.objects.create(
            user=self.user,
            drug_name='Drug A',
            total_quantity=2,
            total_left=2,
            dosage_per_intake=1,
            frequency_per_day=None,
            time_interval=8,  # Hours
            priority_flag=True,
            priority_lead_time=30,  # Minutes
            status='active'
        )

        self.medication_b = Medication.objects.create(
            user=self.user,
            drug_name='Drug B',
            total_quantity=4,
            total_left=4,
            dosage_per_intake=1,
            frequency_per_day=None,
            time_interval=12,  # Hours
            priority_flag=False,
            priority_lead_time=None,
            status='active'
        )

    def test_medication_scheduling_with_priority(self):
        """Test that priority medications are scheduled correctly with lead time."""
        last_scheduled_time = timezone.now().replace(hour=18, minute=0, second=0, microsecond=0)

        # Schedule all medications
        create_next_schedule(self.user, last_scheduled_time)

        # Verify priority drug (Medication A)
        next_schedule_a = Schedule.objects.filter(medication=self.medication_a).latest('scheduled_time')
        expected_time_a = last_scheduled_time + timedelta(hours=8)  # 6 PM + 8 hours = 2 AM
        self.assertEqual(next_schedule_a.scheduled_time, expected_time_a)

        # Verify non-priority drug (Medication B)
        next_schedule_b = Schedule.objects.filter(medication=self.medication_b).latest('scheduled_time')
        expected_time_b = last_scheduled_time + timedelta(hours=12, minutes=30)  # 6 PM + 12 hours + 30 minutes = 6:30 AM
        self.assertEqual(next_schedule_b.scheduled_time, expected_time_b)

        # Debug output
        print(f"Expected Priority Drug A time: {expected_time_a.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Actual Priority Drug A time: {next_schedule_a.scheduled_time.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Expected Non-Priority Drug B time: {expected_time_b.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Actual Non-Priority Drug B time: {next_schedule_b.scheduled_time.strftime('%Y-%m-%d %H:%M:%S')}")

    def test_medication_scheduling_output(self):
        """Test output of scheduled medication times."""
        last_scheduled_time = timezone.now().replace(hour=18, minute=0, second=0, microsecond=0)

        # Schedule all medications
        create_next_schedule(self.user, last_scheduled_time)

        # Verify Medication A (priority)
        next_time_a = Schedule.objects.filter(medication=self.medication_a).latest('scheduled_time').scheduled_time
        
        # Verify Medication B (non-priority)
        next_time_b = Schedule.objects.filter(medication=self.medication_b).latest('scheduled_time').scheduled_time

        # Debug output
        print(f"Drug A is scheduled for: {next_time_a.strftime('%I:%M %p')}")
        print(f"Drug B is scheduled for: {next_time_b.strftime('%I:%M %p')}")
        print("All scheduled times for Drug B:", Schedule.objects.filter(medication=self.medication_b).values_list('scheduled_time', flat=True))

        # Test outputs
        self.assertEqual(next_time_a.strftime('%I:%M %p'), "02:00 AM")  # Priority drug
        self.assertEqual(next_time_b.strftime('%I:%M %p'), "06:30 AM")  # Expected time for Drug B

    def test_lead_time_and_regular_timing_difference(self):
        """Compare schedule timings between priority and non-priority medications."""
        last_scheduled_time = timezone.now().replace(hour=18, minute=0, second=0, microsecond=0)

        # Schedule next doses for both priority and non-priority medications
        create_next_schedule(self.user, last_scheduled_time)

        # Retrieve the schedules from the database
        priority_schedule = Schedule.objects.filter(medication=self.medication_a).latest('scheduled_time')
        non_priority_schedule = Schedule.objects.filter(medication=self.medication_b).latest('scheduled_time')

        # Assert that the priority drug's schedule is earlier than the non-priority drug's
        self.assertTrue(priority_schedule.scheduled_time < non_priority_schedule.scheduled_time)

        # Debug output
        print(f"Priority drug next dose at: {priority_schedule.scheduled_time.strftime('%I:%M %p')}")
        print(f"Non-priority drug next dose at: {non_priority_schedule.scheduled_time.strftime('%I:%M %p')}")

    def test_medication_scheduling_correct_timing(self):
        """Test that the timings for scheduled medications are correct based on the last scheduled time."""
        last_scheduled_time = timezone.now().replace(hour=18, minute=0, second=0, microsecond=0)

        # Schedule all medications
        create_next_schedule(self.user, last_scheduled_time)

        # Verify priority drug (Medication A)
        next_schedule_a = Schedule.objects.filter(medication=self.medication_a).latest('scheduled_time')
        expected_time_a = last_scheduled_time + timedelta(hours=8)  # 6 PM + 8 hours = 2 AM next day
        self.assertEqual(next_schedule_a.scheduled_time, expected_time_a)

        # Verify non-priority drug (Medication B)
        next_schedule_b = Schedule.objects.filter(medication=self.medication_b).latest('scheduled_time')

        # Medication B should be scheduled as follows:
        expected_time_b = last_scheduled_time + timedelta(hours=12) + timedelta(minutes=30)  # 6 AM + 30 minutes
        self.assertEqual(next_schedule_b.scheduled_time, expected_time_b)

        # Debug output
        print("After first scheduling:")
        print(f"Next scheduled time for Drug A: {next_schedule_a.scheduled_time}")
        print(f"Next scheduled time for Drug B: {next_schedule_b.scheduled_time}")
