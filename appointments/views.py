from django.shortcuts import render
from jsonschema import ValidationError
from rest_framework.views import APIView
from rest_framework.response import Response, responses
from rest_framework import status
from rest_framework.exceptions import ValidationError

from .models import Appointment
from .serializers import AppointmentSerializer
from .services import AppointmentService
from django.shortcuts import get_object_or_404
from .models import AppointmentStatus
from datetime import datetime
from drf_spectacular.utils import extend_schema

@extend_schema(
    request=AppointmentSerializer,
    responses=AppointmentSerializer,
)
# Create your views here.
class AppointmentCreateView(APIView):

    def post(self, request):

        serializer = AppointmentSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        appointment = AppointmentService.create_appointment(serializer)

        return Response(
            AppointmentSerializer(appointment).data,
            status=status.HTTP_201_CREATED
@extend_schema(
    request=None,
    responses={200: None},
)        )
class CancelAppointmentView(APIView):

    def patch(self, request, pk):

        appointment = get_object_or_404(Appointment, pk=pk)

        if appointment.status == AppointmentStatus.CANCELLED:
            return Response(
                {"detail": "Appointment is already cancelled."},
                status=status.HTTP_400_BAD_REQUEST
            )

        appointment.status = AppointmentStatus.CANCELLED

        appointment.cancel_reason = request.data.get(
            "cancel_reason",
            ""
        )

        appointment.save()

        return Response(
            {"detail": "Appointment cancelled successfully."},
            status=status.HTTP_200_OK
        )
@extend_schema(
    request=AppointmentSerializer,
    responses=AppointmentSerializer
)
class RescheduleAppointmentView(APIView):

    def patch(self, request, pk):

        appointment = get_object_or_404(Appointment, pk=pk)

        serializer = AppointmentSerializer(
            appointment,
            data=request.data,
            partial=True
        )

        serializer.is_valid(raise_exception=True)

        AppointmentService.reschedule_appointment(
            appointment,
            serializer.validated_data
        )

        return Response(
            AppointmentSerializer(appointment).data
        )
@extend_schema(
    responses={
        200: {
            "type": "array"
        }
    }
)
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
