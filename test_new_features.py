#!/usr/bin/env python3
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from controllers.notification_controller import NotificationController
from controllers.patient_controller import PatientController
from controllers.doctor_controller import DoctorController
from repositories.repository_factory import RepositoryFactory

def test_notifications():
    print("=== Testing Notifications ===")
    user_id = "test_user_123"
    message = "Your appointment is confirmed"
    
    # Test Send
    result = NotificationController.send_notification(user_id, message)
    print(f"Send Notification: {result['success']}")
    notification_id = result['notification'].notification_id
    
    # Test Get
    result = NotificationController.get_notifications(user_id)
    notifications = result['notifications']
    print(f"Get Notifications: {len(notifications)} found")
    
    # Test Mark Read
    result = NotificationController.mark_read(notification_id)
    print(f"Mark Read: {result['success']}")
    
    result = NotificationController.get_notifications(user_id)
    print(f"Status After Mark Read: {result['notifications'][0].status}")
    print()

def test_feedback():
    print("=== Testing Feedback ===")
    patient_id = "pat_123"
    doctor_id = "doc_123"
    
    # Test Submit
    result = PatientController.submit_feedback(
        patient_id=patient_id,
        doctor_id=doctor_id,
        rating=5,
        comment="Great doctor!"
    )
    print(f"Submit Feedback: {result['success']}")
    
    # Test Get
    result = DoctorController.get_feedback(doctor_id)
    feedbacks = result['feedback']
    print(f"Get Feedback: {len(feedbacks)} found")
    if feedbacks:
        print(f"Rating: {feedbacks[0].rating}, Comment: {feedbacks[0].comment}")
    print()

if __name__ == '__main__':
    test_notifications()
    test_feedback()
