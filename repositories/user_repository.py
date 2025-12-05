from threading import Lock
from repositories.base_repository import BaseRepository
from models.user import User


class UserRepository(BaseRepository):
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
        super().__init__('users.csv')
        self._initialized = True
    
    def get_fieldnames(self):
        return ['user_id', 'email', 'password_hash', 'first_name', 'last_name', 'role', 'created_at', 'is_active']
    
    def to_model(self, data):
        return User.from_dict(data)
    
    def find_by_email(self, email):
        results = self.find_by_field('email', email)
        return results[0] if results else None
    
    def authenticate(self, email, password_hash):
        user = self.find_by_email(email)
        if user and user.password_hash == password_hash:
            return user
        return None
