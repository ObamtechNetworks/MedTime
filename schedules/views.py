from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Schedule
from .serializers import ScheduleSerializer

class ScheduleViewSet(viewsets.ModelViewSet):
    queryset = Schedule.objects.all()  # Base queryset without filters
    serializer_class = ScheduleSerializer  # Use the Schedule serializer
    permission_classes = [IsAuthenticated]  # Ensure the user is authenticated

    def get_queryset(self):
        # Optimize the query by fetching related medication in one query using select_related
        return Schedule.objects.select_related('medication').filter(medication__user=self.request.user)
