#!/usr/bin/env python3
"""
run_tests.py — Universal test runner for SyllabusTrace-CS.
Discovers and executes all unit and integration tests using standard unittest.
"""

import sys
import unittest
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

def main():
    print("=" * 70)
    print(" SyllabusTrace-CS -- Automated Test Suite Execution")
    print("=" * 70)
    tests_dir = BASE_DIR / "tests"
    loader = unittest.TestLoader()
    suite = loader.discover(start_dir=str(tests_dir), pattern="test_*.py")
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    print("=" * 70)
    if result.wasSuccessful():
        print(f" [PASS] All {result.testsRun} tests completed successfully with 0 failures!")
        sys.exit(0)
    else:
        print(f" [FAIL] Tests failed: {len(result.failures)} failures, {len(result.errors)} errors.")
        sys.exit(1)

if __name__ == "__main__":
    main()
