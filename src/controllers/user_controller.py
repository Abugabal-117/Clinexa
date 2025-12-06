from flask import session, flash, redirect, url_for
from repositories.repository_factory import RepositoryFactory
from core.authentication import Authentication
from models.user import User
from datetime import datetime


class UserController:    
    _login_attempts = {}

    @staticmethod
    def login(email, password):
        from datetime import datetime, timedelta
        
        if email in UserController._login_attempts:
            attempt_data = UserController._login_attempts[email]
            if attempt_data.get('lock_until') and datetime.now() < attempt_data['lock_until']:
                return {'success': False, 'message': 'Account locked. Try again later.'}
        
        user_repo = RepositoryFactory.get_user_repository()
        patient_repo = RepositoryFactory.get_patient_repository()
        doctor_repo = RepositoryFactory.get_doctor_repository()
        
        user = user_repo.find_by_email(email)
        if not user:
            user = patient_repo.find_by_email(email)
        if not user:
            user = doctor_repo.find_by_email(email)
        
        if user and Authentication.verify_password(password, user.password_hash):
            if email in UserController._login_attempts:
                del UserController._login_attempts[email]
                
            Authentication.login_user(user)
            return {'success': True, 'user': user}
        
        if email not in UserController._login_attempts:
            UserController._login_attempts[email] = {'count': 0, 'lock_until': None}
        
        UserController._login_attempts[email]['count'] += 1
        
        if UserController._login_attempts[email]['count'] >= 3:
            UserController._login_attempts[email]['lock_until'] = datetime.now() + timedelta(minutes=5)
            return {'success': False, 'message': 'Account locked for 5 minutes due to multiple failed attempts.'}
            
        return {'success': False, 'message': 'Invalid email or password'}
    
    @staticmethod
    def logout():
        Authentication.logout_user()
        return {'success': True, 'message': 'Logged out successfully'}
    
    @staticmethod
    def register(email, password, first_name, last_name, user_type='patient', **kwargs):
        if not email or '@' not in email:
            return {'success': False, 'message': 'Invalid email address'}
        if not password or len(password) < 8:
            return {'success': False, 'message': 'Password must be at least 8 characters'}
        if not first_name or not last_name:
            return {'success': False, 'message': 'First and last name are required'}
            
        user_repo = RepositoryFactory.get_user_repository()
        patient_repo = RepositoryFactory.get_patient_repository()
        doctor_repo = RepositoryFactory.get_doctor_repository()
        
        existing_user = user_repo.find_by_email(email) or \
                        patient_repo.find_by_email(email) or \
                        doctor_repo.find_by_email(email)
                        
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
                last_name=last_name,
                role=user_type
            )
            user_repo.save(user)
        
        return {'success': True, 'user': user}
    
    @staticmethod
    def update_profile(user_id, requesting_user_id=None, **updates):
        if requesting_user_id and requesting_user_id != user_id:
            return {'success': False, 'message': 'You can only update your own profile'}
        
        if 'email' in updates:
            if not updates['email'] or '@' not in updates['email']:
                return {'success': False, 'message': 'Invalid email address'}
        
        if 'first_name' in updates:
            if not updates['first_name'] or len(updates['first_name'].strip()) == 0:
                return {'success': False, 'message': 'First name cannot be empty'}
        
        if 'last_name' in updates:
            if not updates['last_name'] or len(updates['last_name'].strip()) == 0:
                return {'success': False, 'message': 'Last name cannot be empty'}
        
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
