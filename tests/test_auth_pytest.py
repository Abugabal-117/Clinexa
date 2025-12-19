import pytest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../src'))

from core.authentication import Authentication


class TestPasswordHashing:
    
    def test_hash_password_creates_valid_hash(self):
        password = "MySecurePassword123"
        hash_result = Authentication.hash_password(password)
        
        assert len(hash_result) == 64
        assert isinstance(hash_result, str)
    
    def test_hash_password_consistency(self):
        password = "ConsistentPassword"
        hash1 = Authentication.hash_password(password)
        hash2 = Authentication.hash_password(password)
        
        assert hash1 == hash2
        
    def test_hash_password_different_passwords_different_hashes(self):
        password1 = "FirstPassword123"
        password2 = "SecondPassword456"
        
        hash1 = Authentication.hash_password(password1)
        hash2 = Authentication.hash_password(password2)
        
        assert hash1 != hash2


class TestPasswordVerification:
    
    def test_verify_password_correct_password(self):
        password = "CorrectPassword123"
        password_hash = Authentication.hash_password(password)
        
        result = Authentication.verify_password(password, password_hash)
        assert result is True
    
    def test_verify_password_incorrect_password(self):
        correct_password = "CorrectPassword123"
        wrong_password = "WrongPassword456"
        password_hash = Authentication.hash_password(correct_password)
        
        result = Authentication.verify_password(wrong_password, password_hash)
        assert result is False
    
    def test_verify_password_empty_password(self):
        password_hash = Authentication.hash_password("NonEmptyPassword")
        
        result = Authentication.verify_password("", password_hash)
        assert result is False
        
    def test_verify_password_case_sensitive(self):
        password = "CaseSensitive123"
        password_hash = Authentication.hash_password(password)
        
        result = Authentication.verify_password("casesensitive123", password_hash)
        assert result is False
