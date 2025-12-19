# Automated Testing with Pytest and Dispatch

## Overview
Complete automated testing suite with 40+ tests using both pytest and unittest frameworks, with dispatch pattern for flexible test execution.

## Test Files

### Pytest Tests (New)
- `test_auth_pytest.py` - Authentication tests (7 tests)
- `test_patient_pytest.py` - Patient controller tests (5 tests)
- `test_doctor_pytest.py` - Doctor controller tests (6 tests)
- `test_user_pytest.py` - User controller tests (7 tests)
- `test_models_pytest.py` - Data model tests (10 tests)
- `test_integration_pytest.py` - Integration tests (10 tests)

### Unittest Tests (Original)
- `test_authentication.py` - Authentication tests
- `test_patient_controller.py` - Patient operations
- `test_doctor_controller.py` - Doctor operations
- `test_user_controller.py` - User management
- `test_models.py` - Data models
- `test_integration.py` - Route integration

## Running Tests

### Using Dispatch Pattern (Interactive)
```bash
python run_tests_dispatch.py dispatch
```
Select from interactive menu with numbered options.

### Quick Commands with Dispatch
```bash
python run_tests_dispatch.py all              # Run all pytest tests
python run_tests_dispatch.py auth             # Run auth tests only
python run_tests_dispatch.py patient          # Run patient tests only
python run_tests_dispatch.py doctor           # Run doctor tests only
python run_tests_dispatch.py user             # Run user tests only
python run_tests_dispatch.py models           # Run model tests only
python run_tests_dispatch.py integration      # Run integration tests only
python run_tests_dispatch.py coverage         # Run with coverage report
python run_tests_dispatch.py unittest         # Run unittest tests
python run_tests_dispatch.py help             # Show help
```

### Direct Pytest
```bash
pytest tests/ -v                              # Run all pytest tests
pytest tests/test_auth_pytest.py -v          # Run specific file
pytest tests/ -k auth -v                     # Run tests matching pattern
pytest tests/ --cov=src --cov-report=html   # With coverage
```

### Direct Unittest
```bash
python -m unittest discover -s tests -p test_*.py -v
python -m unittest tests.test_authentication -v
```

## Dispatch Pattern Architecture

The dispatch pattern allows flexible routing of test execution:

```
dispatch module
├── pytest_all              → Run all pytest tests
├── pytest_auth             → Run auth tests
├── pytest_patient          → Run patient tests
├── pytest_doctor           → Run doctor tests
├── pytest_user             → Run user tests
├── pytest_models           → Run model tests
├── pytest_integration      → Run integration tests
├── unittest_all            → Run all unittest tests
├── unittest_*              → Run specific unittest module
├── coverage                → Run with coverage
└── dispatch                → Interactive menu
```

## Test Coverage

**Total: 40+ Tests**

| Category | Pytest | Unittest | Coverage |
|----------|--------|----------|----------|
| Authentication | 7 | 7 | Password hashing, verification |
| Patient | 5 | 5 | Creation, updates, appointments |
| Doctor | 6 | 6 | Schedule, time slots |
| User | 7 | 7 | Registration, login, lockout |
| Models | 10 | 10 | Object creation, serialization |
| Integration | 10 | 10 | Routes, security, redirects |
| **Total** | **45** | **45** | **Comprehensive** |

## Features

✅ **Dual Framework Support**
- Both pytest and unittest implementations
- Easy migration between frameworks
- Consistent test coverage

✅ **Dispatch Pattern**
- Interactive test menu
- Command-line shortcuts
- Flexible test routing

✅ **Comprehensive Coverage**
- 40+ unit tests
- Authentication and security
- User management and registration
- Patient and doctor operations
- Data model validation
- Route integration testing

✅ **Easy Execution**
```bash
python run_tests_dispatch.py all          # Quick
python run_tests_dispatch.py dispatch     # Interactive
python run_tests_dispatch.py coverage     # With metrics
```

## Installation

Install required packages:
```bash
pip install pytest pytest-cov
```

## Expected Output

Successful test run:
```
================================================ test session starts ================================================
collected 45 items

tests/test_auth_pytest.py::TestPasswordHashing::test_hash_password_creates_valid_hash PASSED    [ 2%]
tests/test_auth_pytest.py::TestPasswordHashing::test_hash_password_consistency PASSED           [ 4%]
...
================================================ 45 passed in X.XXs ================================================
```

## CI/CD Integration

The dispatch pattern is ideal for CI/CD:

```yaml
# Example GitHub Actions
- name: Run all tests
  run: python run_tests_dispatch.py all

- name: Run with coverage
  run: python run_tests_dispatch.py coverage

- name: Run specific tests
  run: python run_tests_dispatch.py auth
```
