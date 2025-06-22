import sys
print("--- Diagnostic Test Script Starting ---")
sys.stdout.flush()
print(f"Python version: {sys.version}")
sys.stdout.flush()
print(f"Python executable: {sys.executable}")
sys.stdout.flush()
print(f"Current working directory: {sys.path[0]}") # Or os.getcwd()
import os
print(f"Actual CWD: {os.getcwd()}")
sys.stdout.flush()
print("--- Diagnostic Test Script Ending ---")
sys.stdout.flush()
