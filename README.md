# 🏥 Clinic Booking API

A RESTful API built with **Django** and **Django REST Framework** for managing doctors, patients, and appointment bookings.

The system allows patients to book appointments with doctors while enforcing business rules such as preventing double-booking, validating appointment dates and working hours, supporting appointment cancellation and rescheduling, and checking doctor availability.

---

# Live Demo

### API Base URL

```
https://clinic-booking-api-w6wz.onrender.com/
```

### Swagger Documentation

```
https://clinic-booking-api-w6wz.onrender.com/docs/
```

### OpenAPI Schema

```
https://clinic-booking-api-w6wz.onrender.com/schema/
```

> **Note**
>
> The deployed application starts with an empty database. Create one or more doctors and patients before creating appointments or checking doctor availability.

---

# Table of Contents

- Features
- Tech Stack
- System Design
- Project Structure
- Installation
- API Endpoints
- Business Rules
- Running Tests
- CI/CD
- AI Reflection

---

# Features

- Create doctors and patients
- Book appointments
- Prevent duplicate bookings
- Validate future appointment dates
- Validate appointments against doctor's working hours
- Cancel appointments with a reason
- Reschedule appointments
- Check doctor availability
- Interactive Swagger API documentation
- Automated test coverage

---

# Tech Stack

- Python 3
- Django
- Django REST Framework
- drf-spectacular (Swagger/OpenAPI)
- SQLite (Development)
- Render (Deployment)
- GitHub Actions (CI/CD)

---

# System Design

## Architecture

The application follows a layered architecture to separate concerns and improve maintainability.

### Models

Responsible for representing the application's data.

- Doctor
- Patient
- Appointment

### Serializers

- Validate incoming requests
- Convert model instances into JSON responses

### Views

- Expose REST endpoints
- Handle HTTP requests and responses

### Services

The business logic is centralized inside an `AppointmentService` class.

Responsibilities include:

- Booking appointments
- Preventing duplicate bookings
- Rescheduling appointments
- Checking doctor availability

### Validators

Custom validators enforce business rules such as:

- Future appointment dates
- Working hour validation

---

## Database Design

### Doctor

| Field |
|--------|
| Name |
| Specialization |
| Working Start Time |
| Working End Time |

### Patient

| Field |
|--------|
| First Name |
| Last Name |
| Email |
| Phone Number |

### Appointment

| Field |
|--------|
| Doctor (Foreign Key) |
| Patient (Foreign Key) |
| Appointment Date |
| Start Time |
| End Time |
| Status |
| Cancellation Reason |

### Relationships

- One doctor can have many appointments.
- One patient can have many appointments.

---

## Appointment Booking Workflow

1. A client submits an appointment request.
2. The serializer validates the request data.
3. Custom validators ensure:
   - the appointment date is in the future
   - the appointment falls within the doctor's working hours
4. The service layer checks whether the requested slot is already booked.
5. If available, the appointment is saved.
6. Otherwise, a validation error is returned.

---

## Design Decisions

- Business logic was moved into an `AppointmentService` to keep views lightweight.
- Validation logic was separated into reusable validator functions.
- Django REST Framework Generic Views were used where appropriate to reduce boilerplate.
- Swagger documentation was integrated using **drf-spectacular** for easier API exploration.

---

## Assumptions & Trade-offs

### Assumptions

- Appointment slots are fixed at **30 minutes**.
- Doctors define their own working hours.
- Only appointments with a status of **BOOKED** occupy a slot.
- Cancelled appointments immediately free the slot for future bookings.

### Trade-offs

- SQLite was used for simplicity during development.
- PostgreSQL would be a better choice for production environments.
- Authentication was omitted to focus on the required booking workflow.

---

# Project Structure

```
clinic-booking-api/
│
├── appointments/
├── doctors/
├── patients/
├── config/
├── .github/
│   └── workflows/
│       └── django.yml
├── manage.py
├── requirements.txt
└── README.md
```

---

# Installation

## Clone the repository

```bash
git clone <repository-url>
cd clinic-booking-api
```

## Create a virtual environment

### Linux / macOS

```bash
python -m venv venv
source venv/bin/activate
```

### Windows

```bash
venv\Scripts\activate
```

## Install dependencies

```bash
pip install -r requirements.txt
```

## Apply migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

## Create a superuser (Optional)

```bash
python manage.py createsuperuser
```

## Run the development server

```bash
python manage.py runserver
```

---

# API Endpoints

## Patients

| Method | Endpoint | Description |
|---------|----------|-------------|
| GET | `/patients/` | List all patients |
| POST | `/patients/` | Create a patient |
| GET | `/patients/{id}/` | Retrieve a patient |

---

## Doctors

| Method | Endpoint | Description |
|---------|----------|-------------|
| GET | `/doctors/` | List all doctors |
| POST | `/doctors/` | Create a doctor |
| GET | `/doctors/{id}/` | Retrieve a doctor |
| GET | `/doctors/{id}/availability/?date=YYYY-MM-DD` | Check available appointment slots |

---

## Appointments

| Method | Endpoint | Description |
|---------|----------|-------------|
| GET | `/appointments/` | List appointments |
| POST | `/appointments/` | Book an appointment |
| PATCH | `/appointments/{id}/cancel/` | Cancel an appointment |
| PATCH | `/appointments/{id}/reschedule/` | Reschedule an appointment |

---

# Business Rules

The API enforces the following rules:

- Appointment dates must be in the future.
- Appointments must fall within a doctor's working hours.
- Doctors cannot be double-booked.
- Cancelled appointments cannot be cancelled again.
- Rescheduled appointments must satisfy the same validation rules as newly created appointments.
- Cancelling an appointment immediately makes the slot available for booking again.

---

# Running Tests

Run the automated test suite with:

```bash
python manage.py test
```

The current tests cover:

- Appointment creation
- Past-date validation
- Duplicate booking prevention
- Appointment cancellation
- Appointment rescheduling

---

# CI/CD

This project uses **GitHub Actions** together with **Render** for Continuous Integration and Continuous Deployment.

## Continuous Integration

Every push and pull request targeting the **main** branch automatically:

- Installs project dependencies
- Applies database migrations
- Runs the Django test suite

## Continuous Deployment

The application is deployed on **Render**.

The **main** branch is connected to Render. After the GitHub Actions workflow completes successfully, Render automatically deploys the latest version of the application.

This ensures that only code that passes all automated tests is deployed.

---

# AI Reflection

## 1. What did you use AI for across the four sections?

- Planned the overall project architecture.
- Generated and refined Django models, serializers, views, validators, services, and URL routing.
- Assisted with debugging Django, DRF, deployment, and Render configuration issues.
- Helped improve the project documentation and README structure.

---

## 2. Give one example where an AI suggestion improved your work.

One useful suggestion was moving the appointment business logic into an `AppointmentService` class instead of placing it directly inside the views.

This improved code organization, reduced duplication, and made the views responsible only for handling HTTP requests.

**Prompt used:**

> *"How can I organize my appointment booking logic following Django best practices?"*

---

## 3. Give one example where AI output was wrong or incomplete and how you caught it.

One AI-generated solution assumed the doctor availability endpoint was implemented correctly, but it still called the service using the wrong method signature, resulting in a runtime error.

I identified the problem by reading the Django traceback, inspecting the view implementation, correcting the service call, and verifying the fix using Postman and automated tests.

This reinforced the importance of validating AI-generated code through testing rather than accepting it without verification.

---

## 4. Name two decisions you made without AI.

- I prioritized completing deployment and CI/CD before implementing optional enhancements because meeting the assessment requirements was the highest priority.
- I chose to keep the service-layer architecture after evaluating alternative approaches because it provided better separation of concerns and made the application easier to maintain and test.

---
