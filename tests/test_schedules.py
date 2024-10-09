from django.test import TestCase
from django.utils import timezone
from datetime import timedelta
from users.models import User
from medications.models import Medication
from schedules.models import Schedule, MissedDose


class MedicationScheduleTestCase(TestCase):

    def setUp(self):
        """Create test users and medications."""
        self.user = User.objects.create_user(
            email='user1@example.com',
            first_name="john",
            last_name="doe",
            password='password123',
            is_verified=True
        )

        # Priority medication (e.g., taken every 8 hours, total 10 doses)
        self.priority_medication = Medication.objects.create(
            user=self.user,
            name='PriorityMed',
            total_quantity=20,
            dosage_per_intake=2,
            frequency_per_day=3,  # every 8 hours
            priority_flag=True,
            priority_lead_time=30,
            time_interval=8,
        )

        # Non-priority medication (e.g., taken every 12 hours, total 5 doses)
        self.non_priority_medication = Medication.objects.create(
            user=self.user,
            name='NonPriorityMed',
            total_quantity=10,
            dosage_per_intake=2,
            frequency_per_day=2,  # every 12 hours
            priority_flag=False,
            time_interval=12,
        )

    def test_schedule_generation(self):
        """Test schedule generation for both priority and non-priority medications."""
        print("\n[INFO] Generating schedules for Priority and Non-Priority Medications...\n")

        # Create an initial schedule for the priority medication
        initial_priority_schedule = Schedule.objects.create(
            medication=self.priority_medication,
            start_time=timezone.now(),
            status='scheduled'
        )

        # Priority medication schedule generation (instance method)
        priority_schedules = initial_priority_schedule.generate_recurring_schedules()
        print(f"Generated {len(priority_schedules)} schedules for priority medication.")

        # Create an initial schedule for the non-priority medication
        initial_non_priority_schedule = Schedule.objects.create(
            medication=self.non_priority_medication,
            start_time=timezone.now(),
            status='scheduled'
        )

        # Non-priority medication schedule generation (instance method)
        non_priority_schedules = initial_non_priority_schedule.generate_recurring_schedules()
        print(f"Generated {len(non_priority_schedules)} schedules for non-priority medication.")

        # Check that the schedules were created correctly
        self.assertEqual(len(priority_schedules), 10)  # 20 pills, 2 per dose = 10 doses
        self.assertEqual(len(non_priority_schedules), 5)  # 10 pills, 2 per dose = 5 doses

    def test_schedule_fulfillment(self):
        """Simulate schedule reaching its time and being fulfilled."""
        # Create an initial schedule for the priority medication
        initial_priority_schedule = Schedule.objects.create(
            medication=self.priority_medication,
            start_time=timezone.now(),
            status='scheduled'
        )

        # Generate schedules
        initial_priority_schedule.generate_recurring_schedules()

        # Fast forward to the first dose time of the priority medication
        priority_schedule = Schedule.objects.filter(medication=self.priority_medication).first()
        print(f"\n[INFO] Priority Medication Schedule (First Dose): {priority_schedule.start_time}")

        # Simulate taking the dose
        print("[INFO] Fulfilling the priority medication dose...")
        priority_schedule.fulfill_schedule()

        # Verify schedule status and next dose calculation
        self.assertEqual(priority_schedule.status, 'fulfilled')
        print(f"[RESULT] Priority Medication Schedule Status: {priority_schedule.status}")
        print(f"[RESULT] Medication Total Left: {self.priority_medication.total_left}")

        # Check if a new schedule is created
        next_priority_schedule = Schedule.objects.filter(medication=self.priority_medication, status='scheduled').first()
        print(f"[INFO] Next Priority Medication Dose Scheduled at: {next_priority_schedule.start_time}")
        self.assertIsNotNone(next_priority_schedule)

    def test_missed_dose(self):
        """Test missed dose handling and medication adjustment."""
        # Create an initial schedule for the non-priority medication
        initial_non_priority_schedule = Schedule.objects.create(
            medication=self.non_priority_medication,
            start_time=timezone.now(),
            status='scheduled'
        )

        # Generate schedules
        initial_non_priority_schedule.generate_recurring_schedules()

        # Fast forward to simulate missing a dose (e.g., no acknowledgment within the time window)
        missed_schedule = Schedule.objects.filter(medication=self.non_priority_medication).first()

        print(f"\n[INFO] Simulating missed dose for Non-Priority Medication at: {missed_schedule.start_time}")
        
        # Simulate missing the dose
        missed_schedule.mark_as_missed()

        # Verify that the schedule was marked as missed and the total medication was adjusted
        missed_schedule.refresh_from_db()
        self.assertEqual(missed_schedule.status, 'missed')
        print(f"[RESULT] Non-Priority Medication Schedule Status: {missed_schedule.status}")
        print(f"[RESULT] Medication Total Left after Miss: {self.non_priority_medication.total_left}")

    def test_priority_medication_flow(self):
        """Simulate a complete flow for a priority medication."""
        print("\n[INFO] Testing full priority medication flow...\n")
        initial_priority_schedule = Schedule.objects.create(
            medication=self.priority_medication,
            start_time=timezone.now(),
            status='scheduled'
        )
        initial_priority_schedule.generate_recurring_schedules()

        for schedule in Schedule.objects.filter(medication=self.priority_medication):
            print(f"[INFO] Fulfilling priority dose scheduled at {schedule.start_time}")
            schedule.fulfill_schedule()

            # Check if the schedule status is updated
            self.assertEqual(schedule.status, 'fulfilled')
            print(f"[RESULT] Schedule Status: {schedule.status}")
            print(f"[RESULT] Medication Total Left: {self.priority_medication.total_left}")

            # Check next dose schedule
            next_schedule = Schedule.objects.filter(medication=self.priority_medication, status='scheduled').first()
            if next_schedule:
                print(f"[INFO] Next dose scheduled at: {next_schedule.start_time}")
            else:
                print("[INFO] No further doses scheduled (end of medication).")


if __name__ == '__main__':
    TestCase.main()
