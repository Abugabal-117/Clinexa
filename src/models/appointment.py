from datetime import datetime


class Appointment:
    def __init__(self, appointment_id, patient_id, doctor_id, appointment_date, 
                 appointment_time, status='pending', reason='', meeting_link='', 
                 created_date=None, updated_date=None):
        self.appointment_id = appointment_id
        self.patient_id = patient_id
        self.doctor_id = doctor_id
        self.appointment_date = appointment_date
        self.appointment_time = appointment_time
        self.status = status
        self.reason = reason
        self.meeting_link = meeting_link
        self.created_date = created_date or datetime.now()
        self.updated_date = updated_date or datetime.now()
    
    def to_dict(self):
        return {
            'appointment_id': self.appointment_id,
            'patient_id': self.patient_id,
            'doctor_id': self.doctor_id,
            'appointment_date': self.appointment_date if isinstance(self.appointment_date, str) else self.appointment_date.strftime('%Y-%m-%d'),
            'appointment_time': self.appointment_time if isinstance(self.appointment_time, str) else self.appointment_time.strftime('%H:%M'),
            'status': self.status,
            'reason': self.reason,
            'meeting_link': self.meeting_link,
            'created_date': self.created_date.isoformat() if isinstance(self.created_date, datetime) else self.created_date,
            'updated_date': self.updated_date.isoformat() if isinstance(self.updated_date, datetime) else self.updated_date
        }
    
    @classmethod
    def from_dict(cls, data):
        created_date = data.get('created_date')
        if created_date and isinstance(created_date, str):
            created_date = datetime.fromisoformat(created_date)
        
        updated_date = data.get('updated_date')
        if updated_date and isinstance(updated_date, str):
            updated_date = datetime.fromisoformat(updated_date)
        
        return cls(
            appointment_id=data['appointment_id'],
            patient_id=data['patient_id'],
            doctor_id=data['doctor_id'],
            appointment_date=data['appointment_date'],
            appointment_time=data['appointment_time'],
            status=data.get('status', 'pending'),
            reason=data.get('reason', ''),
            meeting_link=data.get('meeting_link', ''),
            created_date=created_date,
            updated_date=updated_date
        )
    
    def __repr__(self):
        return f"<Appointment {self.appointment_id} - {self.status}>"
