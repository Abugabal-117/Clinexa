"""
Test runner script for the Clinic System
Runs all unit tests and generates test reports
"""

import unittest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))


def run_all_tests():
    """Discover and run all tests"""
    loader = unittest.TestLoader()
    suite = loader.discover('tests', pattern='test_*.py')
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return 0 if result.wasSuccessful() else 1


def run_specific_test(test_module):
    """Run a specific test module"""
    loader = unittest.TestLoader()
    
    try:
        suite = loader.loadTestsFromName(f'tests.{test_module}')
        runner = unittest.TextTestRunner(verbosity=2)
        result = runner.run(suite)
        return 0 if result.wasSuccessful() else 1
    except Exception as e:
        print(f"Error running test {test_module}: {e}")
        return 1


if __name__ == '__main__':
    if len(sys.argv) > 1:
        test_module = sys.argv[1]
        exit_code = run_specific_test(test_module)
    else:
        exit_code = run_all_tests()
    
    sys.exit(exit_code)
