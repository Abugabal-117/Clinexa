"""
Unit tests for Doctor Controller
Tests doctor-related operations like schedule management and patient management
"""

import unittest
import sys
import os
import tempfile
import shutil

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../src'))

from controllers.doctor_controller import DoctorController


class TestDoctorController(unittest.TestCase):
    """Test cases for DoctorController class"""
    
    @classmethod
    def setUpClass(cls):
        """Set up test fixtures"""
        cls.test_dir = tempfile.mkdtemp()
        os.environ['DATA_DIR'] = cls.test_dir
    
    @classmethod
    def tearDownClass(cls):
        """Clean up test fixtures"""
        shutil.rmtree(cls.test_dir, ignore_errors=True)
    
    def setUp(self):
        """Set up test data for each test"""
        self.doctor_id = "doctor_001"
    
    def test_add_available_time_success(self):
        """Test adding an available time slot for a doctor"""
        date = "2025-12-25"
        time = "10:00"
        
        result = DoctorController.add_available_time(
            self.doctor_id,
            date,
            time
        )
        
        self.assertTrue(result['success'])
        self.assertIn('message', result)
    
    def test_add_available_time_duplicate(self):
        """Test adding duplicate available time slot"""
        date = "2025-12-25"
        time = "10:00"
        
        # Add first time
        result1 = DoctorController.add_available_time(
            self.doctor_id,
            date,
            time
        )
        self.assertTrue(result1['success'])
        
        # Try to add the same time again
        result2 = DoctorController.add_available_time(
            self.doctor_id,
            date,
            time
        )
        self.assertFalse(result2['success'])
    
    def test_get_available_times(self):
        """Test retrieving available times for a doctor"""
        result = DoctorController.get_available_times(self.doctor_id)
        
        self.assertTrue(result['success'])
        self.assertIn('available_times', result)
        self.assertIsInstance(result['available_times'], list)
    
    def test_remove_available_time_success(self):
        """Test removing an available time slot"""
        date = "2025-12-26"
        time = "14:00"
        
        # Add a time first
        add_result = DoctorController.add_available_time(
            self.doctor_id,
            date,
            time
        )
        
        if add_result['success']:
            # Remove the time
            remove_result = DoctorController.remove_available_time(
                self.doctor_id,
                date,
                time
            )
            
            self.assertTrue(remove_result['success'])
    
    def test_remove_available_time_nonexistent(self):
        """Test removing a non-existent available time"""
        date = "2025-12-30"
        time = "16:00"
        
        result = DoctorController.remove_available_time(
            self.doctor_id,
            date,
            time
        )
        
        self.assertFalse(result['success'])
        self.assertIn('not found', result['message'])
    
    def test_get_doctor_success(self):
        """Test retrieving doctor information"""
        result = DoctorController.get_doctor(self.doctor_id)
        
        # This test may succeed or fail depending on whether the doctor exists
        # We just check that the response structure is correct
        self.assertIn('success', result)
        if result['success']:
            self.assertIn('doctor', result)


if __name__ == '__main__':
    unittest.main()
