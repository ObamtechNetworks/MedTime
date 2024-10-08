from datetime import timedelta
import factory
from django.utils import timezone
from medications.models import Medication
from schedules.models import Schedule
from users.models import User

class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    email = factory.Faker('email')
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    is_active = True
    is_verified = True

class MedicationFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Medication

    user = factory.SubFactory(UserFactory)
    name = "Test Medication"
    total_quantity = 20
    total_left = 20
    dosage_per_intake = 2
    frequency_per_day = 2
    time_interval = 6
    priority_flag = False
    last_intake_time = timezone.now()  # Default value for last intake time
    priority_lead_time = factory.LazyAttribute(lambda obj: 30 if obj.priority_flag else None)  # Ensure lead time is set for priority medications
    status = 'active'

class ScheduleFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Schedule

    medication = factory.SubFactory(MedicationFactory)
    start_time = timezone.now()
    status = 'scheduled'
    expected_end_time = factory.LazyAttribute(lambda o: o.start_time + \
                                              timedelta(hours=o.medication.time_interval * (
                                                  o.medication.total_left // o.medication.dosage_per_intake)))