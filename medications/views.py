from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import Medication
from .serializers import MedicationSerializer
from utility.scheduler import create_next_schedule  # Import utility to create schedules

class MedicationViewSet(viewsets.ModelViewSet):
    queryset = Medication.objects.all()
    serializer_class = MedicationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Return medications for the logged-in user
        return self.queryset.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        # Handle the creation of medications
        serializer = self.get_serializer(data=request.data,
                                         many=isinstance(request.data, list))
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        
        # Get start_time from request data, default to None if not provided
        start_time = request.data.get('start_time', None)

        # Trigger schedule creation for the user, with start_time if provided
        create_next_schedule(request.user, last_scheduled_time=start_time)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def perform_create(self, serializer):
        # Save medication and pass the user context
        serializer.save(user=self.request.user)
