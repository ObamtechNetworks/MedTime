from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Medication
from .serializers import MedicationSerializer

# Create your views here.


class MedicationBulkCreateView(APIView):
    """Handle bulk creation of medications"""
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = request.user
        medications_data = request.data.get('medications', [])  # Expecting a list of medications

        if not medications_data:
            return Response({'detail': 'No medication data provided'}, status=status.HTTP_400_BAD_REQUEST)
        
        errors = []
        created_medications = []

        for medication_data in medications_data:
            medication_data['user'] = user.id  # Assuming Medication model has a user ForeignKey
            
            serializer = MedicationSerializer(data=medication_data)
            if serializer.is_valid():
                medication = serializer.save()
                created_medications.append(medication)
            else:
                errors.append(serializer.errors)

        if errors:
            return Response({'created_medications': created_medications, 'errors': errors}, status=status.HTTP_207_MULTI_STATUS)

        return Response({'created_medications': created_medications}, status=status.HTTP_201_CREATED)

class MedicationListCreateAPIView(generics.ListCreateAPIView):
    """View to handle get and post request"""
    # Firstly ensure that user is logged in before accessing this endpoint
    permission_classes = [IsAuthenticated]

    # if user is authenticated, get all the medications for that user
    serializer_class = MedicationSerializer  # specify serializer class
    queryset = Medication.objects.all()

    def perform_create(self, serializer):
        """create medication for the given user"""
        serializer.save(user=self.request.user)  # Associate the medication with the authenticated user
    

class MedicationRetrieveUpdateDestroyAPIView(
    generics.RetrieveUpdateDestroyAPIView):
    """To handle a retrieval of a specific medication by id
    can GET, PUT, DELETE
    """
    # ensure user is authenticated
    permission_classes = [IsAuthenticated]

    # specify the serializer class
    serializer_class = MedicationSerializer

    def get_queryset(self):
        # Fetch only the medications that belong to the authenticated user
        return Medication.objects.filter(user=self.request.user)