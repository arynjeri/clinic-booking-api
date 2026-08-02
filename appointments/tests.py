from datetime import date, time, timedelta

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from doctors.models import Doctor
from patients.models import Patient
from .models import Appointment, AppointmentStatus


class AppointmentTests(APITestCase):

    def setUp(self):
        self.doctor = Doctor.objects.create(
            name="Dr Jane Smith",
            specialization="General Medicine",
            working_start=time(9, 0),
            working_end=time(17, 0),
        )

        self.patient = Patient.objects.create(
            first_name="Mary",
            last_name="Mburu",
            email="mary@test.com",
            phone="0797000000",
        )

        self.create_url = reverse("appointment-create")
    
    def test_create_appointment(self):
        payload = {
            "doctor": self.doctor.id,
            "patient": self.patient.id,
            "appointment_date": str(date.today() + timedelta(days=1)),
            "start_time": "10:00",
            "end_time": "10:30",
        }

        response = self.client.post(
            self.create_url,
            payload,
            format="json"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )

        self.assertEqual(
            Appointment.objects.count(),
            1
        )
    def test_cannot_book_in_past(self):

        payload = {
            "doctor": self.doctor.id,
            "patient": self.patient.id,
            "appointment_date": str(date.today() - timedelta(days=1)),
            "start_time": "10:00",
            "end_time": "10:30",
        }

        response = self.client.post(
            self.create_url,
            payload,
            format="json"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )

    def test_duplicate_slot(self):

        Appointment.objects.create(
            doctor=self.doctor,
            patient=self.patient,
            appointment_date=date.today() + timedelta(days=1),
            start_time=time(10, 0),
            end_time=time(10, 30),
            status=AppointmentStatus.BOOKED,
        )

        payload = {
            "doctor": self.doctor.id,
            "patient": self.patient.id,
            "appointment_date": str(date.today() + timedelta(days=1)),
            "start_time": "10:00",
            "end_time": "10:30",
        }

        response = self.client.post(
            self.create_url,
            payload,
            format="json"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )

    def test_cancel_appointment(self):

        appointment = Appointment.objects.create(
            doctor=self.doctor,
            patient=self.patient,
            appointment_date=date.today() + timedelta(days=1),
            start_time=time(11, 0),
            end_time=time(11, 30),
            status=AppointmentStatus.BOOKED,
        )

        url = reverse(
            "appointment-cancel",
            kwargs={"pk": appointment.id},
        )

        response = self.client.patch(
            url,
            {
                "cancel_reason": "Patient unavailable"
            },
            format="json",
        )

        appointment.refresh_from_db()

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            appointment.status,
            AppointmentStatus.CANCELLED
        )
    def test_reschedule(self):

        appointment = Appointment.objects.create(
            doctor=self.doctor,
            patient=self.patient,
            appointment_date=date.today() + timedelta(days=1),
            start_time=time(9, 0),
            end_time=time(9, 30),
            status=AppointmentStatus.BOOKED,
        )

        url = reverse(
            "appointment-reschedule",
            kwargs={"pk": appointment.id},
        )

        response = self.client.patch(
            url,
            {
                "start_time": "14:00",
                "end_time": "14:30",
            },
            format="json",
        )

        appointment.refresh_from_db()

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            appointment.start_time,
            time(14, 0)
        )