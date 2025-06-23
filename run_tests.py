#!/usr/bin/env python3
"""
Cross-platform test runner for Sentient Core.

Usage:
    python run_tests.py [test_path] [options]
    
Example:
    python run_tests.py tests/unit/state -v
"""

import os
import sys
import subprocess
from pathlib import Path

def run_tests(test_path=None, *pytest_args):
    """Run pytest with the given path and arguments."""
    # Default test directory if none provided
    if not test_path:
        test_path = "tests"
    
    # Ensure we're using the current Python interpreter
    python_exec = sys.executable
    
    # Build the pytest command
    cmd = [python_exec, "-m", "pytest", test_path, "--asyncio-mode=auto"]
    
    # Add any additional pytest arguments
    if pytest_args:
        cmd.extend(pytest_args)
    
    # Run the command
    print(f"Running: {' '.join(cmd)}")
    result = subprocess.run(cmd)
    return result.returncode

if __name__ == "__main__":
    # Parse command line arguments
    import argparse
    
    parser = argparse.ArgumentParser(description='Run Sentient Core tests')
    parser.add_argument('test_path', nargs='?', default=None, 
                       help='Path to test file or directory')
    parser.add_argument('pytest_args', nargs=argparse.REMAINDER, 
                       help='Additional arguments to pass to pytest')
    
    args = parser.parse_args()
    
    # Run the tests
    sys.exit(run_tests(args.test_path, *args.pytest_args))
