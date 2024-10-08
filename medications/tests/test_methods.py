from django.test import TestCase
from django.utils import timezone
from users.models import User
from medications.models import Medication

class MedicationModelTest(TestCase):
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
            dosage_per_intake=2,
            frequency_per_day=3,
            time_interval=8,
            priority_flag=False
        )

    def test_take_dose(self):
        """Test that taking a dose reduces total_left and updates last_intake_time"""
        self.medication.take_dose()
        self.assertEqual(self.medication.total_left, 8)  # Should reduce total_left by 2
        self.assertIsNotNone(self.medication.last_intake_time)  # Should update last_intake_time


class MedicationPriorityTest(TestCase):
    def setUp(self):
        """Setup priority medication for testing"""
        self.user = User.objects.create(email="testuser@example.com", first_name="Jane", last_name="Doe")
        self.priority_medication = Medication.objects.create(
            user=self.user,
            name="Priority Medication",
            total_quantity=10,
            total_left=10,
            dosage_per_intake=2,
            frequency_per_day=3,
            time_interval=8,
            priority_flag=True,
            priority_lead_time=30  # 30 minutes lead time
        )

    def test_priority_lead_time_check(self):
        """Test lead time enforcement for priority medications"""
        self.priority_medication.take_dose()
        lead_time_passed, next_allowed_time = self.priority_medication.priority_lead_time_check()
        self.assertFalse(lead_time_passed)  # Lead time should not have passed immediately after dose
        self.assertIsNotNone(next_allowed_time)  # Next allowed time should be set

    def test_priority_lead_time_check(self):
        """Test lead time enforcement for priority medications, especially for the first dose."""
        self.priority_medication.take_dose()  # Taking the first dose
        lead_time_passed, next_allowed_time = self.priority_medication.priority_lead_time_check()
        
        # For the first dose, lead time should not have passed, and next allowed time should be set based on lead time
        self.assertFalse(lead_time_passed)
        self.assertIsNotNone(next_allowed_time)
        
        # Also check that next dose is calculated correctly
        time_until_next_dose = self.priority_medication.time_until_next_dose()
        self.assertIsNotNone(time_until_next_dose)  # Should have a valid next dose time
    
    def test_priority_lead_time_check(self):
        """Test lead time enforcement for priority medications, especially for the first dose."""
        self.priority_medication.take_dose()  # Taking the first dose
        
        lead_time_passed, next_allowed_time = self.priority_medication.priority_lead_time_check()
        print(f"Lead time passed: {lead_time_passed}, Next allowed time: {next_allowed_time}")
        
        time_until_next_dose = self.priority_medication.time_until_next_dose()
        print(f"Time until next dose: {time_until_next_dose}")
        
        self.assertFalse(lead_time_passed)
        self.assertIsNotNone(next_allowed_time)
        self.assertIsNotNone(time_until_next_dose)
