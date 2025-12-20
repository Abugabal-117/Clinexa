import pytest
import sys
import os
import tempfile
import shutil

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../src'))

from controllers.doctor_controller import DoctorController
from models.doctor import Doctor
from core.authentication import Authentication
from repositories.repository_factory import RepositoryFactory


@pytest.fixture
def test_env():
    test_dir = tempfile.mkdtemp()
    os.environ['DATA_DIR'] = test_dir
    yield
    shutil.rmtree(test_dir, ignore_errors=True)


@pytest.fixture
def setup_doctor(test_env):
    """Create a doctor for testing"""
    doctor_id = "doctor_001"
    doctor_repo = RepositoryFactory.get_doctor_repository()
    doctor = Doctor(
        user_id=doctor_id,
        email="testdoctor@example.com",
        password_hash=Authentication.hash_password("TestPassword123"),
        first_name="Test",
        last_name="Doctor",
        specialization="General Practice"
    )
    doctor_repo.save(doctor)
    return doctor_id


class TestDoctorController:
    
    def test_add_available_time_success(self, setup_doctor):
        doctor_id = setup_doctor
        date = "2025-12-25"
        time = "10:00"
        
        result = DoctorController.add_available_time(
            doctor_id,
            date,
            time
        )
        
        assert result['success'] is True
        assert 'message' in result
    
    def test_add_available_time_duplicate(self, setup_doctor):
        doctor_id = setup_doctor
        date = "2025-12-25"
        time = "10:00"
        
        result1 = DoctorController.add_available_time(
            doctor_id,
            date,
            time
        )
        assert result1['success'] is True
        
        result2 = DoctorController.add_available_time(
            doctor_id,
            date,
            time
        )
        assert result2['success'] is False
    
    def test_get_available_times(self, setup_doctor):
        doctor_id = setup_doctor
        result = DoctorController.get_available_times(doctor_id)
        
        assert result['success'] is True
        assert 'available_times' in result
        assert isinstance(result['available_times'], list)
    
    def test_remove_available_time_success(self, setup_doctor):
        doctor_id = setup_doctor
        date = "2025-12-26"
        time = "14:00"
        
        add_result = DoctorController.add_available_time(
            doctor_id,
            date,
            time
        )
        
        if add_result['success']:
            remove_result = DoctorController.remove_available_time(
                doctor_id,
                date,
                time
            )
            
            assert remove_result['success'] is True
    
    def test_remove_available_time_nonexistent(self, setup_doctor):
        doctor_id = setup_doctor
        date = "2025-12-30"
        time = "16:00"
        
        result = DoctorController.remove_available_time(
            doctor_id,
            date,
            time
        )
        
        assert result['success'] is False
        assert 'not found' in result['message']
    
    def test_get_doctor_success(self, setup_doctor):
        doctor_id = setup_doctor
        result = DoctorController.get_doctor(doctor_id)
        
        assert 'success' in result
        if result['success']:
            assert 'doctor' in result
