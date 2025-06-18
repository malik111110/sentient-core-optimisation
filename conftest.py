import sys
import os

# Add the project root directory to sys.path
# This allows imports like 'from src.main import app' in tests
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
