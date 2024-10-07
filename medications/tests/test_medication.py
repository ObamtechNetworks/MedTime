from django.test import TestCase
from .models import Medication
from users.models import User


class MedicationModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(username="testuser")
        self.medication = Medication.objects.create(
            user=self.user,
            name="Test Drug",
            total_quantity=20,
            dosage_per_intake=2,
            frequency_per_day=3,
            time_interval=8,
        )

    def test_take_dose_reduces_total_left(self):
        self.assertEqual(self.medication.total_left, 20)
        self.medication.take_dose()
        self.assertEqual(self.medication.total_left, 18)

    def test_medication_exhausted(self):
        self.medication.total_left = 2
        self.medication.take_dose()
        self.assertEqual(self.medication.total_left, 0)
        self.assertTrue(self.medication.is_exhausted())
