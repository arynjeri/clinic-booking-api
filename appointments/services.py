from datetime import datetime, timedelta

from rest_framework.exceptions import ValidationError

from doctors.models import Doctor
from .models import Appointment, AppointmentStatus

class AppointmentService:

    @staticmethod
    def slot_is_available(
        doctor,
        appointment_date,
        start_time,
        appointment_id=None,
    ):
        appointments = Appointment.objects.filter(
            doctor=doctor,
            appointment_date=appointment_date,
            start_time=start_time,
            status=AppointmentStatus.BOOKED,
        )

        if appointment_id:
            appointments = appointments.exclude(pk=appointment_id)

        return not appointments.exists()

    @staticmethod
    def create_appointment(serializer):
        data = serializer.validated_data

        available = AppointmentService.slot_is_available(
            data["doctor"],
            data["appointment_date"],
            data["start_time"],
        )

        if not available:
            raise ValidationError(
                "This appointment slot is already booked."
            )

        return serializer.save()

    @staticmethod
    def reschedule_appointment(appointment, data):
        doctor = data.get("doctor", appointment.doctor)

        appointment_date = data.get(
            "appointment_date",
            appointment.appointment_date,
        )

        start_time = data.get(
            "start_time",
            appointment.start_time,
        )

        end_time = data.get(
            "end_time",
            appointment.end_time,
        )

        available = AppointmentService.slot_is_available(
            doctor,
            appointment_date,
            start_time,
            appointment.id,
        )

        if not available:
            raise ValidationError(
                "Selected appointment slot is unavailable."
            )

        appointment.doctor = doctor
        appointment.appointment_date = appointment_date
        appointment.start_time = start_time
        appointment.end_time = end_time

        appointment.save()

        return appointment

    @staticmethod
    def generate_available_slots(doctor_id, date):
        doctor = Doctor.objects.get(pk=doctor_id)

        booked_slots = Appointment.objects.filter(
            doctor=doctor,
            appointment_date=date,
            status=AppointmentStatus.BOOKED,
        ).values_list("start_time", flat=True)

        slots = []

        current = datetime.combine(date, doctor.working_start)
        end = datetime.combine(date, doctor.working_end)

        while current < end:
            start = current.time()
            finish = (current + timedelta(minutes=30)).time()

            if start not in booked_slots:
                slots.append(
                    {
                        "start_time": start.strftime("%H:%M"),
                        "end_time": finish.strftime("%H:%M"),
                    }
                )

            current += timedelta(minutes=30)

        return slots