from django.core.exceptions import ValidationError
from django.test import TestCase
from django.utils import timezone
from users.models import User
from medications.models import Medication

class MedicationModelTest(TestCase):
    
    def setUp(self):
        self.user = User.objects.create_user(
            email='test@example.com',
            password='password',
            first_name='Test',
            last_name='User'
        )
        self.medication = Medication.objects.create(
            user=self.user,
            name='Test Medication',
            total_quantity=30,
            total_left=30,
            dosage_per_intake=1,
            frequency_per_day=3,
            time_interval=8,
            priority_flag=False,
            priority_lead_time=None,
            last_intake_time=None
        )

    def test_medication_creation(self):
        self.assertEqual(self.medication.name, 'Test Medication')
        self.assertEqual(self.medication.total_left, 30)

    def test_take_dose(self):
        initial_left = self.medication.total_left
        print('before taking dose, initial qty: ', self.medication.total_quantity)
        self.medication.take_dose()
        print('after taking dose')
        self.assertEqual(self.medication.total_left, initial_left - self.medication.dosage_per_intake)
        print('total left: ', self.medication.total_left)

    def test_missed_dose(self):
        self.medication.last_intake_time = timezone.now() - timezone.timedelta(hours=10)  # Simulating a past dose
        print('total_quantity: ', self.medication.total_quantity)
        self.medication.take_dose()
        print('status: ', self.medication.status)
        print('total left: ', self.medication.total_left)
        self.assertEqual(self.medication.status, 'missed')  # Ensure missed status is set
        print('status: ', self.medication.status)

    def test_clean_method_validation(self):
        with self.assertRaises(ValidationError):
            self.medication.priority_flag = True
            self.medication.priority_lead_time = None  # Should raise validation error
            self.medication.clean()

    def test_is_exhausted(self):
        self.medication.total_left = 0
        print(self.medication.total_left)
        self.assertTrue(self.medication.is_exhausted())


from schedules.models import Schedule

class ScheduleModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            email='test@example.com',
            password='password',
            first_name='Test',
            last_name='User'
        )
        self.medication = Medication.objects.create(
            user=self.user,
            name='Test Medication',
            total_quantity=30,
            total_left=30,
            dosage_per_intake=1,
            frequency_per_day=3,
            time_interval=8,
            priority_flag=False
        )
        self.schedule = Schedule.objects.create(
            medication=self.medication,
            start_time=timezone.now()
        )

        print("start time: ", self.schedule.start_time)
        print('Expected end time: ', self.schedule.expected_end_time)
        tbd = self.schedule.calculate_expected_end_time()
        print("TIME BETWEEN DOSES", tbd)

    def test_calculate_next_dose(self):
        self.schedule.calculate_next_dose()
        print(self.schedule.next_dose)
        self.assertIsNotNone(self.schedule.next_dose)

    # def test_handle_end_of_reminder(self):
    #     self.schedule.handle_end_of_reminder()
    #     # Ensure that the status is updated appropriately
    #     print('expected end time: ', self.schedule.expected_end_time)
    #     self.assertEqual(self.schedule.status, 'scheduled')

    def test_generate_recurring_schedules(self):
        self.schedule.generate_recurring_schedules()
        print('after generating recurring schedules')
        self.assertEqual(Schedule.objects.count(), self.medication.total_quantity // self.medication.dosage_per_intake)
        print('total schedules: ', Schedule.objects.all())
