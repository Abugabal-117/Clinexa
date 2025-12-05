from threading import Lock
from repositories.base_repository import BaseRepository
from models.feedback import Feedback

class FeedbackRepository(BaseRepository):
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
        super().__init__('feedback.csv', 'feedback_id')
        self._initialized = True

    def get_fieldnames(self):
        return ['feedback_id', 'patient_id', 'doctor_id', 'rating', 'comment', 'created_at']

    def to_model(self, data):
        return Feedback.from_dict(data)

    def find_by_doctor(self, doctor_id):
        return self.find_by_field('doctor_id', doctor_id)
        
    def find_by_patient(self, patient_id):
        return self.find_by_field('patient_id', patient_id)
