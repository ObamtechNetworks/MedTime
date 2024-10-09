from rest_framework import generics
from .models import Schedule
from .serializers import DoseScheduleSerializer
from rest_framework.permissions import IsAuthenticated


class DoseScheduleListCreateAPIView(generics.ListCreateAPIView):
    """Handle get and post request """
    # ensure user is authenticated
    permission_classes = [IsAuthenticated]

    # if user is authenticated, get all schedule for that user
    serializer_class = DoseScheduleSerializer
    queryset = Schedule.objects.all()

    def perform_create(self, serializer):
        """create dose schedule for the given user"""
        serializer.save(user=self.request.user)  # associate schedule with user
    

class DoseScheduleRetrieveUpdateDestroyAPIView(
    generics.RetrieveUpdateDestroyAPIView):
    """To handle a retrieval of a specific medication dose by id
    can GET, PUT, DELETE
    """
    # ensure user is authenticated
    permission_classes = [IsAuthenticated]

    # specify the serializer class
    serializer_class = DoseScheduleSerializer

    def get_queryset(self):
        # Fetch only the medications that belong to the authenticated user
        return Schedule.objects.filter(user=self.request.user)
