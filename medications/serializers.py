from rest_framework import serializers
from .models import Medication

class MedicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Medication
        fields = [
            'id', 'drug_name', 'total_quantity', 'dosage_per_intake', 
            'frequency_per_day', 'time_interval', 'priority_flag', 
            'priority_lead_time', 'status', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def create(self, validated_data):
        user = self.context['request'].user
        if isinstance(validated_data, list):
            # Handle bulk creation
            medications = [Medication.objects.create(**{**data, 'user': user}) for data in validated_data]
            return medications
        else:
            # Handle single record creation
            return Medication.objects.create(**{**validated_data, 'user': user})
