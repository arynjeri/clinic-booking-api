from rest_framework import serializers

from .models import Appointment
from .validators import (
    validate_future_date,
    validate_working_hours,
)


class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = "__all__"

    def validate(self, attrs):
        doctor = attrs.get(
            "doctor",
            self.instance.doctor if self.instance else None,
        )

        appointment_date = attrs.get(
            "appointment_date",
            self.instance.appointment_date if self.instance else None,
        )

        start_time = attrs.get(
            "start_time",
            self.instance.start_time if self.instance else None,
        )

        end_time = attrs.get(
            "end_time",
            self.instance.end_time if self.instance else None,
        )

        validate_future_date(appointment_date)

        validate_working_hours(
            doctor,
            start_time,
            end_time,
        )

        return attrs