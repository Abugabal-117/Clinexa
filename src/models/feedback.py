from datetime import datetime

class Feedback:
    def __init__(self, feedback_id, patient_id, doctor_id, rating, comment='', created_at=None):
        self.feedback_id = feedback_id
        self.patient_id = patient_id
        self.doctor_id = doctor_id
        self.rating = rating
        self.comment = comment
        self.created_at = created_at or datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    @classmethod
    def from_dict(cls, data):
        return cls(
            feedback_id=data.get('feedback_id'),
            patient_id=data.get('patient_id'),
            doctor_id=data.get('doctor_id'),
            rating=int(data.get('rating')),
            comment=data.get('comment', ''),
            created_at=data.get('created_at')
        )

    def to_dict(self):
        return {
            'feedback_id': self.feedback_id,
            'patient_id': self.patient_id,
            'doctor_id': self.doctor_id,
            'rating': self.rating,
            'comment': self.comment,
            'created_at': self.created_at
        }
