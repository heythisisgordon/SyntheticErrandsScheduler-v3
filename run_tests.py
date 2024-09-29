import unittest
import sys
import os
from typing import TextIO

# Add the project root directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

if __name__ == '__main__':
    # Discover and run all tests
    test_loader: unittest.TestLoader = unittest.TestLoader()
    test_suite: unittest.TestSuite = test_loader.discover('tests', pattern='test_*.py')

    # Run the tests
    runner: unittest.TextTestRunner = unittest.TextTestRunner(verbosity=2)
    result: unittest.TestResult = runner.run(test_suite)

    # Exit with non-zero status if there were failures
    sys.exit(not result.wasSuccessful())