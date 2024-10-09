from django.urls import path
from .views import MedicationListCreateAPIView, MedicationRetrieveUpdateDestroyAPIView


urlpatterns = [
    path('medications/', MedicationListCreateAPIView.as_view(),
         name='medication-list-create'),
    path('medications/<int:pk>/', MedicationRetrieveUpdateDestroyAPIView.as_view(),
         name='medication-detail'),
]
