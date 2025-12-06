#!/usr/bin/env python3
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from controllers.user_controller import UserController

def clear_all_data():
    print("Clearing existing data...")
    
    data_files = [
        'data/users.csv',
        'data/patients.csv',
        'data/doctors.csv',
        'data/appointments.csv',
        'data/notifications.csv',
        'data/feedback.csv',
        'data/appointment_records.csv'
    ]
    
    headers = {
        'data/users.csv': 'user_id,email,password_hash,first_name,last_name,role,created_at,is_active\n',
        'data/patients.csv': 'user_id,email,password_hash,first_name,last_name,role,created_at,is_active,date_of_birth,medical_history,appointments\n',
        'data/doctors.csv': 'user_id,email,password_hash,first_name,last_name,role,created_at,is_active,specialization,license_number,patients,appointments\n',
        'data/appointments.csv': 'appointment_id,patient_id,doctor_id,appointment_date,appointment_time,status,reason,created_at\n',
        'data/notifications.csv': 'notification_id,user_id,message,is_read,created_at\n',
        'data/feedback.csv': 'feedback_id,patient_id,doctor_id,rating,comment,created_at\n',
        'data/appointment_records.csv': 'record_id,appointment_id,patient_id,doctor_id,diagnosis,prescription,notes,created_at\n'
    }
    
    for file_path in data_files:
        if os.path.exists(file_path):
            with open(file_path, 'w') as f:
                f.write(headers.get(file_path, ''))
    
    print("✅ Data cleared")

def create_default_doctor():
    print("Creating doctor account...")
    
    result = UserController.register(
        email='doctor@clinic.com',
        password='DOCPassword33',
        first_name='Default',
        last_name='Doctor',
        user_type='doctor',
        specialization='General Medicine',
        license_number='DOC-2024-001'
    )
    
    if result['success']:
        print("✅ Doctor created: doctor@clinic.com / DOCPassword33")
        return True
    else:
        print(f"❌ Failed: {result['message']}")
        return False

def main():
    print("=" * 60)
    print("DATABASE INITIALIZATION")
    print("=" * 60)
    print("\n⚠️  This will DELETE all existing data!")
    
    response = input("\nContinue? (yes/no): ").strip().lower()
    if response != 'yes':
        print("Aborted.")
        return
    
    print()
    clear_all_data()
    success = create_default_doctor()
    
    print("\n" + "=" * 60)
    if success:
        print("✅ INITIALIZATION COMPLETE")
    else:
        print("❌ INITIALIZATION FAILED")
    print("=" * 60)

if __name__ == '__main__':
    main()
