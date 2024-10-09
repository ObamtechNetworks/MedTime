from django.urls import path
from .views import (DoseScheduleListCreateAPIView,
                    DoseScheduleRetrieveUpdateDestroyAPIView)


urlpatterns = [
    path('schedules/', DoseScheduleListCreateAPIView.as_view(),
         name='schedule-list-create'),
    path('schedules/<int:pk>/', DoseScheduleRetrieveUpdateDestroyAPIView.as_view(),
         name='medication-detail'),
]
