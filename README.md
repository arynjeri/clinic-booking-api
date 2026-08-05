# 🏥 Clinic Booking API

A RESTful API built with **Django** and **Django REST Framework** for managing doctors, patients, and appointment bookings. The API prevents double-booking, validates appointment dates and working hours, and allows appointment cancellation, rescheduling, and doctor availability checks.

## Live Demo

**API Base URL**

```
https://clinic-booking-api-w6wz.onrender.com/

> **Note:** The deployed application starts with an empty database. Create doctors and patients before booking appointments or checking doctor availability.
```

**Swagger Documentation**

```
https://clinic-booking-api-w6wz.onrender.com/docs/
```

**OpenAPI Schema**

```
https://clinic-booking-api-w6wz.onrender.com/schema/
```

## System Design

### Architecture

The project follows a layered architecture to separate responsibilities and improve maintainability.

* **Models** define the application's data structure for Doctors, Patients, and Appointments.
* **Serializers** validate incoming requests and convert model instances to JSON responses.
* **Views** expose REST API endpoints and handle HTTP requests and responses.
* **Services** contain the business logic, such as appointment booking, rescheduling, duplicate booking prevention, and doctor availability checks.
* **Validators** enforce business rules such as future appointment dates and appointments within a doctor's working hours.

### Database Design

The application consists of three main entities:

* **Doctor**

  * Name
  * Specialty
  * Working start time
  * Working end time

* **Patient**

  * First name
  * Last name
  * Email
  * Phone number

* **Appointment**

  * Doctor (Foreign Key)
  * Patient (Foreign Key)
  * Appointment date
  * Start time
  * End time
  * Status (Booked or Cancelled)
  * Cancellation reason

A doctor can have many appointments, and a patient can have many appointments.

### Appointment Booking Workflow

1. The client submits an appointment request.
2. The serializer validates the request data.
3. Custom validators ensure:

   * The appointment date is in the future.
   * The appointment falls within the doctor's working hours.
4. The service layer checks whether the requested time slot is already booked.
5. If the slot is available, the appointment is saved.
6. A success response is returned; otherwise, a validation error is returned.

### Design Decisions

* Business logic was moved into an `AppointmentService` class to keep views focused on handling HTTP requests.
* Custom validators were used to separate validation rules from the models and views.
* Django REST Framework generic views were used for standard CRUD operations to reduce boilerplate code.
* Swagger documentation was integrated using **drf-spectacular** to simplify API exploration and testing.

### Assumptions & Tradeoffs

* Appointment slots are fixed at 30-minute intervals.
* Doctors cannot be double-booked for the same date and start time.
* Only booked appointments occupy a time slot.
* Working hours are predefined for each doctor.
* SQLite was selected for simplicity during development, with PostgreSQL being a suitable option for production deployments.


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
python manage.py makemigrations
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


## API Endpoints

### Patients

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/patients/` | List all patients |
| POST | `/patients/` | Create a new patient |
| GET | `/patients/{id}/` | Retrieve a patient |

### Doctors

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/doctors/` | List all doctors |
| POST | `/doctors/` | Create a new doctor |
| GET | `/doctors/{id}/` | Retrieve a doctor |
| GET | `/doctors/{id}/availability/?date=YYYY-MM-DD` | View available appointment slots |

### Appointments

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/appointments/` | List all appointments |
| POST | `/appointments/` | Create a new appointment |
| PATCH | `/appointments/{id}/cancel/` | Cancel an appointment |
| PATCH | `/appointments/{id}/reschedule/` | Reschedule an appointment |

---

## Running Tests

```bash
python manage.py test
```

---

## Business Rules

- Appointment dates must be in the future.
- Appointment time must fall within the doctor's working hours.
- A doctor cannot have two active (booked) appointments in the same time slot.
- Cancelled appointments cannot be cancelled again.

---



## AI Reflection

### 1. What did you use AI for across the four sections?

* Planned the project structure and application architecture.
* Generated and reviewed Django models, serializers, views, services, validators, and URL routing.
* Assisted in debugging Django errors, API responses, migrations, deployment issues, and Render configuration.
* Helped prepare project documentation, deployment instructions, and the README.

### 2. Give one example where an AI suggestion improved your work. What did you prompt it with?

AI suggested separating the appointment business logic from the views into an `AppointmentService` class. This made the code easier to maintain, reduced duplication, and kept the views focused on request handling.

**Prompt:** *"How can I organize my appointment booking logic following Django best practices?"*

### 3. Give one example where AI output was wrong or incomplete and how you caught it.

One AI suggestion assumed the appointment availability endpoint was implemented correctly, but the view was still calling the service with the wrong method signature, causing a runtime error. I identified the issue by reading the Django traceback, checking the view implementation, updating the method call, and verifying the fix through Postman testing. Throughout development, I treated AI suggestions as guidance rather than final solutions and validated them by running the application and reviewing the results.

### 4. Name two decisions you made without AI. Why did you trust your own judgment there?

* I chose to complete deployment before implementing optional enhancements such as richer API documentation because meeting the submission requirements was the highest priority.
* I decided to retain the service-layer architecture after evaluating different approaches because it improved code organization, separated business logic from HTTP handling, and made the application easier to maintain and test.


---
