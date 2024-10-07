import pytest
from django.core.exceptions import ValidationError
from django.utils import timezone
from users.models import User
from models import Medication

@pytest.mark.django_db
class TestMedicationModel:
    @pytest.fixture
    def user(self):
        """Create a verified user for testing."""
        return User.objects.create(
            first_name="Mike",
            last_name="Owen",
            email="mikeowen@gmail.com",
            password="securepassword123",
            is_verified=True  # Assuming you have an is_verified field in the User model
        )

    def test_create_medication_with_valid_data(self, user):
        """Test creating a medication instance with valid data."""
        medication = Medication.objects.create(
            user=user,
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
        assert medication.name == "Aspirin"
        assert medication.total_quantity == 100
        assert medication.total_left == 100
        assert medication.dosage_per_intake == 1
        assert medication.frequency_per_day == 3
        assert medication.time_interval == 8
        assert medication.user == user

    def test_create_medication_without_required_fields(self, user):
        """Test that creating a medication without required fields raises an error."""
        with pytest.raises(ValidationError):
            medication = Medication.objects.create(
                user=user,
                name="",
                total_quantity=None,  # Required field
                total_left=None,      # Required field
                dosage_per_intake=None,  # Required field
                frequency_per_day=None,   # Required field
                time_interval=8,
                last_intake_time=None,
                priority_flag=False,
                priority_lead_time=None,
                status='active'
            )
            medication.full_clean()  # This will trigger field validations

    def test_invalid_total_quantity(self, user):
        """Test that creating a medication with a negative total quantity raises an error."""
        with pytest.raises(ValidationError):
            medication = Medication.objects.create(
                user=user,
                name="Ibuprofen",
                total_quantity=-200,  # Invalid total quantity
                total_left=100,
                dosage_per_intake=1,
                frequency_per_day=3,
                time_interval=8,
                last_intake_time=None,
                priority_flag=False,
                priority_lead_time=None,
                status='active'
            )
            medication.full_clean()

    def test_medication_str_representation(self, user):
        """Test the string representation of the Medication model."""
        medication = Medication.objects.create(
            user=user,
            name="Paracetamol",
            total_quantity=250,
            total_left=250,
            dosage_per_intake=1,
            frequency_per_day=3,
            time_interval=8,
            last_intake_time=None,
            priority_flag=False,
            priority_lead_time=None,
            status='active'
        )
        assert str(medication) == "Paracetamol for Mike Owen"

    def test_update_medication_data(self, user):
        """Test updating an existing medication instance."""
        medication = Medication.objects.update(
            user=user,
            name="Cough Syrup",
            total_quantity=10,
            total_left=10,
            dosage_per_intake=1,
            frequency_per_day=3,
            time_interval=8,
            last_intake_time=None,
            priority_flag=False,
            priority_lead_time=None,
            status='active'
        )
        medication.name = "Updated Cough Syrup"
        medication.save()

        updated_medication = Medication.objects.get(id=medication.id)
        assert updated_medication.name == "Updated Cough Syrup"

    def test_take_dose(self, user):
        """Test taking a dose from the medication."""
        medication = Medication.objects.create(
            user=user,
            name="Vitamin C",
            total_quantity=100,
            total_left=100,
            dosage_per_intake=10,
            frequency_per_day=2,
            time_interval=12,
            last_intake_time=None,
            priority_flag=False,
            priority_lead_time=None,
            status='active'
        )
        
        assert medication.total_left == 100
        assert medication.take_dose()  # Taking a dose should return True
        assert medication.total_left == 90  # Should reduce total_left by dosage_per_intake (10)
        assert medication.last_intake_time is not None  # Should update last intake time
        assert medication.status == 'active'  # Status remains active

        # Test if it updates to exhausted
        medication.total_left = 10  # Set it to the last dose
        medication.take_dose()  # This should exhaust the medication
        assert medication.total_left == 0
        assert medication.status == 'exhausted'  # Status should now be exhausted

    def test_time_until_next_dose(self, user):
        """Test calculating time until the next dose."""
        medication = Medication.objects.create(
            user=user,
            name="Pain Reliever",
            total_quantity=50,
            total_left=50,
            dosage_per_intake=5,
            frequency_per_day=4,
            time_interval=6,  # every 6 hours
            last_intake_time=timezone.now() - timezone.timedelta(hours=6),  # Last taken 6 hours ago
            priority_flag=False,
            priority_lead_time=None,
            status='active'
        )

        time_until_next_dose = medication.time_until_next_dose()
        assert time_until_next_dose is not None
        assert time_until_next_dose.total_seconds() <= 6 * 3600  # Should be less than or equal to 6 hours

    def test_delete_medication(self, user):
        """Test deleting a medication instance."""
        medication = Medication.objects.create(
            user=user,
            name="Fish Oil",
            total_quantity=200,
            total_left=200,
            dosage_per_intake=2,
            frequency_per_day=1,
            time_interval=24,
            last_intake_time=None,
            priority_flag=False,
            priority_lead_time=None,
            status='active'
        )
        medication_id = medication.id
        medication.delete()

        with pytest.raises(Medication.DoesNotExist):
            Medication.objects.get(id=medication_id)
