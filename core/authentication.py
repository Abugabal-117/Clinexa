import hashlib
from functools import wraps
from flask import session, redirect, url_for


class Authentication:
    @staticmethod
    def hash_password(password):
        return hashlib.sha256(password.encode()).hexdigest()
    
    @staticmethod
    def verify_password(password, password_hash):
        return Authentication.hash_password(password) == password_hash
    
    @staticmethod
    def login_user(user):
        session['user_id'] = user.user_id
        session['email'] = user.email
        session['logged_in'] = True
    
    @staticmethod
    def logout_user():
        session.clear()
    
    @staticmethod
    def is_authenticated():
        return session.get('logged_in', False)
    
    @staticmethod
    def login_required(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not Authentication.is_authenticated():
                return redirect(url_for('login'))
            return f(*args, **kwargs)
        return decorated_function

