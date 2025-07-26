"""
Tests for setup module
"""
import pytest
import os
from unittest.mock import Mock, patch
from app.setup import create_venv, install_whisper, install_yt_dlp, ensure_venv_and_whisper, ensure_yt_dlp

def test_create_venv(mock_subprocess, temp_dir):
    """Test virtual environment creation"""
    with patch('app.setup.VENV_DIR', os.path.join(temp_dir, "venv")), \
         patch('app.setup.log') as mock_log:
        
        create_venv()
        
        # Check that venv.create was called
        mock_log.assert_called_with("Creating virtual environment...")

def test_install_whisper(mock_subprocess, temp_dir):
    """Test Whisper installation"""
    with patch('app.setup.VENV_DIR', os.path.join(temp_dir, "venv")), \
         patch('app.setup.LOG_FILE', os.path.join(temp_dir, "test.log")), \
         patch('app.setup.log') as mock_log:
        
        install_whisper()
        
        # Check that installation was logged
        mock_log.assert_called_with("Installing Whisper...")
        
        # Check that subprocess.check_call was called for pip install
        mock_subprocess['check_call'].assert_called()

def test_install_yt_dlp(mock_subprocess, temp_dir):
    """Test yt-dlp installation"""
    with patch('app.setup.VENV_DIR', os.path.join(temp_dir, "venv")), \
         patch('app.setup.LOG_FILE', os.path.join(temp_dir, "test.log")), \
         patch('app.setup.log') as mock_log:
        
        install_yt_dlp()
        
        # Check that installation was logged
        mock_log.assert_called_with("Installing yt-dlp...")
        
        # Check that subprocess.check_call was called for pip install
        mock_subprocess['check_call'].assert_called()

def test_ensure_venv_and_whisper_venv_exists(mock_subprocess, temp_dir):
    """Test ensure_venv_and_whisper when venv exists"""
    venv_dir = os.path.join(temp_dir, "venv")
    os.makedirs(venv_dir, exist_ok=True)
    
    with patch('app.setup.VENV_DIR', venv_dir), \
         patch('app.setup.create_venv') as mock_create, \
         patch('app.setup.install_whisper') as mock_install:
        
        # Mock successful import
        mock_subprocess['run'].return_value = Mock(returncode=0)
        
        ensure_venv_and_whisper()
        
        # Should not create venv since it exists
        mock_create.assert_not_called()
        # Should not install whisper since import succeeds
        mock_install.assert_not_called()

def test_ensure_venv_and_whisper_venv_missing(mock_subprocess, temp_dir):
    """Test ensure_venv_and_whisper when venv is missing"""
    venv_dir = os.path.join(temp_dir, "venv")
    
    with patch('app.setup.VENV_DIR', venv_dir), \
         patch('app.setup.create_venv') as mock_create, \
         patch('app.setup.install_whisper') as mock_install:
        
        # Mock failed import - use CalledProcessError instead of generic Exception
        from subprocess import CalledProcessError
        mock_subprocess['run'].side_effect = CalledProcessError(1, "python", "Import failed")
        
        ensure_venv_and_whisper()
        
        # Should create venv since it doesn't exist
        mock_create.assert_called_once()
        # Should install whisper since import fails
        mock_install.assert_called_once()

def test_ensure_yt_dlp_installed(mock_subprocess, temp_dir):
    """Test ensure_yt_dlp when yt-dlp is already installed"""
    with patch('app.setup.VENV_DIR', os.path.join(temp_dir, "venv")), \
         patch('app.setup.install_yt_dlp') as mock_install:
        
        # Mock successful import
        mock_subprocess['run'].return_value = Mock(returncode=0)
        
        ensure_yt_dlp()
        
        # Should not install since import succeeds
        mock_install.assert_not_called()

def test_ensure_yt_dlp_not_installed(mock_subprocess, temp_dir):
    """Test ensure_yt_dlp when yt-dlp is not installed"""
    with patch('app.setup.VENV_DIR', os.path.join(temp_dir, "venv")), \
         patch('app.setup.install_yt_dlp') as mock_install:
        
        # Mock failed import - use CalledProcessError instead of generic Exception
        from subprocess import CalledProcessError
        mock_subprocess['run'].side_effect = CalledProcessError(1, "python", "Import failed")
        
        ensure_yt_dlp()
        
        # Should install since import fails
        mock_install.assert_called_once() 