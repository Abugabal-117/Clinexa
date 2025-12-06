from datetime import datetime


class AppointmentRecord:
    def __init__(self, record_id, appointment_id, patient_id, doctor_id, 
                 diagnosis='', prescription='', notes='', created_date=None):
        self.record_id = record_id
        self.appointment_id = appointment_id
        self.patient_id = patient_id
        self.doctor_id = doctor_id
        self.diagnosis = diagnosis
        self.prescription = prescription
        self.notes = notes
        self.created_date = created_date or datetime.now()
    
    def to_dict(self):
        return {
            'record_id': self.record_id,
            'appointment_id': self.appointment_id,
            'patient_id': self.patient_id,
            'doctor_id': self.doctor_id,
            'diagnosis': self.diagnosis,
            'prescription': self.prescription,
            'notes': self.notes,
            'created_date': self.created_date.isoformat() if isinstance(self.created_date, datetime) else self.created_date
        }
    
    @classmethod
    def from_dict(cls, data):
        created_date = data.get('created_date')
        if created_date and isinstance(created_date, str):
            created_date = datetime.fromisoformat(created_date)
        
        return cls(
            record_id=data['record_id'],
            appointment_id=data['appointment_id'],
            patient_id=data['patient_id'],
            doctor_id=data['doctor_id'],
            diagnosis=data.get('diagnosis', ''),
            prescription=data.get('prescription', ''),
            notes=data.get('notes', ''),
            created_date=created_date
        )
    
    def __repr__(self):
        return f"<AppointmentRecord {self.record_id}>"
