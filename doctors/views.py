from datetime import datetime

from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics
from .models import Doctor
from .serializers import DoctorSerializer

from appointments.services import AppointmentService

class DoctorListCreateView(generics.ListCreateAPIView):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer


class DoctorDetailView(generics.RetrieveAPIView):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer

class DoctorAvailabilityView(APIView):

    def get(self, request, pk):
        date_str = request.query_params.get("date")

        if not date_str:
            raise ValidationError(
                {"date": "This query parameter is required."}
            )

        try:
            appointment_date = datetime.strptime(
                date_str,
                "%Y-%m-%d"
            ).date()
        except ValueError:
            raise ValidationError(
                {"date": "Use YYYY-MM-DD format."}
            )

        slots = AppointmentService.generate_available_slots(
            pk,
            appointment_date,
        )

        return Response(slots)