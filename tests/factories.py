import factory
from django.utils import timezone
from medications.models import Medication
from schedules.models import Schedule
from users.models import User

class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Sequence(lambda n: f"user{n}")

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
    status = 'active'

class ScheduleFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Schedule

    medication = factory.SubFactory(MedicationFactory)
    start_time = timezone.now()
    status = 'scheduled'
