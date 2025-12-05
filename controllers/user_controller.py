from flask import session, flash, redirect, url_for
from repositories.repository_factory import RepositoryFactory
from core.authentication import Authentication
from models.user import User
from datetime import datetime


class UserController:    
    @staticmethod
    def login(email, password):
        user_repo = RepositoryFactory.get_user_repository()
        patient_repo = RepositoryFactory.get_patient_repository()
        doctor_repo = RepositoryFactory.get_doctor_repository()
        
        password_hash = Authentication.hash_password(password)
        
        user = user_repo.find_by_email(email)
        if not user:
            user = patient_repo.find_by_email(email)
        if not user:
            user = doctor_repo.find_by_email(email)
        
        if user and Authentication.verify_password(password, user.password_hash):
            Authentication.login_user(user)
            return {'success': True, 'user': user}
        
        return {'success': False, 'message': 'Invalid email or password'}
    
    @staticmethod
    def logout():
        Authentication.logout_user()
        return {'success': True, 'message': 'Logged out successfully'}
    
    @staticmethod
    def register(email, password, first_name, last_name, user_type='patient', **kwargs):
        user_repo = RepositoryFactory.get_user_repository()
        patient_repo = RepositoryFactory.get_patient_repository()
        doctor_repo = RepositoryFactory.get_doctor_repository()
        
        existing_user = user_repo.find_by_email(email)
        if existing_user:
            return {'success': False, 'message': 'Email already registered'}
        
        password_hash = Authentication.hash_password(password)
        user_id = UserController._generate_user_id()
        
        if user_type == 'patient':
            from models.patient import Patient
            user = Patient(
                user_id=user_id,
                email=email,
                password_hash=password_hash,
                first_name=first_name,
                last_name=last_name,
                date_of_birth=kwargs.get('date_of_birth'),
                medical_history=kwargs.get('medical_history', [])
            )
            patient_repo.save(user)
        elif user_type == 'doctor':
            from models.doctor import Doctor
            user = Doctor(
                user_id=user_id,
                email=email,
                password_hash=password_hash,
                first_name=first_name,
                last_name=last_name,
                specialization=kwargs.get('specialization'),
                license_number=kwargs.get('license_number')
            )
            doctor_repo.save(user)
        else:
            user = User(
                user_id=user_id,
                email=email,
                password_hash=password_hash,
                first_name=first_name,
                last_name=last_name
            )
            user_repo.save(user)
        
        return {'success': True, 'user': user}
    
    @staticmethod
    def update_profile(user_id, **updates):
        user_repo = RepositoryFactory.get_user_repository()
        patient_repo = RepositoryFactory.get_patient_repository()
        doctor_repo = RepositoryFactory.get_doctor_repository()
        
        user = user_repo.get_by_id(user_id)
        repo_to_use = user_repo
        if not user:
            user = patient_repo.get_by_id(user_id)
            repo_to_use = patient_repo
        if not user:
            user = doctor_repo.get_by_id(user_id)
            repo_to_use = doctor_repo
        
        if not user:
            return {'success': False, 'message': 'User not found'}
        
        if 'first_name' in updates:
            user.first_name = updates['first_name']
        if 'last_name' in updates:
            user.last_name = updates['last_name']
        if 'email' in updates:
            user.email = updates['email']
        
        if hasattr(user, 'date_of_birth') and 'date_of_birth' in updates:
            user.date_of_birth = updates['date_of_birth']
        
        if hasattr(user, 'specialization') and 'specialization' in updates:
            user.specialization = updates['specialization']
        
        repo_to_use.save(user)
        
        return {'success': True, 'user': user}
    
    @staticmethod
    def get_profile(user_id):
        user_repo = RepositoryFactory.get_user_repository()
        patient_repo = RepositoryFactory.get_patient_repository()
        doctor_repo = RepositoryFactory.get_doctor_repository()
        
        user = user_repo.get_by_id(user_id)
        if not user:
            user = patient_repo.get_by_id(user_id)
        if not user:
            user = doctor_repo.get_by_id(user_id)
        
        if user:
            return {'success': True, 'user': user}
        return {'success': False, 'message': 'User not found'}
    
    @staticmethod
    def _generate_user_id():
        import uuid
        return str(uuid.uuid4())[:8]
