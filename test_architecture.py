#!/usr/bin/env python3
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from repositories.repository_factory import RepositoryFactory
from models.user import User
from models.patient import Patient
from models.doctor import Doctor
from core.csv_manager import CSVManager


def test_singleton_pattern():
    print("=== Testing Singleton Pattern ===")
    
    csv1 = CSVManager()
    csv2 = CSVManager()
    print(f"CSV Manager Singleton: {csv1 is csv2}")
    
    user_repo1 = RepositoryFactory.get_user_repository()
    user_repo2 = RepositoryFactory.get_user_repository()
    print(f"UserRepository Singleton: {user_repo1 is user_repo2}")
    
    patient_repo1 = RepositoryFactory.get_patient_repository()
    patient_repo2 = RepositoryFactory.get_patient_repository()
    print(f"PatientRepository Singleton: {patient_repo1 is patient_repo2}")
    
    doctor_repo1 = RepositoryFactory.get_doctor_repository()
    doctor_repo2 = RepositoryFactory.get_doctor_repository()
    print(f"DoctorRepository Singleton: {doctor_repo1 is doctor_repo2}")
    print()


def test_factory_pattern():
    print("=== Testing Factory Pattern ===")
    
    user_repo = RepositoryFactory.get_repository('user')
    print(f"Factory created UserRepository: {type(user_repo).__name__}")
    
    patient_repo = RepositoryFactory.get_repository('patient')
    print(f"Factory created PatientRepository: {type(patient_repo).__name__}")
    
    doctor_repo = RepositoryFactory.get_repository('doctor')
    print(f"Factory created DoctorRepository: {type(doctor_repo).__name__}")
    print()


def test_csv_operations():
    print("=== Testing CSV Operations ===")
    
    user_repo = RepositoryFactory.get_user_repository()
    patient_repo = RepositoryFactory.get_patient_repository()
    doctor_repo = RepositoryFactory.get_doctor_repository()
    
    test_user = User('001', 'test@example.com', 'hashed_password', 'John', 'Doe')
    user_repo.save(test_user)
    print(f"Saved User: {test_user}")
    
    retrieved_user = user_repo.get_by_id('001')
    print(f"Retrieved User: {retrieved_user}")
    
    test_patient = Patient('002', 'patient@example.com', 'hashed_pass', 'Jane', 'Smith', 
                           date_of_birth='1990-01-01', medical_history=['Checkup 2024'])
    patient_repo.save(test_patient)
    print(f"Saved Patient: {test_patient}")
    
    retrieved_patient = patient_repo.get_by_id('002')
    print(f"Retrieved Patient: {retrieved_patient}")
    print(f"Medical History: {retrieved_patient.medical_history}")
    
    test_doctor = Doctor('003', 'doctor@example.com', 'hashed_pass', 'Dr. Mike', 'Johnson',
                         specialization='Cardiology', license_number='LIC123')
    doctor_repo.save(test_doctor)
    print(f"Saved Doctor: {test_doctor}")
    
    retrieved_doctor = doctor_repo.get_by_id('003')
    print(f"Retrieved Doctor: {retrieved_doctor}")
    print(f"Specialization: {retrieved_doctor.specialization}")
    print()


def test_repository_pattern():
    print("=== Testing Repository Pattern ===")
    
    patient_repo = RepositoryFactory.get_patient_repository()
    
    all_patients = patient_repo.get_all()
    print(f"Total Patients: {len(all_patients)}")
    
    patient_by_email = patient_repo.find_by_email('patient@example.com')
    if patient_by_email:
        print(f"Found Patient by Email: {patient_by_email.get_full_name()}")
    
    doctor_repo = RepositoryFactory.get_doctor_repository()
    cardiology_doctors = doctor_repo.find_by_specialization('Cardiology')
    print(f"Cardiologists: {len(cardiology_doctors)}")
    print()


if __name__ == '__main__':
    print("Starting Verification Tests...\n")
    
    test_singleton_pattern()
    test_factory_pattern()
    test_csv_operations()
    test_repository_pattern()
    
    print("✅ All tests completed successfully!")
