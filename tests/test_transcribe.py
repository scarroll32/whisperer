"""
Tests for transcribe module
"""
import pytest
import os
from unittest.mock import Mock, patch
from app.transcribe import transcribe

def test_transcribe_success(mock_subprocess, temp_dir):
    """Test successful transcription"""
    with patch('app.transcribe.VENV_DIR', os.path.join(temp_dir, "venv")), \
         patch('app.transcribe.MEDIA_DIR', os.path.join(temp_dir, "media")), \
         patch('app.transcribe.LOG_FILE', os.path.join(temp_dir, "test.log")), \
         patch('app.transcribe.log') as mock_log:
        
        # Mock successful Whisper execution
        mock_subprocess['run'].return_value = Mock(returncode=0)
        
        transcribe("test_audio.mp3")
        
        # Check that transcription was logged
        mock_log.assert_called_with("Transcribing 'test_audio.mp3' to text in fr...")
        
        # Check that subprocess.run was called with correct arguments
        mock_subprocess['run'].assert_called_once()
        call_args = mock_subprocess['run'].call_args[0][0]
        assert "whisper" in call_args[0]
        assert call_args[1] == "test_audio.mp3"
        assert "--language" in call_args
        assert "fr" in call_args
        assert "--task" in call_args
        assert "transcribe" in call_args
        assert "--output_format" in call_args
        assert "txt" in call_args

def test_transcribe_custom_language(mock_subprocess, temp_dir):
    """Test transcription with custom language"""
    with patch('app.transcribe.VENV_DIR', os.path.join(temp_dir, "venv")), \
         patch('app.transcribe.MEDIA_DIR', os.path.join(temp_dir, "media")), \
         patch('app.transcribe.LOG_FILE', os.path.join(temp_dir, "test.log")), \
         patch('app.transcribe.log') as mock_log:
        
        # Mock successful Whisper execution
        mock_subprocess['run'].return_value = Mock(returncode=0)
        
        transcribe("test_audio.mp3", "en")
        
        # Check that subprocess.run was called with English language
        call_args = mock_subprocess['run'].call_args[0][0]
        assert "en" in call_args

def test_transcribe_failure(mock_subprocess, temp_dir):
    """Test transcription failure"""
    with patch('app.transcribe.VENV_DIR', os.path.join(temp_dir, "venv")), \
         patch('app.transcribe.MEDIA_DIR', os.path.join(temp_dir, "media")), \
         patch('app.transcribe.LOG_FILE', os.path.join(temp_dir, "test.log")), \
         patch('app.transcribe.log') as mock_log, \
         patch('sys.exit') as mock_exit:
        
        # Mock failed Whisper execution
        mock_subprocess['run'].return_value = Mock(returncode=1)
        
        transcribe("test_audio.mp3")
        
        # Check that error was logged
        mock_log.assert_any_call("Transcription failed for test_audio.mp3 with exit code 1")
        
        # Check that sys.exit was called
        mock_exit.assert_called_once_with(1)

def test_transcribe_whisper_command_path(mock_subprocess, temp_dir):
    """Test that Whisper command path is correctly constructed"""
    venv_dir = os.path.join(temp_dir, "venv")
    os.makedirs(venv_dir, exist_ok=True)
    
    with patch('app.transcribe.VENV_DIR', venv_dir), \
         patch('app.transcribe.MEDIA_DIR', os.path.join(temp_dir, "media")), \
         patch('app.transcribe.LOG_FILE', os.path.join(temp_dir, "test.log")), \
         patch('app.transcribe.log') as mock_log:
        
        # Mock successful Whisper execution
        mock_subprocess['run'].return_value = Mock(returncode=0)
        
        transcribe("test_audio.mp3")
        
        # Check that Whisper command path is correct
        call_args = mock_subprocess['run'].call_args[0][0]
        expected_whisper_path = os.path.join(venv_dir, "bin", "whisper")
        assert call_args[0] == expected_whisper_path

def test_transcribe_working_directory(mock_subprocess, temp_dir):
    """Test that transcription runs in correct working directory"""
    media_dir = os.path.join(temp_dir, "media")
    os.makedirs(media_dir, exist_ok=True)
    
    with patch('app.transcribe.VENV_DIR', os.path.join(temp_dir, "venv")), \
         patch('app.transcribe.MEDIA_DIR', media_dir), \
         patch('app.transcribe.LOG_FILE', os.path.join(temp_dir, "test.log")), \
         patch('app.transcribe.log') as mock_log:
        
        # Mock successful Whisper execution
        mock_subprocess['run'].return_value = Mock(returncode=0)
        
        transcribe("test_audio.mp3")
        
        # Check that working directory is set to media directory
        call_kwargs = mock_subprocess['run'].call_args[1]
        assert call_kwargs['cwd'] == media_dir 