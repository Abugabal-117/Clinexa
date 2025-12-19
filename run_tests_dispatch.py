#!/usr/bin/env python3
"""
Test runner for Clinic System using pytest and unittest
Supports both pytest and unittest execution with dispatch
"""

import subprocess
import sys
import os


def run_pytest_all():
    """Run all pytest tests"""
    print("=" * 60)
    print("Running ALL PYTEST TESTS")
    print("=" * 60)
    result = subprocess.run([
        sys.executable, '-m', 'pytest', 
        'tests/', 
        '-v',
        '--tb=short'
    ])
    return result.returncode


def run_pytest_by_category(category):
    """Run pytest tests by category"""
    print("=" * 60)
    print(f"Running PYTEST TESTS: {category}")
    print("=" * 60)
    
    category_map = {
        'auth': 'test_auth_pytest.py',
        'patient': 'test_patient_pytest.py',
        'doctor': 'test_doctor_pytest.py',
        'user': 'test_user_pytest.py',
        'models': 'test_models_pytest.py',
        'integration': 'test_integration_pytest.py'
    }
    
    if category in category_map:
        result = subprocess.run([
            sys.executable, '-m', 'pytest',
            f'tests/{category_map[category]}',
            '-v',
            '--tb=short'
        ])
        return result.returncode
    else:
        print(f"Unknown category: {category}")
        print(f"Available categories: {', '.join(category_map.keys())}")
        return 1


def run_unittest_all():
    """Run all unittest tests"""
    print("=" * 60)
    print("Running ALL UNITTEST TESTS")
    print("=" * 60)
    result = subprocess.run([
        sys.executable, '-m', 'unittest',
        'discover', '-s', 'tests', '-p', 'test_*.py', '-v'
    ])
    return result.returncode


def run_unittest_specific(module):
    """Run specific unittest module"""
    print("=" * 60)
    print(f"Running UNITTEST: {module}")
    print("=" * 60)
    result = subprocess.run([
        sys.executable, '-m', 'unittest',
        f'tests.{module}', '-v'
    ])
    return result.returncode


def run_pytest_coverage():
    """Run pytest with coverage"""
    print("=" * 60)
    print("Running PYTEST WITH COVERAGE")
    print("=" * 60)
    result = subprocess.run([
        sys.executable, '-m', 'pytest',
        'tests/',
        '--cov=src',
        '--cov-report=html',
        '--cov-report=term',
        '-v'
    ])
    return result.returncode


def run_dispatch():
    """Run tests using dispatch pattern"""
    print("=" * 60)
    print("RUNNING TESTS WITH DISPATCH PATTERN")
    print("=" * 60)
    
    dispatches = {
        'pytest_all': run_pytest_all,
        'pytest_auth': lambda: run_pytest_by_category('auth'),
        'pytest_patient': lambda: run_pytest_by_category('patient'),
        'pytest_doctor': lambda: run_pytest_by_category('doctor'),
        'pytest_user': lambda: run_pytest_by_category('user'),
        'pytest_models': lambda: run_pytest_by_category('models'),
        'pytest_integration': lambda: run_pytest_by_category('integration'),
        'unittest_all': run_unittest_all,
        'coverage': run_pytest_coverage,
    }
    
    print("\nAvailable dispatch commands:")
    for i, cmd in enumerate(dispatches.keys(), 1):
        print(f"  {i}. {cmd}")
    
    choice = input("\nSelect test to run (enter number or name): ").strip()
    
    if choice.isdigit() and 1 <= int(choice) <= len(dispatches):
        cmd_name = list(dispatches.keys())[int(choice) - 1]
    else:
        cmd_name = choice
    
    if cmd_name in dispatches:
        return dispatches[cmd_name]()
    else:
        print(f"Unknown command: {cmd_name}")
        return 1


def print_help():
    """Print help information"""
    print("""
USAGE: python run_tests.py [OPTION]

OPTIONS:
    all                 Run all pytest tests
    auth                Run authentication pytest tests
    patient             Run patient pytest tests
    doctor              Run doctor pytest tests
    user                Run user pytest tests
    models              Run model pytest tests
    integration         Run integration pytest tests
    coverage            Run pytest with coverage report
    unittest            Run all unittest tests
    unittest_auth       Run authentication unittest tests
    unittest_patient    Run patient unittest tests
    unittest_doctor     Run doctor unittest tests
    unittest_user       Run user unittest tests
    unittest_models     Run model unittest tests
    dispatch            Interactive dispatch menu
    help                Show this help message

EXAMPLES:
    python run_tests.py all
    python run_tests.py auth
    python run_tests.py coverage
    python run_tests.py dispatch
    """)


def main():
    """Main entry point"""
    if len(sys.argv) < 2:
        run_dispatch()
        return
    
    command = sys.argv[1].lower()
    
    dispatch = {
        'all': run_pytest_all,
        'auth': lambda: run_pytest_by_category('auth'),
        'patient': lambda: run_pytest_by_category('patient'),
        'doctor': lambda: run_pytest_by_category('doctor'),
        'user': lambda: run_pytest_by_category('user'),
        'models': lambda: run_pytest_by_category('models'),
        'integration': lambda: run_pytest_by_category('integration'),
        'coverage': run_pytest_coverage,
        'unittest': run_unittest_all,
        'unittest_auth': lambda: run_unittest_specific('test_authentication'),
        'unittest_patient': lambda: run_unittest_specific('test_patient_controller'),
        'unittest_doctor': lambda: run_unittest_specific('test_doctor_controller'),
        'unittest_user': lambda: run_unittest_specific('test_user_controller'),
        'unittest_models': lambda: run_unittest_specific('test_models'),
        'dispatch': run_dispatch,
        'help': lambda: (print_help(), 0),
    }
    
    if command in dispatch:
        exit_code = dispatch[command]()
        sys.exit(exit_code if exit_code is not None else 0)
    else:
        print(f"Unknown command: {command}")
        print_help()
        sys.exit(1)


if __name__ == '__main__':
    main()
