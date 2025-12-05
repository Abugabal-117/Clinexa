#!/usr/bin/env python3
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from controllers.user_controller import UserController
from controllers.patient_controller import PatientController
from controllers.doctor_controller import DoctorController
from repositories.repository_factory import RepositoryFactory


def test_user_registration():
    print("=== Testing User Registration ===")
    
    import uuid
    unique_id = str(uuid.uuid4())[:8]
    
    result = UserController.register(
        email=f'patient_{unique_id}@example.com',
        password='password123',
        first_name='Alice',
        last_name='Smith',
        user_type='patient',
        date_of_birth='1990-05-15'
    )
    print(f"Patient Registration: {result['success']} - {result.get('user', result.get('message'))}")
    
    result = UserController.register(
        email=f'doctor_{unique_id}@example.com',
        password='docpass123',
        first_name='Dr. John',
        last_name='Doe',
        user_type='doctor',
        specialization='Cardiology',
        license_number='LIC12345'
    )
    print(f"Doctor Registration: {result['success']} - {result.get('user', result.get('message'))}")
    print()


def test_patient_operations():
    print("=== Testing Patient Operations ===")
    
    result = PatientController.get_all_patients()
    patients = result['patients']
    print(f"Total Patients: {len(patients)}")
    
    if patients:
        patient = patients[0]
        print(f"Patient: {patient.get_full_name()}")
        
        result = PatientController.add_medical_record(
            patient.user_id,
            'Annual Checkup 2024 - All vitals normal'
        )
        print(f"Add Medical Record: {result['success']}")
        
        result = PatientController.get_medical_history(patient.user_id)
        print(f"Medical History Records: {len(result['medical_history'])}")
        
        result = PatientController.search_patients('Alice')
        print(f"Search Results for 'Alice': {len(result['patients'])} found")
    print()


def test_doctor_operations():
    print("=== Testing Doctor Operations ===")
    
    result = DoctorController.get_all_doctors()
    doctors = result['doctors']
    print(f"Total Doctors: {len(doctors)}")
    
    if doctors:
        doctor = doctors[0]
        print(f"Doctor: {doctor.get_full_name()} - {doctor.specialization}")
        
        result = DoctorController.search_doctors(specialization='Cardiology')
        print(f"Cardiologists Found: {len(result['doctors'])}")
        
        result = DoctorController.get_todays_appointments(doctor.user_id)
        print(f"Today's Appointments: {len(result['appointments'])}")
    print()


def test_appointment_booking():
    print("=== Testing Appointment Booking ===")
    
    patient_result = PatientController.get_all_patients()
    doctor_result = DoctorController.get_all_doctors()
    
    if patient_result['patients'] and doctor_result['doctors']:
        patient = patient_result['patients'][0]
        doctor = doctor_result['doctors'][0]
        
        result = PatientController.book_appointment(
            patient_id=patient.user_id,
            doctor_id=doctor.user_id,
            appointment_date='2025-02-15',
            appointment_time='10:00',
            reason='Regular checkup'
        )
        print(f"Book Appointment: {result['success']}")
        
        if result['success']:
            appointment = result['appointment']
            print(f"Appointment ID: {appointment.appointment_id}")
            print(f"Status: {appointment.status}")
            
            result = PatientController.get_appointments(patient.user_id)
            print(f"Patient Appointments: {len(result['appointments'])}")
            
            result = DoctorController.get_appointments(doctor.user_id)
            print(f"Doctor Appointments: {len(result['appointments'])}")
    print()


def test_medical_records():
    print("=== Testing Medical Records ===")
    
    appointment_repo = RepositoryFactory.get_appointment_repository()
    appointments = appointment_repo.get_all()
    
    if appointments:
        appointment = appointments[0]
        
        result = DoctorController.create_medical_record(
            doctor_id=appointment.doctor_id,
            patient_id=appointment.patient_id,
            appointment_id=appointment.appointment_id,
            diagnosis='Mild hypertension, well managed',
            prescription='Continue current medication, annual follow-up recommended',
            notes='Patient is doing well, no major concerns'
        )
        print(f"Create Medical Record: {result['success']}")
        
        if result['success']:
            result = DoctorController.view_patient_history(
                appointment.doctor_id,
                appointment.patient_id
            )
            print(f"Patient History Retrieved: {result['success']}")
            print(f"Appointment Records: {len(result.get('appointment_records', []))}")
    print()


def test_profile_updates():
    print("=== Testing Profile Updates ===")
    
    patient_result = PatientController.get_all_patients()
    if patient_result['patients']:
        patient = patient_result['patients'][0]
        
        result = UserController.update_profile(
            patient.user_id,
            first_name='Alicia',
            last_name='Smith-Johnson'
        )
        print(f"Update Profile: {result['success']}")
        
        if result['success']:
            updated_user = result['user']
            print(f"Updated Name: {updated_user.get_full_name()}")
    print()


def test_reports():
    print("=== Testing Report Generation ===")
    
    doctor_result = DoctorController.get_all_doctors()
    if doctor_result['doctors']:
        doctor = doctor_result['doctors'][0]
        
        result = DoctorController.generate_report(
            doctor.user_id,
            report_type='workload'
        )
        print(f"Generate Report: {result['success']}")
        
        if result['success']:
            report = result['report']
            print(f"Total Appointments: {report['total_appointments']}")
            print(f"Confirmed: {report['confirmed']}")
            print(f"Completed: {report['completed']}")
            print(f"Cancelled: {report['cancelled']}")
    print()


if __name__ == '__main__':
    print("=" * 60)
    print("CONTROLLER FUNCTIONALITY TESTS")
    print("=" * 60)
    print()
    
    test_user_registration()
    test_patient_operations()
    test_doctor_operations()
    test_appointment_booking()
    test_medical_records()
    test_profile_updates()
    test_reports()
    
    print("=" * 60)
    print("✅ All controller tests completed!")
    print("=" * 60)
