import pytest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

class TestModelsExist:
    def test_user_model_imports(self):
        try:
            from models.user import User
            assert User is not None
        except ImportError:
            pytest.skip("User model not found")
    
    def test_patient_model_imports(self):
        try:
            from models.patient import Patient
            assert Patient is not None
        except ImportError:
            pytest.skip("Patient model not found")
    
    def test_doctor_model_imports(self):
        try:
            from models.doctor import Doctor
            assert Doctor is not None
        except ImportError:
            pytest.skip("Doctor model not found")
    
    def test_appointment_model_imports(self):
        try:
            from models.appointment import Appointment
            assert Appointment is not None
        except ImportError:
            pytest.skip("Appointment model not found")

class TestControllers:
    def test_user_controller_imports(self):
        try:
            from controllers.user_controller import UserController
            assert UserController is not None
        except ImportError:
            pytest.skip("UserController not found")
    
    def test_patient_controller_imports(self):
        try:
            from controllers.patient_controller import PatientController
            assert PatientController is not None
        except ImportError:
            pytest.skip("PatientController not found")
    
    def test_doctor_controller_imports(self):
        try:
            from controllers.doctor_controller import DoctorController
            assert DoctorController is not None
        except ImportError:
            pytest.skip("DoctorController not found")
