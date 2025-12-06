import sys
import os

# Ensure we can import from local modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from repositories.repository_factory import RepositoryFactory

def verify():
    print("Verifying DoctorRepository...")
    try:
        doctor_repo = RepositoryFactory.get_doctor_repository()
        doctors = doctor_repo.get_all()
        print(f"Loaded {len(doctors)} doctors.")
        for doc in doctors:
            print(f"Doctor: {doc.email}, Role: {doc.role}, CreatedAt: {doc.created_at}")
            assert doc.role == 'doctor', f"Expected role 'doctor', got '{doc.role}'"
    except Exception as e:
        print(f"FAILED to load doctors: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

    print("\nVerifying UserRepository...")
    try:
        user_repo = RepositoryFactory.get_user_repository()
        users = user_repo.get_all()
        print(f"Loaded {len(users)} users.")
        for user in users:
            print(f"User: {user.email}, Role: {user.role}, CreatedAt: {user.created_at}")
            # role check might vary if generic user
    except Exception as e:
        print(f"FAILED to load users: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
    
    print("\nVerification Successful!")

if __name__ == "__main__":
    verify()
