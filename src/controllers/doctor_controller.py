from repositories.repository_factory import RepositoryFactory
from models.doctor import Doctor
from datetime import datetime


class DoctorController:
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
        """Add an available time slot for the doctor"""
        doctor_repo = RepositoryFactory.get_doctor_repository()
        doctor = doctor_repo.get_by_id(doctor_id)
        
        if not doctor:
            return {'success': False, 'message': 'Doctor not found'}
        
        available_slot = {'date': date, 'time': time}
        
        # Avoid duplicates
        if available_slot not in doctor.available_times:
            doctor.available_times.append(available_slot)
            doctor_repo.save(doctor)
            return {'success': True, 'message': 'Time slot added successfully'}
        
        return {'success': False, 'message': 'Time slot already exists'}

    @staticmethod
    def remove_available_time(doctor_id, date, time):
        """Remove an available time slot for the doctor"""
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
        """Get all available time slots for a doctor"""
        doctor_repo = RepositoryFactory.get_doctor_repository()
        doctor = doctor_repo.get_by_id(doctor_id)
        
        if not doctor:
            return {'success': False, 'message': 'Doctor not found'}
        
        return {'success': True, 'available_times': doctor.available_times}

    @staticmethod
    def remove_patient(doctor_id, patient_id):
        """Remove a patient from doctor's patient list"""
        doctor_repo = RepositoryFactory.get_doctor_repository()
        doctor = doctor_repo.get_by_id(doctor_id)
        
        if not doctor:
            return {'success': False, 'message': 'Doctor not found'}
        
        if patient_id in doctor.patients:
            doctor.patients.remove(patient_id)
            doctor_repo.save(doctor)
            return {'success': True, 'message': 'Patient removed successfully'}
        
        return {'success': False, 'message': 'Patient not found'}
