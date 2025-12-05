#!/usr/bin/env python3
"""
Quick test script to verify authentication and validation fixes.
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from controllers.user_controller import UserController
import uuid


def test_registration():
    print("=== Testing Registration with Full Data ===")
    
    email = f"test_user_{uuid.uuid4().hex[:8]}@example.com"
    result = UserController.register(
        email=email,
        password='password123',  # 8+ chars
        first_name='John',
        last_name='Doe',
        user_type='patient',
        date_of_birth='1990-01-01'
    )
    
    print(f"Registration: {result['success']}")
    if result['success']:
        user = result['user']
        print(f"  User ID: {user.user_id}")
        print(f"  Full Name: {user.get_full_name()}")
        print(f"  Email: {user.email}")
        print(f"  Role: {user.role}")
        return user.user_id
    else:
        print(f"  Error: {result['message']}")
        return None


def test_password_validation():
    print("\n=== Testing Password Validation ===")
    
    # Test short password
    result = UserController.register(
        email=f"test_{uuid.uuid4().hex[:8]}@example.com",
        password='short',  # Only 5 chars
        first_name='Test',
        last_name='User',
        user_type='patient'
    )
    
    print(f"Short password (5 chars): {result['success']}")
    if not result['success']:
        print(f"  Expected error: {result['message']}")


def test_ownership_validation(user_id):
    print("\n=== Testing Ownership Validation ===")
    
    if not user_id:
        print("Skipping - no user created")
        return
    
    # Try to update another user's profile
    result = UserController.update_profile(
        user_id=user_id,
        requesting_user_id='different_user_id',  # Different user trying to update
        first_name='Hacked'
    )
    
    print(f"Update other user's profile: {result['success']}")
    if not result['success']:
        print(f"  Expected error: {result['message']}")
    
    # Try to update own profile
    result = UserController.update_profile(
        user_id=user_id,
        requesting_user_id=user_id,  # Same user
        first_name='Jane'
    )
    
    print(f"Update own profile: {result['success']}")
    if result['success']:
        print(f"  Name updated to: {result['user'].first_name}")


def test_empty_field_validation(user_id):
    print("\n=== Testing Empty Field Validation ===")
    
    if not user_id:
        print("Skipping - no user created")
        return
    
    result = UserController.update_profile(
        user_id=user_id,
        requesting_user_id=user_id,
        first_name=''  # Empty first name
    )
    
    print(f"Empty first name: {result['success']}")
    if not result['success']:
        print(f"  Expected error: {result['message']}")


if __name__ == '__main__':
    print("=" * 60)
    print("SECURITY & VALIDATION TESTS")
    print("=" * 60)
    print()
    
    user_id = test_registration()
    test_password_validation()
    test_ownership_validation(user_id)
    test_empty_field_validation(user_id)
    
    print()
    print("=" * 60)
    print("✅ All tests completed!")
    print("=" * 60)
