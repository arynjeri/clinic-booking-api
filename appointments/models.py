from django.db import models
from doctors.models import Doctor
from patients.models import Patient


class AppointmentStatus(models.TextChoices):
    BOOKED = "BOOKED", "Booked"
    CANCELLED = "CANCELLED", "Cancelled"


class Appointment(models.Model):
    doctor = models.ForeignKey(
        Doctor,
        on_delete=models.CASCADE,
        related_name="appointments",
    )

    patient = models.ForeignKey(
        Patient,
        on_delete=models.CASCADE,
        related_name="appointments",
    )

    appointment_date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()

    status = models.CharField(
        max_length=20,
        choices=AppointmentStatus.choices,
        default=AppointmentStatus.BOOKED,
    )

    cancel_reason = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["appointment_date", "start_time"]
        constraints = [
            models.UniqueConstraint(
                fields=["doctor", "appointment_date", "start_time"],
                name="unique_doctor_slot",
            )
        ]

    def __str__(self):
        return (
            f"{self.patient} - {self.doctor} "
            f"({self.appointment_date} {self.start_time})"
        )