# 🏥 Clinic Booking API

A RESTful API built with **Django** and **Django REST Framework** for managing doctors, patients, and appointment bookings. The API prevents double-booking, validates appointment dates and working hours, and allows appointment cancellation, rescheduling, and doctor availability checks.

---

## Features

- Create appointments
- Prevent duplicate bookings for the same doctor and time slot
- Validate future appointment dates
- Validate appointments against a doctor's working hours
- Cancel appointments
- Reschedule appointments
- Check a doctor's available time slots
- Interactive API documentation with Swagger (drf-spectacular)
- Automated tests

---

## Tech Stack

- Python 3
- Django
- Django REST Framework
- drf-spectacular (Swagger/OpenAPI)
- SQLite (development)

---

## Project Structure

```
clinic-booking-api/
├── appointments/
├── doctors/
├── patients/
├── config/
├── manage.py
├── requirements.txt
└── README.md
```

---

## Installation

### Clone the repository

```bash
git clone <your-repository-url>
cd clinic-booking-api
```

### Create a virtual environment

Linux/macOS

```bash
python -m venv venv
source venv/bin/activate
```

Windows

```bash
venv\Scripts\activate
```

### Install dependencies

```bash
pip install -r requirements.txt
```

### Apply migrations

```bash
python manage.py migrate
```

### Create a superuser (optional)

```bash
python manage.py createsuperuser
```

### Run the server

```bash
python manage.py runserver
```

---

## API Documentation

Swagger UI

```
http://127.0.0.1:8000/docs/
```

OpenAPI Schema

```
http://127.0.0.1:8000/schema/
```

---

## Main Endpoints

### Appointments

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/appointments/` | Create appointment |
| PATCH | `/appointments/{id}/cancel/` | Cancel appointment |
| PATCH | `/appointments/{id}/reschedule/` | Reschedule appointment |

### Doctors

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/doctors/{id}/availability/?date=YYYY-MM-DD` | View available appointment slots |

---

## Running Tests

```bash
python manage.py test
```

---

## Business Rules

- Appointment dates must be in the future.
- Appointment time must fall within the doctor's working hours.
- A doctor cannot have two appointments in the same time slot.
- Cancelled appointments cannot be cancelled again.

---

## Future Improvements

- Authentication & Authorization
- CRUD endpoints for Doctors and Patients
- PostgreSQL support
- Docker deployment
- CI/CD pipeline
- Email/SMS appointment reminders

---
