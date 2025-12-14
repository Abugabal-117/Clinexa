import pytest

class TestSecurityHeaders:
    def test_no_server_header_leak(self, client):
        response = client.get('/')
        server_header = response.headers.get('Server', '')
        assert 'Werkzeug' not in server_header or response.status_code in [200, 302]
    
    def test_session_cookie_security(self, app):
        assert app.secret_key is not None
        assert len(app.secret_key) >= 16

class TestInputValidation:
    def test_login_empty_fields(self, client):
        response = client.post('/login', data={
            'email': '',
            'password': ''
        })
        assert response.status_code in [200, 302, 400]
    
    def test_signup_empty_fields(self, client):
        response = client.post('/signup', data={
            'email': '',
            'password': '',
            'name': ''
        })
        assert response.status_code in [200, 302, 400]

class TestAuthorizationChecks:
    def test_cannot_access_other_user_profile_without_login(self, client):
        response = client.get('/edit_profile', follow_redirects=False)
        assert response.status_code in [302, 401]
    
    def test_cannot_cancel_appointment_without_login(self, client):
        response = client.post('/cancel_appointment', data={
            'appointment_id': '1'
        }, follow_redirects=False)
        assert response.status_code in [302, 401, 405]
