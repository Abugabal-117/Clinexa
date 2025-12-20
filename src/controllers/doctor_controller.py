from repositories.repository_factory import RepositoryFactory
from models.doctor import Doctor
from datetime import datetime
import csv
import os

class DoctorController:
    
    @staticmethod
    def _get_data_file_path(filename):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        base_dir = os.path.dirname(current_dir) 
        data_path = os.path.join(base_dir, 'data', filename)
        return data_path

    @staticmethod
    def get_doctor(doctor_id):
        doctor_repo = RepositoryFactory.get_doctor_repository()
        doctor = doctor_repo.get_by_id(doctor_id)
        
        if doctor:
            return {'success': True, 'doctor': doctor}
        return {'success': False, 'message': 'Doctor not found'}
    
    @staticmethod
    def get_all_doctors():
        doctor_repo = RepositoryFactory.get_doctor_repository()
        doctors = doctor_repo.get_all()
        return {'success': True, 'doctors': doctors}

    @staticmethod
    def get_feedback(doctor_id):
        feedback_repo = RepositoryFactory.get_feedback_repository()
        feedback = feedback_repo.find_by_doctor(doctor_id)
        return {'success': True, 'feedback': feedback}

    @staticmethod
    def add_available_time(doctor_id, date, time):
        doctor_repo = RepositoryFactory.get_doctor_repository()
        doctor = doctor_repo.get_by_id(doctor_id)
        
        if not doctor:
            return {'success': False, 'message': 'Doctor not found'}
        
        available_slot = {'date': date, 'time': time}
        
        if available_slot not in doctor.available_times:
            doctor.available_times.append(available_slot)
            doctor_repo.save(doctor)
            return {'success': True, 'message': 'Time slot added successfully'}
        
        return {'success': False, 'message': 'Time slot already exists'}

    @staticmethod
    def remove_available_time(doctor_id, date, time):
        doctor_repo = RepositoryFactory.get_doctor_repository()
        doctor = doctor_repo.get_by_id(doctor_id)
        
        if not doctor:
            return {'success': False, 'message': 'Doctor not found'}
        
        available_slot = {'date': date, 'time': time}
        
        if available_slot in doctor.available_times:
            doctor.available_times.remove(available_slot)
            doctor_repo.save(doctor)
            return {'success': True, 'message': 'Time slot removed successfully'}
        
        return {'success': False, 'message': 'Time slot not found'}

    @staticmethod
    def get_available_times(doctor_id):
        doctor_repo = RepositoryFactory.get_doctor_repository()
        doctor = doctor_repo.get_by_id(doctor_id)
        
        if not doctor:
            return {'success': False, 'message': 'Doctor not found'}
        
        return {'success': True, 'available_times': doctor.available_times}

    @staticmethod
    def remove_patient(doctor_id, patient_id):
        doctor_repo = RepositoryFactory.get_doctor_repository()
        doctor = doctor_repo.get_by_id(doctor_id)
        
        if not doctor:
            return {'success': False, 'message': 'Doctor not found'}
        
        if patient_id in doctor.patients:
            doctor.patients.remove(patient_id)
            doctor_repo.save(doctor)
            return {'success': True, 'message': 'Patient removed successfully'}
        
        return {'success': False, 'message': 'Patient not found'}

    @staticmethod
    def get_all_patients():
        patients = []
        patients_path = DoctorController._get_data_file_path('patients.csv')
        
        print(f"DEBUG: Reading patients from: {patients_path}")

        try:
            with open(patients_path, mode='r', encoding='utf-8-sig') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    if 'patient_id' in row and 'user_id' not in row:
                        row['user_id'] = row['patient_id']
                    
                    patients.append(row)
        except FileNotFoundError:
            print(f"DEBUG: File not found at {patients_path}")
        except Exception as e:
            print(f"DEBUG: Error reading patients file: {str(e)}")
            
        return patients

    @staticmethod
    def create_report(doctor_id, patient_id, patient_name, details):
        report_path = DoctorController._get_data_file_path('reports.csv')
        file_exists = os.path.isfile(report_path)
        
        os.makedirs(os.path.dirname(report_path), exist_ok=True)
        
        try:
            with open(report_path, mode='a', newline='', encoding='utf-8') as file:
                fieldnames = ['report_id', 'doctor_id', 'patient_id', 'patient_name', 'details', 'created_at']
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                
                if not file_exists:
                    writer.writeheader()
                
                writer.writerow({
                    'report_id': datetime.now().strftime("%Y%m%d%H%M%S"),
                    'doctor_id': doctor_id,
                    'patient_id': patient_id,
                    'patient_name': patient_name,
                    'details': details,
                    'created_at': datetime.now().strftime("%Y-%m-%d %H:%M")
                })
            return {'success': True}
        except Exception as e:
            print(f"Error creating report: {e}")
            return {'success': False, 'message': str(e)}

    @staticmethod
    def get_doctor_reports(doctor_id):
        reports = []
        report_path = DoctorController._get_data_file_path('reports.csv')
        
        if not os.path.isfile(report_path):
            return {'success': True, 'reports': []}
            
        try:
            with open(report_path, mode='r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    if row['doctor_id'] == str(doctor_id):
                        reports.insert(0, row)
            return {'success': True, 'reports': reports}
        except Exception as e:
            print(f"Error reading reports: {e}")
            return {'success': False, 'message': str(e)}