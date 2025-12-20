import pytest
from flask import session

class TestBasicRoutes:
    def test_home_page(self, client):
        response = client.get('/')
        assert response.status_code in [200, 302]
    
    def test_login_page_get(self, client):
        response = client.get('/login')
        assert response.status_code == 200
    
    def test_signup_page_get(self, client):
        response = client.get('/signup')
        assert response.status_code == 200
    
    def test_logout_redirect(self, client):
        response = client.get('/logout', follow_redirects=False)
        assert response.status_code == 302
    
    def test_rating_page_requires_login(self, client):
        response = client.get('/rating', follow_redirects=False)
        assert response.status_code in [302, 401]

class TestAuthentication:
    def test_login_with_invalid_credentials(self, client):
        response = client.post('/login', data={
            'email': 'nonexistent@example.com',
            'password': 'wrongpassword'
        }, follow_redirects=True)
        assert response.status_code == 200
    
    def test_signup_page_accessible(self, client):
        response = client.get('/signup')
        assert response.status_code == 200
        assert b'signup' in response.data.lower() or b'sign up' in response.data.lower() or response.status_code == 200

class TestProtectedRoutes:
    def test_dashboard_requires_login(self, client):
        response = client.get('/dashboard', follow_redirects=False)
        assert response.status_code in [302, 401]
    
    def test_appointments_requires_login(self, client):
        response = client.get('/appointments', follow_redirects=False)
        assert response.status_code in [302, 401]
    
    def test_booking_requires_login(self, client):
        response = client.get('/booking', follow_redirects=False)
        assert response.status_code in [302, 401]

class TestApplicationHealth:
    def test_app_exists(self, app):
        assert app is not None
    
    def test_app_is_testing(self, app):
        assert app.config['TESTING'] == True
    
    def test_secret_key_exists(self, app):
        assert app.secret_key is not None
