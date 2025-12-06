from repositories.user_repository import UserRepository
from repositories.patient_repository import PatientRepository
from repositories.doctor_repository import DoctorRepository
from repositories.appointment_repository import AppointmentRepository
from repositories.appointment_record_repository import AppointmentRecordRepository
from repositories.feedback_repository import FeedbackRepository


class RepositoryFactory:
    _repositories = {
        'user': UserRepository,
        'patient': PatientRepository,
        'doctor': DoctorRepository,
        'appointment': AppointmentRepository,
        'appointment_record': AppointmentRecordRepository,
        'feedback': FeedbackRepository
    }
    
    @classmethod
    def get_repository(cls, repository_type):
        repository_class = cls._repositories.get(repository_type.lower())
        if repository_class is None:
            raise ValueError(f"Unknown repository type: {repository_type}")
        return repository_class()
    
    @classmethod
    def get_user_repository(cls):
        return cls.get_repository('user')
    
    @classmethod
    def get_patient_repository(cls):
        return cls.get_repository('patient')
    
    @classmethod
    def get_doctor_repository(cls):
        return cls.get_repository('doctor')
    
    @classmethod
    def get_appointment_repository(cls):
        return cls.get_repository('appointment')
    
    @classmethod
    def get_appointment_record_repository(cls):
        return cls.get_repository('appointment_record')

    @classmethod
    def get_feedback_repository(cls):
        return cls.get_repository('feedback')
