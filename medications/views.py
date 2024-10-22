from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from .models import Medication
from .serializers import MedicationSerializer
from utility.scheduler import create_next_schedule

# LOGGIN ERRORS
import logging

logger = logging.getLogger(__name__)

class MedicationViewSet(viewsets.ModelViewSet):
    queryset = Medication.objects.all()
    serializer_class = MedicationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        logger.info(f"Received data: {request.data}")  # Log the incoming request data
        
        # Extract medications from the request
        medications_data = request.data.get('medications', [])
        start_time = request.data.get('start_time', None)

        # Check if medications data is a list
        if isinstance(medications_data, list) and medications_data:
            serializer = self.get_serializer(data=medications_data, many=True)
        else:
            return Response({"error": "Medications data is required."}, status=status.HTTP_400_BAD_REQUEST)

        # Validate the serializer
        serializer.is_valid(raise_exception=True)

        # Save the medications
        medications = serializer.save(user=request.user)

        # Create schedules ONLY for the medications created in this request
        create_next_schedule(medications, last_scheduled_time=start_time)

        # Respond with serialized data
        return Response(MedicationSerializer(medications, many=True).data, status=status.HTTP_201_CREATED)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=False, methods=['delete'])
    def delete_all(self, request):
        """Delete all medications for the authenticated user."""
        count, _ = Medication.objects.filter(user=self.request.user).delete()
        return Response(
            {"message": f"Successfully deleted {count} medications."},
            status=status.HTTP_204_NO_CONTENT
)
