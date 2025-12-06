from datetime import datetime


class User:
    def __init__(self, user_id, email, password_hash, first_name, last_name, role='user', created_at=None, is_active=True):
        self.user_id = user_id
        self.email = email
        self.password_hash = password_hash
        self.first_name = first_name
        self.last_name = last_name
        self.role = role
        self.created_at = created_at or datetime.now()
        self.is_active = is_active
    
    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"
    
    def to_dict(self):
        return {
            'user_id': self.user_id,
            'email': self.email,
            'password_hash': self.password_hash,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'role': self.role,
            'created_at': self.created_at.isoformat() if isinstance(self.created_at, datetime) else self.created_at,
            'is_active': str(self.is_active)
        }
    
    @classmethod
    def from_dict(cls, data):
        created_at = data.get('created_at')
        if created_at and isinstance(created_at, str):
            created_at = datetime.fromisoformat(created_at)
        
        return cls(
            user_id=data['user_id'],
            email=data['email'],
            password_hash=data['password_hash'],
            first_name=data['first_name'],
            last_name=data['last_name'],
            role=data.get('role', 'user'),
            created_at=created_at,
            is_active=data.get('is_active', 'True') == 'True'
        )
    
    def __repr__(self):
        return f"<User {self.email}>"
