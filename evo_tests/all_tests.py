import glob
import os
import unittest
from evo_tests.util import test_cases_path, to_module_path


def main():
    """ Create a Test Suite to Run Each of the Test Cases within the directory /test_cases """
    suite = unittest.TestSuite()

    for test_file_path in glob.glob(os.path.join(test_cases_path, 'test_*.py')):
        module_path = to_module_path(test_file_path)
        suite.addTest(unittest.defaultTestLoader.loadTestsFromName(module_path))

    unittest.TextTestRunner().run(suite)


if __name__ == "__main__":
    main()
