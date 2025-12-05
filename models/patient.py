import json
from models.user import User


class Patient(User):
    def __init__(self, user_id, email, password_hash, first_name, last_name, 
                 date_of_birth=None, medical_history=None, appointments=None, **kwargs):
        super().__init__(user_id, email, password_hash, first_name, last_name, 
                        role='patient', created_at=kwargs.get('created_at'), is_active=kwargs.get('is_active', True))
        self.date_of_birth = date_of_birth
        self.medical_history = medical_history or []
        self.appointments = appointments or []
    
    def add_medical_record(self, record):
        self.medical_history.append(record)
    
    def to_dict(self):
        data = super().to_dict()
        data.update({
            'date_of_birth': self.date_of_birth or '',
            'medical_history': json.dumps(self.medical_history),
            'appointments': json.dumps(self.appointments)
        })
        return data
    
    @classmethod
    def from_dict(cls, data):
        medical_history = json.loads(data.get('medical_history', '[]'))
        appointments = json.loads(data.get('appointments', '[]'))
        
        return cls(
            user_id=data['user_id'],
            email=data['email'],
            password_hash=data['password_hash'],
            first_name=data['first_name'],
            last_name=data['last_name'],
            date_of_birth=data.get('date_of_birth') or None,
            medical_history=medical_history,
            appointments=appointments,
            created_at=data.get('created_at'),
            is_active=data.get('is_active', 'True') == 'True'
        )
    
    def __repr__(self):
        return f"<Patient {self.email}>"
