import pytest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../src'))

from models.patient import Patient
from models.doctor import Doctor
from models.appointment import Appointment
from core.authentication import Authentication


class TestPatientModel:
    
    def test_patient_creation(self):
        patient = Patient(
            user_id="p001",
            email="patient@example.com",
            password_hash=Authentication.hash_password("Password123"),
            first_name="John",
            last_name="Doe"
        )
        
        assert patient.user_id == "p001"
        assert patient.email == "patient@example.com"
        assert patient.first_name == "John"
        assert patient.last_name == "Doe"
    
    def test_patient_get_full_name(self):
        patient = Patient(
            user_id="p001",
            email="patient@example.com",
            password_hash=Authentication.hash_password("Password123"),
            first_name="John",
            last_name="Doe"
        )
        
        assert patient.get_full_name() == "John Doe"
    
    def test_patient_to_dict(self):
        patient = Patient(
            user_id="p001",
            email="patient@example.com",
            password_hash=Authentication.hash_password("Password123"),
            first_name="John",
            last_name="Doe"
        )
        
        patient_dict = patient.to_dict()
        
        assert patient_dict['user_id'] == "p001"
        assert patient_dict['email'] == "patient@example.com"
        assert patient_dict['first_name'] == "John"


class TestDoctorModel:
    
    def test_doctor_creation(self):
        doctor = Doctor(
            user_id="d001",
            email="doctor@example.com",
            password_hash=Authentication.hash_password("Password123"),
            first_name="Jane",
            last_name="Smith",
            specialization="Cardiology"
        )
        
        assert doctor.user_id == "d001"
        assert doctor.email == "doctor@example.com"
        assert doctor.specialization == "Cardiology"
        assert doctor.role == "doctor"
    
    def test_doctor_get_full_name(self):
        doctor = Doctor(
            user_id="d001",
            email="doctor@example.com",
            password_hash=Authentication.hash_password("Password123"),
            first_name="Jane",
            last_name="Smith"
        )
        
        assert doctor.get_full_name() == "Jane Smith"
    
    def test_doctor_add_patient(self):
        doctor = Doctor(
            user_id="d001",
            email="doctor@example.com",
            password_hash=Authentication.hash_password("Password123"),
            first_name="Jane",
            last_name="Smith"
        )
        
        doctor.add_patient("p001")
        
        assert "p001" in doctor.patients
    
    def test_doctor_to_dict(self):
        doctor = Doctor(
            user_id="d001",
            email="doctor@example.com",
            password_hash=Authentication.hash_password("Password123"),
            first_name="Jane",
            last_name="Smith",
            specialization="Neurology",
            license_number="LIC123"
        )
        
        doctor_dict = doctor.to_dict()
        
        assert doctor_dict['user_id'] == "d001"
        assert doctor_dict['specialization'] == "Neurology"
        assert doctor_dict['license_number'] == "LIC123"


class TestAppointmentModel:
    
    def test_appointment_creation(self):
        appointment = Appointment(
            appointment_id="apt001",
            patient_id="p001",
            doctor_id="d001",
            appointment_date="2025-12-25",
            appointment_time="10:00",
            status="confirmed"
        )
        
        assert appointment.appointment_id == "apt001"
        assert appointment.patient_id == "p001"
        assert appointment.doctor_id == "d001"
        assert appointment.appointment_date == "2025-12-25"
        assert appointment.appointment_time == "10:00"
        assert appointment.status == "confirmed"
    
    def test_appointment_to_dict(self):
        appointment = Appointment(
            appointment_id="apt001",
            patient_id="p001",
            doctor_id="d001",
            appointment_date="2025-12-25",
            appointment_time="10:00",
            status="confirmed",
            reason="Checkup"
        )
        
        apt_dict = appointment.to_dict()
        
        assert apt_dict['appointment_id'] == "apt001"
        assert apt_dict['status'] == "confirmed"
        assert apt_dict['reason'] == "Checkup"
