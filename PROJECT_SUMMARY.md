
## Project Structure

Clinexa/
├── models/                      # Data Models (M in MVC)
│   ├── user.py                 # Base user model
│   ├── patient.py              # Patient model with medical history
│   ├── doctor.py               # Doctor model with specialization
│   ├── appointment.py          # Appointment bookings
│   └── appointment_record.py   # Medical consultation records
│
├── repositories/                # Data Access Layer (Repository Pattern)
│   ├── base_repository.py      # Abstract base with CRUD operations
│   ├── user_repository.py      # User data access (Singleton)
│   ├── patient_repository.py   # Patient data access (Singleton)
│   ├── doctor_repository.py    # Doctor data access (Singleton)
│   ├── appointment_repository.py
│   ├── appointment_record_repository.py
│   └── repository_factory.py   # Factory Pattern for repositories
│
├── controllers/                 # Business Logic (C in MVC)
│   ├── user_controller.py      # Authentication & profile management
│   ├── patient_controller.py   # Patient operations & appointments
│   └── doctor_controller.py    # Doctor operations & medical records
│
├── core/                        # Core Utilities
│   ├── csv_manager.py          # CSV file handling (Singleton)
│   └── authentication.py       # Password hashing & session management
│
├── data/                        # CSV Data Storage
│   ├── users.csv
│   ├── patients.csv
│   ├── doctors.csv
│   ├── appointments.csv
│   └── appointment_records.csv
│
└── templates/                   # Views (V in MVC) - Ready for integration
