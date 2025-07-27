"""
Pytest configuration and fixtures
"""
import pytest
import os
import tempfile
import shutil
from unittest.mock import Mock, patch
from app.config import BASE_DIR

@pytest.fixture
def temp_dir():
    """Create a temporary directory for testing"""
    temp_dir = tempfile.mkdtemp()
    yield temp_dir
    shutil.rmtree(temp_dir)

@pytest.fixture
def mock_venv_dir(temp_dir):
    """Mock virtual environment directory"""
    venv_dir = os.path.join(temp_dir, "venv")
    os.makedirs(venv_dir, exist_ok=True)
    return venv_dir

@pytest.fixture
def mock_media_dir(temp_dir):
    """Mock media directory"""
    media_dir = os.path.join(temp_dir, "media")
    os.makedirs(media_dir, exist_ok=True)
    return media_dir

@pytest.fixture
def mock_log_dir(temp_dir):
    """Mock log directory"""
    log_dir = os.path.join(temp_dir, "logs")
    os.makedirs(log_dir, exist_ok=True)
    return log_dir

@pytest.fixture
def mock_subprocess():
    """Mock subprocess calls"""
    with patch('subprocess.run') as mock_run, \
         patch('subprocess.check_call') as mock_check_call, \
         patch('subprocess.Popen') as mock_popen:
        
        # Mock successful subprocess calls
        mock_run.return_value = Mock(returncode=0)
        mock_check_call.return_value = None
        
        # Mock Popen for transcription
        mock_process = Mock()
        mock_process.stdout.readline.side_effect = [
            "Transcription line 1\n",
            "Transcription line 2\n",
            ""  # Empty line to end the loop
        ]
        mock_process.poll.return_value = 0  # Process finished
        mock_process.wait.return_value = 0  # Success
        mock_popen.return_value = mock_process
        
        yield {
            'run': mock_run,
            'check_call': mock_check_call,
            'Popen': mock_popen
        }

@pytest.fixture
def mock_urllib():
    """Mock urllib requests"""
    with patch('urllib.request.urlretrieve') as mock_retrieve:
        mock_retrieve.return_value = None
        yield mock_retrieve

@pytest.fixture
def sample_audio_file(mock_media_dir):
    """Create a sample audio file for testing"""
    audio_file = os.path.join(mock_media_dir, "test_audio.mp3")
    with open(audio_file, 'w') as f:
        f.write("fake audio content")
    return audio_file

@pytest.fixture
def sample_transcript_file(mock_media_dir):
    """Create a sample transcript file for testing"""
    transcript_file = os.path.join(mock_media_dir, "test_audio.txt")
    with open(transcript_file, 'w', encoding='utf-8') as f:
        f.write("This is a test transcript.\nIt has multiple lines.")
    return transcript_file 