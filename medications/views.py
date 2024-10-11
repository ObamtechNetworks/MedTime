from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from .models import Medication
from .serializers import MedicationSerializer
from utility.scheduler import create_next_schedule

class MedicationViewSet(viewsets.ModelViewSet):
    queryset = Medication.objects.all()
    serializer_class = MedicationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        is_list = isinstance(request.data, list)

        # Use many=True when data is a list
        serializer = self.get_serializer(data=request.data, many=is_list)
        serializer.is_valid(raise_exception=True)
        
        # Save the medication(s)
        medications = serializer.save()

        # Get start_time from the first item if it's a list or directly from data
        start_time = None
        if is_list and request.data:
            start_time = request.data[0].get('start_time', None)
        elif not is_list:
            start_time = request.data.get('start_time', None)

        # Create schedules ONLY for the medications created in this request
        create_next_schedule(medications, last_scheduled_time=start_time)

        # Respond with serialized data (adjust for single vs bulk)
        if is_list:
            return Response(MedicationSerializer(medications, many=True).data, status=status.HTTP_201_CREATED)
        else:
            return Response(MedicationSerializer(medications).data, status=status.HTTP_201_CREATED)


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
