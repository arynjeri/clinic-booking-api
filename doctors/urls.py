from django.urls import path
from appointments.views import DoctorAvailabilityView

urlpatterns = [
    path(
        "<int:pk>/availability/",
        DoctorAvailabilityView.as_view(),
        name="doctor-availability",
    ),
]