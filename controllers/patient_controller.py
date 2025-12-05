from repositories.repository_factory import RepositoryFactory
from models.patient import Patient
from datetime import datetime


class PatientController:
    @staticmethod
    def create_patient(email, password_hash, first_name, last_name, date_of_birth=None, **kwargs):
        patient_repo = RepositoryFactory.get_patient_repository()
        
        existing = patient_repo.find_by_email(email)
        if existing:
            return {'success': False, 'message': 'Patient already exists'}
        
        import uuid
        patient_id = str(uuid.uuid4())[:8]
        
        patient = Patient(
            user_id=patient_id,
            email=email,
            password_hash=password_hash,
            first_name=first_name,
            last_name=last_name,
            date_of_birth=date_of_birth,
            medical_history=kwargs.get('medical_history', [])
        )
        
        patient_repo.save(patient)
        return {'success': True, 'patient': patient}
    
    @staticmethod
    def get_patient(patient_id):
        patient_repo = RepositoryFactory.get_patient_repository()
        patient = patient_repo.get_by_id(patient_id)
        
        if patient:
            return {'success': True, 'patient': patient}
        return {'success': False, 'message': 'Patient not found'}
    
    @staticmethod
    def get_all_patients():
        patient_repo = RepositoryFactory.get_patient_repository()
        patients = patient_repo.get_all()
        return {'success': True, 'patients': patients}
    
    @staticmethod
    def update_patient(patient_id, **updates):
        patient_repo = RepositoryFactory.get_patient_repository()
        patient = patient_repo.get_by_id(patient_id)
        
        if not patient:
            return {'success': False, 'message': 'Patient not found'}
        
        if 'first_name' in updates:
            patient.first_name = updates['first_name']
        if 'last_name' in updates:
            patient.last_name = updates['last_name']
        if 'email' in updates:
            patient.email = updates['email']
        if 'date_of_birth' in updates:
            patient.date_of_birth = updates['date_of_birth']
        
        patient_repo.save(patient)
        return {'success': True, 'patient': patient}
    
    @staticmethod
    def delete_patient(patient_id):
        patient_repo = RepositoryFactory.get_patient_repository()
        patient = patient_repo.get_by_id(patient_id)
        
        if not patient:
            return {'success': False, 'message': 'Patient not found'}
        
        patient.is_active = False
        patient_repo.save(patient)
        return {'success': True, 'message': 'Patient archived successfully'}
    
    @staticmethod
    def add_medical_record(patient_id, record):
        patient_repo = RepositoryFactory.get_patient_repository()
        patient = patient_repo.get_by_id(patient_id)
        
        if not patient:
            return {'success': False, 'message': 'Patient not found'}
        
        patient.add_medical_record(record)
        patient_repo.save(patient)
        return {'success': True, 'patient': patient}
    
    @staticmethod
    def get_medical_history(patient_id):
        patient_repo = RepositoryFactory.get_patient_repository()
        patient = patient_repo.get_by_id(patient_id)
        
        if not patient:
            return {'success': False, 'message': 'Patient not found'}
        
        return {'success': True, 'medical_history': patient.medical_history}
    
    @staticmethod
    def get_appointments(patient_id):
        appointment_repo = RepositoryFactory.get_appointment_repository()
        appointments = appointment_repo.find_by_patient(patient_id)
        return {'success': True, 'appointments': appointments}
    
    @staticmethod
    def book_appointment(patient_id, doctor_id, appointment_date, appointment_time, reason=''):
        appointment_repo = RepositoryFactory.get_appointment_repository()
        patient_repo = RepositoryFactory.get_patient_repository()
        doctor_repo = RepositoryFactory.get_doctor_repository()
        
        patient = patient_repo.get_by_id(patient_id)
        if not patient:
            return {'success': False, 'message': 'Patient not found'}
        
        doctor = doctor_repo.get_by_id(doctor_id)
        if not doctor:
            return {'success': False, 'message': 'Doctor not found'}
        
        existing_appointments = appointment_repo.find_by_date(appointment_date)
        for apt in existing_appointments:
            if apt.doctor_id == doctor_id and apt.appointment_time == appointment_time and apt.status != 'cancelled':
                return {'success': False, 'message': 'Time slot not available'}
        
        from models.appointment import Appointment
        import uuid
        appointment_id = str(uuid.uuid4())[:8]
        
        appointment = Appointment(
            appointment_id=appointment_id,
            patient_id=patient_id,
            doctor_id=doctor_id,
            appointment_date=appointment_date,
            appointment_time=appointment_time,
            status='confirmed',
            reason=reason
        )
        
        appointment_repo.save(appointment)
        
        # Prototype: Send notification to doctor
        from controllers.notification_controller import NotificationController
        NotificationController.send_notification(
            recipient_id=doctor_id,
            message=f"New appointment booked by {patient.first_name} {patient.last_name} for {appointment_date} at {appointment_time}"
        )
        # Notify patient
        NotificationController.send_notification(
            recipient_id=patient_id,
            message=f"Appointment confirmed with Dr. {doctor.last_name} on {appointment_date} at {appointment_time}"
        )
        
        return {'success': True, 'appointment': appointment}

    @staticmethod
    def search_doctors(query):
        # Delegate to DoctorController or implement here
        # For prototype completeness, we'll implement a direct call or rely on DoctorController
        from controllers.doctor_controller import DoctorController
        return DoctorController.search_doctors(query=query)
    
    @staticmethod
    def cancel_appointment(appointment_id):
        appointment_repo = RepositoryFactory.get_appointment_repository()
        appointment = appointment_repo.get_by_id(appointment_id)
        
        if not appointment:
            return {'success': False, 'message': 'Appointment not found'}
        
        appointment.status = 'cancelled'
        appointment.updated_date = datetime.now()
        appointment_repo.save(appointment)
        return {'success': True, 'message': 'Appointment cancelled'}
    
    @staticmethod
    def search_patients(query):
        patient_repo = RepositoryFactory.get_patient_repository()
        all_patients = patient_repo.get_all()
        
        results = []
        query_lower = query.lower()
        for patient in all_patients:
            if (query_lower in patient.first_name.lower() or 
                query_lower in patient.last_name.lower() or 
                query_lower in patient.email.lower()):
                results.append(patient)
        
        return {'success': True, 'patients': results}

    @staticmethod
    def submit_feedback(patient_id, doctor_id, rating, comment=''):
        from models.feedback import Feedback
        import uuid
        
        feedback_repo = RepositoryFactory.get_feedback_repository()
        
        feedback_id = str(uuid.uuid4())[:8]
        feedback = Feedback(
            feedback_id=feedback_id,
            patient_id=patient_id,
            doctor_id=doctor_id,
            rating=rating,
            comment=comment
        )
        
        feedback_repo.save(feedback)
        return {'success': True, 'feedback': feedback}
