from datetime import timezone
from rest_framework import serializers
from .models import Medication
from schedules.models import Schedule


class MedicationSerializer(serializers.ModelSerializer):
    """Serializer for medications"""
    
    # if user sets the time to start the schedule
    start_time = serializers.DateTimeField(required=False)
    class Meta:
        model = Medication
        fields = ['drug_name', 'total_quantity', 'total_left',
                  'dosage_per_intake',
                  'frequency_per_day', 'time_interval',
                  'status', 'priority_flag']

        extra_kwargs = {
            'time_interval': {'required': False},
            'priority_lead_time': {'required': False},
        }

    def create(self, validated_data):
        """Handle validation of data from the request"""
        # Remove start_time from validated_data if it's not present
        start_time = validated_data.pop('start_time', timezone.now())

        # Create the Medication instance without saving it to the database
        medication = Medication(**validated_data)

        # Validate the instance
        medication.full_clean()  # raise a ValidationError if validation fails

        # Now save the instance
        medication.save()

        # Automatically generate the initial schedule for this medication
        self._generate_schedules(medication, start_time)

        return medication
    
    def _generate_schedules(self, medication, start_time):
        """helper method to automatically
        generate schedules for medication"""


    def validate(self, data):
        """Custom validation for priority-related fields"""
        if data.get('priority_flag') and not data.get('priority_lead_time'):
            raise serializers.ValidationError(
                {'priority_lead_time': 'Priority lead time must be set for priority medications.'}
            )
        if data.get('priority_flag') and not data.get('time_interval'):
            raise serializers.ValidationError(
                {'time_interval': 'Time interval must be set for priority medications.'}
            )
        if not data.get('priority_flag') and not (data.get('time_interval') or data.get('frequency_per_day')):
            raise serializers.ValidationError(
                {'time_interval': 'Either time interval or frequency per day must be set for regular medications.'}
            )
        return data
