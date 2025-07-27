"""
Tests for setup module
"""
import pytest
import os
from unittest.mock import Mock, patch
from app.setup import create_venv, install_dependencies, ensure_venv_and_dependencies

def test_create_venv(mock_subprocess, temp_dir):
    """Test virtual environment creation"""
    with patch('app.setup.VENV_DIR', os.path.join(temp_dir, "venv")), \
         patch('app.setup.log') as mock_log:
        
        create_venv()
        
        # Check that venv.create was called
        mock_log.assert_called_with("Creating virtual environment...")

def test_install_dependencies(mock_subprocess, temp_dir):
    """Test dependencies installation"""
    with patch('app.setup.VENV_DIR', os.path.join(temp_dir, "venv")), \
         patch('app.setup.LOG_FILE', os.path.join(temp_dir, "test.log")), \
         patch('app.setup.log') as mock_log:
        
        install_dependencies()
        
        # Check that installation was logged
        mock_log.assert_called_with("Installing dependencies from requirements.txt...")
        
        # Check that subprocess.check_call was called for pip install
        mock_subprocess['check_call'].assert_called()

def test_ensure_venv_and_dependencies_venv_exists(mock_subprocess, temp_dir):
    """Test ensure_venv_and_dependencies when venv exists"""
    venv_dir = os.path.join(temp_dir, "venv")
    os.makedirs(venv_dir, exist_ok=True)
    
    with patch('app.setup.VENV_DIR', venv_dir), \
         patch('app.setup.create_venv') as mock_create, \
         patch('app.setup.install_dependencies') as mock_install:
        
        # Mock successful import
        mock_subprocess['run'].return_value = Mock(returncode=0)
        
        ensure_venv_and_dependencies()
        
        # Should not create venv since it exists
        mock_create.assert_not_called()
        # Should not install dependencies since import succeeds
        mock_install.assert_not_called()

def test_ensure_venv_and_dependencies_venv_missing(mock_subprocess, temp_dir):
    """Test ensure_venv_and_dependencies when venv is missing"""
    venv_dir = os.path.join(temp_dir, "venv")
    
    with patch('app.setup.VENV_DIR', venv_dir), \
         patch('app.setup.create_venv') as mock_create, \
         patch('app.setup.install_dependencies') as mock_install:
        
        # Mock failed import - use CalledProcessError instead of generic Exception
        from subprocess import CalledProcessError
        mock_subprocess['run'].side_effect = CalledProcessError(1, "python", "Import failed")
        
        ensure_venv_and_dependencies()
        
        # Should create venv since it doesn't exist
        mock_create.assert_called_once()
        # Should install dependencies since import fails
        mock_install.assert_called_once()

