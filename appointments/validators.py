from datetime import datetime
from rest_framework.exceptions import ValidationError


def validate_future_date(appointment_date):
    if appointment_date < datetime.today().date():
        raise ValidationError(
            "Appointments cannot be booked in the past."
        )

def validate_working_hours(doctor, start_time, end_time):

    if start_time < doctor.working_start:
        raise ValidationError(
            "Appointment is before doctor's working hours."
        )

    if end_time > doctor.working_end:
        raise ValidationError(
            "Appointment is after doctor's working hours."
        )