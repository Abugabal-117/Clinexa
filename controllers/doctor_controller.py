from repositories.repository_factory import RepositoryFactory
from models.doctor import Doctor
from datetime import datetime


class DoctorController:
    @staticmethod
    def create_doctor(email, password_hash, first_name, last_name, specialization, license_number, **kwargs):
        doctor_repo = RepositoryFactory.get_doctor_repository()
        
        existing = doctor_repo.find_by_email(email)
        if existing:
            return {'success': False, 'message': 'Doctor already exists'}
        
        import uuid
        doctor_id = str(uuid.uuid4())[:8]
        
        doctor = Doctor(
            user_id=doctor_id,
            email=email,
            password_hash=password_hash,
            first_name=first_name,
            last_name=last_name,
            specialization=specialization,
            license_number=license_number
        )
        
        doctor_repo.save(doctor)
        return {'success': True, 'doctor': doctor}
    
    @staticmethod
    def get_doctor(doctor_id):
        doctor_repo = RepositoryFactory.get_doctor_repository()
        doctor = doctor_repo.get_by_id(doctor_id)
        
        if doctor:
            return {'success': True, 'doctor': doctor}
        return {'success': False, 'message': 'Doctor not found'}
    
    @staticmethod
    def get_all_doctors():
        doctor_repo = RepositoryFactory.get_doctor_repository()
        doctors = doctor_repo.get_all()
        return {'success': True, 'doctors': doctors}
    
    @staticmethod
    def update_doctor(doctor_id, **updates):
        doctor_repo = RepositoryFactory.get_doctor_repository()
        doctor = doctor_repo.get_by_id(doctor_id)
        
        if not doctor:
            return {'success': False, 'message': 'Doctor not found'}
        
        if 'first_name' in updates:
            doctor.first_name = updates['first_name']
        if 'last_name' in updates:
            doctor.last_name = updates['last_name']
        if 'email' in updates:
            doctor.email = updates['email']
        if 'specialization' in updates:
            doctor.specialization = updates['specialization']
        if 'license_number' in updates:
            doctor.license_number = updates['license_number']
        
        doctor_repo.save(doctor)
        return {'success': True, 'doctor': doctor}
    
    @staticmethod
    def delete_doctor(doctor_id):
        doctor_repo = RepositoryFactory.get_doctor_repository()
        doctor = doctor_repo.get_by_id(doctor_id)
        
        if not doctor:
            return {'success': False, 'message': 'Doctor not found'}
        
        doctor.is_active = False
        doctor_repo.save(doctor)
        return {'success': True, 'message': 'Doctor archived successfully'}
    
    @staticmethod
    def get_appointments(doctor_id, date=None):
        appointment_repo = RepositoryFactory.get_appointment_repository()
        appointments = appointment_repo.find_by_doctor(doctor_id)
        
        if date:
            appointments = [apt for apt in appointments if apt.appointment_date == date]
        
        return {'success': True, 'appointments': appointments}
    
    @staticmethod
    def get_todays_appointments(doctor_id):
        today = datetime.now().strftime('%Y-%m-%d')
        return DoctorController.get_appointments(doctor_id, today)
    
    @staticmethod
    def add_patient(doctor_id, patient_id):
        doctor_repo = RepositoryFactory.get_doctor_repository()
        patient_repo = RepositoryFactory.get_patient_repository()
        
        doctor = doctor_repo.get_by_id(doctor_id)
        if not doctor:
            return {'success': False, 'message': 'Doctor not found'}
        
        patient = patient_repo.get_by_id(patient_id)
        if not patient:
            return {'success': False, 'message': 'Patient not found'}
        
        doctor.add_patient(patient_id)
        doctor_repo.save(doctor)
        return {'success': True, 'doctor': doctor}
    
    @staticmethod
    def get_patients(doctor_id):
        doctor_repo = RepositoryFactory.get_doctor_repository()
        doctor = doctor_repo.get_by_id(doctor_id)
        
        if not doctor:
            return {'success': False, 'message': 'Doctor not found'}
        
        patient_repo = RepositoryFactory.get_patient_repository()
        patients = []
        for patient_id in doctor.patients:
            patient = patient_repo.get_by_id(patient_id)
            if patient:
                patients.append(patient)
        
        return {'success': True, 'patients': patients}
    
    @staticmethod
    def create_medical_record(doctor_id, patient_id, appointment_id, diagnosis, prescription, notes=''):
        from models.appointment_record import AppointmentRecord
        record_repo = RepositoryFactory.get_appointment_record_repository()
        
        doctor = DoctorController.get_doctor(doctor_id)
        if not doctor['success']:
            return doctor
        
        import uuid
        record_id = str(uuid.uuid4())[:8]
        
        record = AppointmentRecord(
            record_id=record_id,
            appointment_id=appointment_id,
            patient_id=patient_id,
            doctor_id=doctor_id,
            diagnosis=diagnosis,
            prescription=prescription,
            notes=notes
        )
        
        record_repo.save(record)
        return {'success': True, 'record': record}
    
    @staticmethod
    def get_medical_records(doctor_id, patient_id=None):
        record_repo = RepositoryFactory.get_appointment_record_repository()
        
        if patient_id:
            records = record_repo.find_by_patient(patient_id)
            records = [r for r in records if r.doctor_id == doctor_id]
        else:
            records = record_repo.find_by_doctor(doctor_id)
        
        return {'success': True, 'records': records}
    
    @staticmethod
    def view_patient_history(doctor_id, patient_id):
        patient_repo = RepositoryFactory.get_patient_repository()
        record_repo = RepositoryFactory.get_appointment_record_repository()
        
        patient = patient_repo.get_by_id(patient_id)
        if not patient:
            return {'success': False, 'message': 'Patient not found'}
        
        records = record_repo.find_by_patient(patient_id)
        
        return {
            'success': True,
            'patient': patient,
            'medical_history': patient.medical_history,
            'appointment_records': records
        }
    
    @staticmethod
    def search_doctors(specialization=None, query=None):
        doctor_repo = RepositoryFactory.get_doctor_repository()
        
        if specialization:
            doctors = doctor_repo.find_by_specialization(specialization)
        else:
            doctors = doctor_repo.get_all()
        
        if query:
            query_lower = query.lower()
            doctors = [d for d in doctors if 
                      query_lower in d.first_name.lower() or 
                      query_lower in d.last_name.lower() or 
                      query_lower in d.email.lower()]
        
        return {'success': True, 'doctors': doctors}
    
    @staticmethod
    def generate_report(doctor_id, report_type='workload', start_date=None, end_date=None):
        appointment_repo = RepositoryFactory.get_appointment_repository()
        appointments = appointment_repo.find_by_doctor(doctor_id)
        
        if start_date:
            appointments = [a for a in appointments if a.appointment_date >= start_date]
        if end_date:
            appointments = [a for a in appointments if a.appointment_date <= end_date]
        
        report_data = {
            'doctor_id': doctor_id,
            'report_type': report_type,
            'total_appointments': len(appointments),
            'confirmed': len([a for a in appointments if a.status == 'confirmed']),
            'completed': len([a for a in appointments if a.status == 'completed']),
            'cancelled': len([a for a in appointments if a.status == 'cancelled']),
            'appointments': appointments
        }
        
        return {'success': True, 'report': report_data}

    @staticmethod
    def get_feedback(doctor_id):
        feedback_repo = RepositoryFactory.get_feedback_repository()
        feedback = feedback_repo.find_by_doctor(doctor_id)
        return {'success': True, 'feedback': feedback}

    @staticmethod
    def cancel_appointment(appointment_id):
        appointment_repo = RepositoryFactory.get_appointment_repository()
        appointment = appointment_repo.get_by_id(appointment_id)
        
        if not appointment:
            return {'success': False, 'message': 'Appointment not found'}
        
        appointment.status = 'cancelled'
        appointment.updated_date = datetime.now()
        appointment_repo.save(appointment)
        
        # Notify patient
        from controllers.notification_controller import NotificationController
        NotificationController.send_notification(
            recipient_id=appointment.patient_id,
            message=f"Your appointment on {appointment.appointment_date} has been cancelled by Dr.{appointment.doctor_id}" # Ideally get name
        )
        
        return {'success': True, 'message': 'Appointment cancelled'}
