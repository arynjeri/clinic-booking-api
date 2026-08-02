from django.contrib import admin
from .models import Patient

# Register your models here.
@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = (
        "first_name",
        "last_name",
        "email",
        "phone",
    )

    search_fields = (
        "first_name",
        "last_name",
        "email",
    )
