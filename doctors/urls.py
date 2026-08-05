from django.urls import path
from .views import (
    DoctorListCreateView,
    DoctorDetailView,
    DoctorAvailabilityView,
)
urlpatterns = [
    path(
        "",
        DoctorListCreateView.as_view(),
        name="doctor-list-create",
    ),
    path(
        "<int:pk>/",
        DoctorDetailView.as_view(),
        name="doctor-detail",
    ),
    path(
        "<int:pk>/availability/",
        DoctorAvailabilityView.as_view(),
        name="doctor-availability",
    ),
]