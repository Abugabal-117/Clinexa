# Clinexa

**Clinexa** is a comprehensive clinical management and appointment booking system designed to streamline interactions between doctors and patients. This project utilizes a layered software architecture to ensure scalability and maintainability, using flat-file (CSV) storage for data persistence.

## 📂 Project Structure

The project follows a Model-View-Controller (MVC) pattern with a Repository layer for data access:

* **`src/app.py`**: The entry point of the application.
* **`src/controllers/`**: Handles business logic (Auth, Doctor, Patient, User).
* **`src/models/`**: Data objects representing the domain (Appointment, Doctor, Patient, etc.).
* **`src/repositories/`**: Handles direct data access and CSV manipulation.
* **`src/core/`**: Core utilities including Authentication and CSV management.
* **`src/data/`**: Storage directory for application data (CSV files).
* **`templates/` & `static/`**: Frontend views and assets.

## 🚀 Features

* **User Authentication**: Secure Login and Signup for Doctors and Patients.
* **Role-Based Dashboards**: Distinct interfaces for Doctors and Patients.
* **Appointment Management**:
    * Patients can book available slots.
    * Doctors can manage schedules (`schedule-management.html`).
* **Feedback System**: Patients can rate and review doctors.
* **Reporting**: View patient reports and appointment history.
* **Data Persistence**: Custom CSV-based database management system.

## 🛠️ Tech Stack

* **Language**: Python 3.x
* **Web Framework**: Flask (Inferred)
* **Frontend**: HTML5, CSS3, JavaScript
* **Storage**: CSV (File-based persistence)
* **Testing**: Pytest
* **Containerization**: Docker & Docker Compose

## ⚙️ Installation & Setup

### Prerequisites
* Python 3.10+
* Docker (Optional)

### Local Development

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/yourusername/Clinexa.git](https://github.com/yourusername/Clinexa.git)
    cd Clinexa
    ```

2.  **Create and activate a virtual environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Run the application:**
    ```bash
    python src/app.py
    ```
    Access the app at `http://localhost:5000` (default).

### 🐳 Running with Docker

1.  **Build and Run using Docker Compose:**
    ```bash
    docker-compose up --build
    ```

## 🧪 Testing

This project maintains high code quality with a comprehensive test suite located in the `tests/` directory.

To run the full test suite:
```bash
# Using the dispatch script
python run_tests_dispatch.py

# OR using pytest directly
pytest
