from functools import wraps
from flask import session, redirect, url_for, flash

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user' not in session:
            flash('Please login to access this page', 'error')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def patient_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user' not in session:
            flash('Please login to access this page', 'error')
            return redirect(url_for('login'))
        if session['user'].get('role') != 'patient':
            flash('This page is only for patients', 'error')
            return redirect(url_for('dashboard'))
        return f(*args, **kwargs)
    return decorated_function

def get_current_user():
    return session.get('user')

def is_logged_in():
    return 'user' in session

def refresh_session_user(user_id):
    from controllers.user_controller import UserController
    result = UserController.get_profile(user_id)
    if result['success']:
        user = result['user']
        session['user'] = {
            'id': user.user_id,
            'name': user.get_full_name(),
            'role': user.role,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name
        }
        return True
    return False
