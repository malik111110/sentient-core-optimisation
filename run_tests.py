#!/usr/bin/env python3
"""
Cross-platform test runner for Sentient Core.

This script is a simple wrapper around `python -m pytest`.
It forwards all command-line arguments to pytest and ensures
the asyncio mode is set correctly.

Usage:
    python run_tests.py [pytest_options]
    
Example:
    python run_tests.py -v tests/unit/state
"""

import sys
import subprocess

def main():
    """Constructs and runs the pytest command."""
    python_exec = sys.executable
    
    # Start with the base command
    cmd = [python_exec, "-m", "pytest"]
    
    # Add all arguments passed to this script
    pytest_args = sys.argv[1:]
    cmd.extend(pytest_args)
    
    # Ensure asyncio_mode is set if not already specified by the user
    if not any(arg.startswith('--asyncio-mode') for arg in pytest_args):
        cmd.append('--asyncio-mode=auto')
        
    # Run the command
    print(f"Running: {' '.join(cmd)}")
    result = subprocess.run(cmd)
    
    sys.exit(result.returncode)

if __name__ == "__main__":
    main()

