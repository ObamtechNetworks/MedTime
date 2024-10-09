from rest_framework import serializers
from .models import Schedule

class DoseScheduleSerializer(serializers.ModelSerializer):
    """Serializer for the dose schedule model"""
    class Meta:
        model = Schedule
        fields = '__all__'