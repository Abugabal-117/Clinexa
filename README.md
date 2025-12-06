# Clinexa Medical System

Clinexa is a comprehensive web-based healthcare management system designed to streamline the interaction between healthcare providers and patients. It replaces traditional paper-based processes with a digital solution, improving efficiency and accessibility.

## Features

### For Patients
- **User Authentication**: Secure signup and login.
- **Dashboard**: View upcoming appointments and status.
- **Search**: Find doctors by name or specialization.
- **Booking**: Schedule appointments with doctors.
- **Medical History**: Access personal medical records and prescriptions.
- **Feedback**: Rate and review doctors.

### For Doctors
- **Profile Management**: Update specialization and availability.
- **Schedule Management**: View and manage appointments.
- **Patient Records**: Create and view medical records for patients.
- **Reports**: Generate workload and appointment reports.

## Architecture

The system follows a **Model-View-Controller (MVC)** architectural pattern to ensure separation of concerns and maintainability.

- **Models**: Python classes representing data entities (User, Patient, Doctor, Appointment, Review, etc.).
- **Views**: HTML templates styled with CSS for the user interface.
- **Controllers**: Business logic handlers that process requests and interact with models and repositories.
- **Repositories**: Data access layer managing file-based storage (PSV format).

## Tech Stack

- **Backend**: Python 3.x, Flask
- **Frontend**: HTML5, CSS3, Jinja2
- **Data Storage**: Text-based file system

## Project Structure

```
Clinexa/
├── controllers/      # Business logic controllers
├── models/           # Data models
├── repositories/     # Data access layer
├── templates/        # HTML templates
├── static/           # CSS and assets
├── data/             # Data storage files
├── docs/             # Documentation (SRS, Design)
└── app.py            # Main application entry point
```

## Setup and Usage

1. **Prerequisites**: Python 3.x installed.
2. **Installation**:
   ```bash
   # Clone the repository
   # Navigate to the project directory
   cd Clinexa
   ```
3. **Run the Application**:
   ```bash
   python3 app.py
   ```
4. **Access**: Open your browser and navigate to `http://localhost:5000`.

