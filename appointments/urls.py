from django.urls import path

from .views import (
    AppointmentListCreateView,
    CancelAppointmentView,
    RescheduleAppointmentView,
)

urlpatterns = [
    path("",
         AppointmentListCreateView.as_view(),
         name="appointment-list-create"),


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