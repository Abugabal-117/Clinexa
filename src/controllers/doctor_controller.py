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
