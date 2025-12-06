from threading import Lock
from repositories.base_repository import BaseRepository
from models.appointment_record import AppointmentRecord


class AppointmentRecordRepository(BaseRepository):
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
        super().__init__('appointment_records.csv', id_field='record_id')
        self._initialized = True
    
    def get_fieldnames(self):
        return ['record_id', 'appointment_id', 'patient_id', 'doctor_id', 
                'diagnosis', 'prescription', 'notes', 'created_date']
    
    def to_model(self, data):
        return AppointmentRecord.from_dict(data)
    
    def find_by_patient(self, patient_id):
        return self.find_by_field('patient_id', patient_id)
    
    def find_by_doctor(self, doctor_id):
        return self.find_by_field('doctor_id', doctor_id)
    
    def find_by_appointment(self, appointment_id):
        results = self.find_by_field('appointment_id', appointment_id)
        return results[0] if results else None
