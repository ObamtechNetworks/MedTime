from unittest.mock import patch
from django.test import TestCase
from django.utils import timezone
from datetime import timedelta
from reminders.utils import send_reminder, check_reminder_acknowledgment
from medications.models import Medication
from users.models import User
from schedules.models import Schedule
from reminders.models import Reminder

class ReminderTest(TestCase):
    def setUp(self):
        self.test_user = User.objects.create_user(
        email='obamsings@gmail.com',
        first_name='Test',
        last_name='User',
        password='securepassword123',
        is_verified=True,
        is_active=True
        )
        print(f"Created test user: {self.test_user.full_name} ({self.test_user.email})")

        # Create medication for the existing user
        self.medication = Medication.objects.create(
            user=self.test_user,
            name="Aspirin",
            total_quantity=100,
            total_left=100,
            dosage_per_intake=1,
            frequency_per_day=3,
            time_interval=8,  # every 8 hours
            last_intake_time=None,
            priority_flag=False,
            priority_lead_time=None,
            status='active'
        )
        print(f"Created medication: {self.medication.name} for user: {self.test_user.full_name}")

        # Create a schedule for this medication
        self.schedule = Schedule.objects.create(
            medication=self.medication,
            start_time=timezone.now(),
            status='scheduled',
        )
        print(f"Created schedule for medication: {self.medication.name} with start time: {self.schedule.start_time}")

    def test_send_reminder_and_acknowledge(self):
        # Mock the sending of a reminder
        print("Sending reminder...")
        send_reminder(self.schedule)

        # Fetch the reminder
        reminder = Reminder.objects.get(schedule=self.schedule)
        print(f"Reminder created with ID: {reminder.id}, Scheduled for: {reminder.reminder_time}")

        # Simulate the passing of time
        reminder.reminder_time = timezone.now() - timedelta(minutes=31)
        reminder.save()
        print(f"Simulated reminder time passed. Current time: {timezone.now()}, Reminder time: {reminder.reminder_time}")

        # Check acknowledgment logic
        print("Checking acknowledgment...")
        result = check_reminder_acknowledgment(reminder)

        # Verify the results
        self.assertFalse(result)  # Should be marked as missed
        self.assertTrue(reminder.missed)  # Ensure the reminder is marked as missed
        self.assertEqual(self.medication.total_left, 99)  # Ensure medication count is reduced
        print(f"Test completed. Reminder missed: {reminder.missed}, Medication left: {self.medication.total_left}")

    @patch('reminders.utils.send_mail')  # Adjust the path as needed
    def test_send_reminder_and_acknowledge(self, mock_send_mail):
        # Mock the sending of a reminder
        print("Sending reminder...")
        send_reminder(self.schedule)

        # Assert that send_mail was called
        mock_send_mail.assert_called_once()
        print("Email sent successfully (mocked).")

        # ... (rest of your test)
