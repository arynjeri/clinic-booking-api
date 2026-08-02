from django.contrib import admin
from .models import Appointment

# Register your models here.
@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = (
        "doctor",
        "patient",
        "appointment_date",
        "start_time",
    )

    search_fields = (
        "doctor__name",
        "patient__first_name",
        "patient__last_name",
    )
