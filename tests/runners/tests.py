#!/usr/bin/env python3
"""
Simple test runner script for Whisperer
Uses existing virtual environment if available
"""
import subprocess
import sys
import os

def run_tests():
    """Run the test suite"""
    print("Running Whisperer tests...")
    
    # Get the project root directory (three levels up from this script)
    project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    requirements_file = os.path.join(project_root, "requirements-test.txt")
    
    # Check if we're in a virtual environment
    if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
        print("Using existing virtual environment")
        python_exe = sys.executable
    else:
        # Try to use the project's virtual environment
        venv_python = os.path.join(project_root, "venv", "bin", "python")
        if os.path.exists(venv_python):
            print("Using project virtual environment")
            python_exe = venv_python
        else:
            print("No virtual environment found. Creating temporary one...")
            # Fall back to creating a temporary venv
            return run_tests_with_temp_venv(project_root, requirements_file)
    
    try:
        # Install test dependencies if needed
        try:
            subprocess.run([python_exe, "-c", "import pytest"], check=True, capture_output=True)
        except subprocess.CalledProcessError:
            print("Installing test dependencies...")
            subprocess.check_call([python_exe, "-m", "pip", "install", "-r", requirements_file])
        
        # Run tests from project root
        cmd = [python_exe, "-m", "pytest", "tests/", "-v", "--cov=app", "--cov-report=term-missing"]
        
        subprocess.run(cmd, check=True, cwd=project_root)
        print("\nAll tests passed!")
        return 0
        
    except subprocess.CalledProcessError as e:
        print(f"\nTests failed with error: {e}")
        return 1

def run_tests_with_temp_venv(project_root, requirements_file):
    """Run tests with a temporary virtual environment"""
    import venv
    import tempfile
    import shutil
    
    temp_dir = tempfile.mkdtemp()
    venv_dir = os.path.join(temp_dir, "test_venv")
    venv.create(venv_dir, with_pip=True)
    
    try:
        python_exe = os.path.join(venv_dir, "bin", "python")
        pip_exe = os.path.join(venv_dir, "bin", "pip")
        
        print("Installing test dependencies...")
        subprocess.check_call([pip_exe, "install", "-r", requirements_file])
        
        cmd = [python_exe, "-m", "pytest", "tests/", "-v", "--cov=app", "--cov-report=term-missing"]
        subprocess.run(cmd, check=True, cwd=project_root)
        print("\nAll tests passed!")
        return 0
        
    except subprocess.CalledProcessError as e:
        print(f"\nTests failed with error: {e}")
        return 1
    finally:
        shutil.rmtree(temp_dir)

if __name__ == "__main__":
    sys.exit(run_tests()) 