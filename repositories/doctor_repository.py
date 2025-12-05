from threading import Lock
from repositories.base_repository import BaseRepository
from models.doctor import Doctor


class DoctorRepository(BaseRepository):
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
        super().__init__('doctors.csv')
        self._initialized = True
    
    def get_fieldnames(self):
        return ['user_id', 'email', 'password_hash', 'first_name', 'last_name', 
                'created_at', 'is_active', 'specialization', 'license_number', 'patients', 'appointments']
    
    def to_model(self, data):
        return Doctor.from_dict(data)
    
    def find_by_email(self, email):
        results = self.find_by_field('email', email)
        return results[0] if results else None
    
    def find_by_specialization(self, specialization):
        return self.find_by_field('specialization', specialization)
