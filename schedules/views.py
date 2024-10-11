from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Schedule
from .serializers import ScheduleSerializer

class ScheduleViewSet(viewsets.ModelViewSet):
    queryset = Schedule.objects.all()  # Retrieve all Schedule objects
    serializer_class = ScheduleSerializer  # Use the Schedule serializer
    permission_classes = [IsAuthenticated]  # Ensure the user is authenticated

    def get_queryset(self):
        # Filter schedules based on the logged-in user's medication
        return self.queryset.filter(medication__user=self.request.user)