from django.urls import path

from .views import (
    AppointmentCreateView,
    CancelAppointmentView,
    DoctorAvailabilityView,
    RescheduleAppointmentView,
)

urlpatterns = [
    path(
        "",
        AppointmentCreateView.as_view(),
        name="appointment-create",
    ),
    path(
        "<int:pk>/availability/",
        DoctorAvailabilityView.as_view(),
        name="doctor-availability",
    ),

    path(
        "<int:pk>/cancel/",
        CancelAppointmentView.as_view(),
        name="appointment-cancel",
    ),

    path(
        "<int:pk>/reschedule/",
        RescheduleAppointmentView.as_view(),
        name="appointment-reschedule",
    ),
]