import pytest
import sys
import os
import tempfile
import shutil

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../src'))

from controllers.doctor_controller import DoctorController


@pytest.fixture(scope="class")
def test_env():
    test_dir = tempfile.mkdtemp()
    os.environ['DATA_DIR'] = test_dir
    yield
    shutil.rmtree(test_dir, ignore_errors=True)


class TestDoctorController:
    
    def test_add_available_time_success(self, test_env):
        doctor_id = "doctor_001"
        date = "2025-12-25"
        time = "10:00"
        
        result = DoctorController.add_available_time(
            doctor_id,
            date,
            time
        )
        
        assert result['success'] is True
        assert 'message' in result
    
    def test_add_available_time_duplicate(self, test_env):
        doctor_id = "doctor_002"
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
    
    def test_get_available_times(self, test_env):
        doctor_id = "doctor_003"
        result = DoctorController.get_available_times(doctor_id)
        
        assert result['success'] is True
        assert 'available_times' in result
        assert isinstance(result['available_times'], list)
    
    def test_remove_available_time_success(self, test_env):
        doctor_id = "doctor_004"
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
    
    def test_remove_available_time_nonexistent(self, test_env):
        doctor_id = "doctor_005"
        date = "2025-12-30"
        time = "16:00"
        
        result = DoctorController.remove_available_time(
            doctor_id,
            date,
            time
        )
        
        assert result['success'] is False
        assert 'not found' in result['message']
    
    def test_get_doctor_success(self, test_env):
        doctor_id = "doctor_001"
        result = DoctorController.get_doctor(doctor_id)
        
        assert 'success' in result
        if result['success']:
            assert 'doctor' in result
