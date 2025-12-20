**
**Clinexa** is a Clinical Management System designed to streamline interactions between doctors and patients. It features a complete appointment booking engine, role-based dashboards, and a custom CSV-based persistence layer, developed for the CSAI203 Software Engineering course.

## Project Architecture

The application implements a strict **MVC (Model-View-Controller)** architecture with a **Repository Pattern** to decouple business logic from data access.

* **`src/controllers/`**: Orchestrates logic between the UI and data models.
* **`src/repositories/`**: Handles direct interactions with the CSV database.
* **`src/models/`**: Python classes representing core entities (Doctor, Patient, Appointment).
* **`src/data/`**: Flat-file database storage containing all system records in CSV format.
* **`src/core/`**: Core system utilities including Authentication and CSV management.

## Key Features

* **Role-Based Access**:
    * **Doctors**: Manage schedules, view appointments, and upload reports.
    * **Patients**: Book appointments, view medical reports, and rate/review doctors.
* **Appointment System**: Full lifecycle management (Booking, Scheduling, History).
* **Feedback Loop**: Integrated rating system stored in `feedback.csv`.
* **Data Persistence**: Custom-built CSV manager ensuring data integrity without an SQL engine.
* **Secure Authentication**: Hashed credentials and session management.


* **Language**: Python 3.x
* **Framework**: Flask
* **Frontend**: HTML5, CSS3, JavaScript
* **Testing**: Pytest (Unit & Integration tests)
* **Containerization**: Docker & Docker Compose


* Python 3.10+
* Docker (Optional)

### Local Development (No Docker)

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/r4g4b/Clinexa.git
    cd Clinexa
    ```

2.  **Set up the environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # Windows: venv\Scripts\activate
    pip install -r requirements.txt
    ```

3.  **Run the application:**
    ```bash
    python src/app.py
    ```
    Access at: `http://localhost:5000`

###  Running with Docker (Recommended)

To run the application in an isolated environment:

```bash
docker-compose up --build
```

This project maintains high code quality with a comprehensive test suite located in the `tests/` directory.

To run the full test suite:
```bash
python run_tests_dispatch.py

pytest
**