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
        user = self.context['request'].user  # Assign current logged-in user
        medications = []
        if isinstance(validated_data, list):
            for data in validated_data:
                data['user'] = user  # Set user for each medication
                medication = Medication.objects.create(**data)
                medications.append(medication)
        else:
            validated_data['user'] = user
            medication = Medication.objects.create(**validated_data)
            medications.append(medication)
        return medications  # Return created instances
