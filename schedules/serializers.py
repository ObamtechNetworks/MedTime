from rest_framework import serializers
from .models import Schedule

class ScheduleSerializer(serializers.ModelSerializer):
    medication_name = serializers.CharField(source='medication.drug_name', read_only=True)  # Get the name of the medication

    class Meta:
        model = Schedule
        fields = ['id', 'medication_name', 'created_at', 'next_dose_due_at', 'status']  # Only include the relevant fields
        read_only_fields = ['id', 'created_at', 'updated_at']  # Ensure fields are read-only where necessary
