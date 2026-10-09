# Clinexa

**Clinexa** is a Clinical Management System designed to streamline interactions between doctors and patients. It features a complete appointment booking engine, role-based dashboards, and a custom CSV-based persistence layer, developed for the CSAI203 Software Engineering course.

---

## Project Architecture

The application implements a strict **MVC (Model-View-Controller)** architecture with a **Repository Pattern** to decouple business logic from data access.

- `src/controllers/`: Orchestrates logic between the UI and data models.
- `src/repositories/`: Handles direct interactions with the CSV database.
- `src/models/`: Python classes representing core entities (Doctor, Patient, Appointment).
- `src/data/`: Flat-file database storage containing all system records in CSV format[cite: 1].
- `src/core/`: Core system utilities including Authentication and CSV management[cite: 1].

---

## Key Features

- **Role-Based Access:**[cite: 1]
  - **Doctors:** Manage schedules, view appointments, and upload reports[cite: 1].
  - **Patients:** Book appointments, view medical reports, and rate/review doctors[cite: 1].
- **Appointment System:** Full lifecycle management (Booking, Scheduling, History)[cite: 1].
- **Feedback Loop:** Integrated rating system stored in `feedback.csv`[cite: 1].
- **Data Persistence:** Custom-built CSV manager ensuring data integrity[cite: 1].
- **Secure Authentication:** Hashed credentials and session management[cite: 1].

---

## Project Documentation

Detailed documentation regarding the system design, requirements, and usage instructions can be found in the `docs/` folder of this repository[cite: 1].

| Document | Path | Description |
| :--- | :--- | :--- |
| **User Manual** | `docs/Clinexa User Manual` | Step-by-step guide for Patients and Doctors. |
| **System Design** | `docs/CSAI203_Design_Team26.pdf` | UML diagrams, architecture, and design patterns. |
| **SRS** | `docs/CSAI203_SRS_Team26.pdf` | Functional & non-functional requirements. |

---

## Default Login Credentials

Use these credentials to test the application's different roles[cite: 1].

| Role | Email | Password |
| :--- | :--- | :--- |
| **Doctor** | `Clinexa_Doctor@clinexa.eg` | `Doctor_Password_123` |

---

## Tech Stack

- **Language:** Python 3.11[cite: 1]
- **Framework:** Flask[cite: 1]
- **Frontend:** HTML5, CSS3, JavaScript[cite: 1]
- **Containerization:** Docker[cite: 1]
- **CI/CD:** GitHub Actions[cite: 1]

---

## Installation & Setup

We recommend running Clinexa by pulling the pre-built image from Docker Hub[cite: 1].

### Prerequisites
- Docker Desktop or Docker Engine installed[cite: 1].
- Git[cite: 1].

### Step 1: Clone the Repository
```bash
git clone [https://github.com/r4g4b/clinexa.git](https://github.com/r4g4b/clinexa.git)
cd clinexa
