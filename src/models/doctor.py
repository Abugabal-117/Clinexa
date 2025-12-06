import json
from models.user import User


class Doctor(User):
    def __init__(self, user_id, email, password_hash, first_name, last_name,
                 specialization=None, license_number=None, patients=None, appointments=None, **kwargs):
        super().__init__(user_id, email, password_hash, first_name, last_name,
                        role='doctor', created_at=kwargs.get('created_at'), is_active=kwargs.get('is_active', True))
        self.specialization = specialization
        self.license_number = license_number
        self.patients = patients or []
        self.appointments = appointments or []
    
    def add_patient(self, patient):
        if patient not in self.patients:
            self.patients.append(patient)
    
    def to_dict(self):
        data = super().to_dict()
        data.update({
            'specialization': self.specialization or '',
            'license_number': self.license_number or '',
            'patients': json.dumps(self.patients),
            'appointments': json.dumps(self.appointments)
        })
        return data
    
    @classmethod
    def from_dict(cls, data):
        patients = json.loads(data.get('patients', '[]'))
        appointments = json.loads(data.get('appointments', '[]'))
        
        return cls(
            user_id=data['user_id'],
            email=data['email'],
            password_hash=data['password_hash'],
            first_name=data['first_name'],
            last_name=data['last_name'],
            specialization=data.get('specialization') or None,
            license_number=data.get('license_number') or None,
            patients=patients,
            appointments=appointments,
            created_at=data.get('created_at'),
            is_active=data.get('is_active', 'True') == 'True'
        )
    
    def __repr__(self):
        return f"<Doctor {self.email} - {self.specialization}>"
