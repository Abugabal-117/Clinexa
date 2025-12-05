from threading import Lock
from repositories.base_repository import BaseRepository
from models.appointment import Appointment


class AppointmentRepository(BaseRepository):
    _instance = None
    _lock = Lock()
    
    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if self._initialized:
            return
        super().__init__('appointments.csv', id_field='appointment_id')
        self._initialized = True
    
    def get_fieldnames(self):
        return ['appointment_id', 'patient_id', 'doctor_id', 'appointment_date', 
                'appointment_time', 'status', 'reason', 'meeting_link', 'created_date', 'updated_date']
    
    def to_model(self, data):
        return Appointment.from_dict(data)
    
    def find_by_patient(self, patient_id):
        return self.find_by_field('patient_id', patient_id)
    
    def find_by_doctor(self, doctor_id):
        return self.find_by_field('doctor_id', doctor_id)
    
    def find_by_status(self, status):
        return self.find_by_field('status', status)
    
    def find_by_date(self, date):
        return self.find_by_field('appointment_date', date)
