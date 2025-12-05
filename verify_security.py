import requests

BASE_URL = 'http://127.0.0.1:5000'

def test_protected_routes():
    print("=== Testing Protected Routes ===")
    session = requests.Session()
    
    # Try accessing edit-profile without login
    response = session.get(f"{BASE_URL}/edit-profile", allow_redirects=False)
    print(f"Access /edit-profile (No Login): Status {response.status_code}")
    if response.status_code == 302 and '/login' in response.headers.get('Location', ''):
        print("PASS: Redirected to login")
    else:
        print(f"FAIL: Expected redirect to login, got {response.status_code}")

def test_registration_persistence():
    print("\n=== Testing Registration Persistence ===")
    # Simulate form submission
    # Since we can't easily run the full flask app here without more setup, 
    # we will rely on the unit tests which invoke the controller directly.
    # But let's check if we can verify the csv content after running a controller action.
    
    from controllers.user_controller import UserController
    import uuid
    
    email = f"patient_test_{str(uuid.uuid4())[:8]}@example.com"
    result = UserController.register(
        email=email,
        password='password123',
        first_name='Test',
        last_name='Patient',
        user_type='patient',
        date_of_birth='1995-01-01'
    )
    
    print(f"Registration Result: {result['success']}")
    
    # Verify in CSV
    import csv
    with open('data/patients.csv', 'r') as f:
        reader = csv.reader(f)
        found = False
        for row in reader:
            if email in row:
                found = True
                print(f"PASS: User {email} found in patients.csv")
                print(f"Role in CSV: {row[5]}") # Assuming role is index 5
                break
        if not found:
            print(f"FAIL: User {email} NOT found in patients.csv")

if __name__ == "__main__":
    # We can only test the persistence part directly here unless we spawn the server
    # For protected routes, we'll assume the server isn't running in this context 
    # and rely on inspection or unit tests. 
    # Actually, let's just run the persistence check.
    test_registration_persistence()
