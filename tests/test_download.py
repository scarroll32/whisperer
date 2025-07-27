"""
Tests for download module
"""
import pytest
import os
from unittest.mock import Mock, patch
from app.download import is_youtube_url, download_from_url, download_youtube_audio, download_direct_audio

def test_is_youtube_url_youtube_com():
    """Test YouTube URL detection for youtube.com"""
    url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    assert is_youtube_url(url) is True

def test_is_youtube_url_youtu_be():
    """Test YouTube URL detection for youtu.be"""
    url = "https://youtu.be/dQw4w9WgXcQ"
    assert is_youtube_url(url) is True

def test_is_youtube_url_mobile():
    """Test YouTube URL detection for mobile YouTube"""
    url = "https://m.youtube.com/watch?v=dQw4w9WgXcQ"
    assert is_youtube_url(url) is True

def test_is_youtube_url_not_youtube():
    """Test that non-YouTube URLs return False"""
    url = "https://example.com/video.mp4"
    assert is_youtube_url(url) is False

def test_download_from_url_youtube(mock_subprocess, temp_dir):
    """Test download_from_url with YouTube URL"""
    with patch('app.download.download_youtube_audio') as mock_youtube, \
         patch('app.download.download_direct_audio') as mock_direct:
        
        mock_youtube.return_value = "test_video.mp3"
        
        result = download_from_url("https://youtube.com/watch?v=test")
        
        mock_youtube.assert_called_once_with("https://youtube.com/watch?v=test")
        mock_direct.assert_not_called()
        assert result == "test_video.mp3"

def test_download_from_url_direct(mock_subprocess, temp_dir):
    """Test download_from_url with direct audio URL"""
    with patch('app.download.download_youtube_audio') as mock_youtube, \
         patch('app.download.download_direct_audio') as mock_direct:
        
        mock_direct.return_value = "test_audio.mp3"
        
        result = download_from_url("https://example.com/audio.mp3")
        
        mock_direct.assert_called_once_with("https://example.com/audio.mp3")
        mock_youtube.assert_not_called()
        assert result == "test_audio.mp3"

def test_download_youtube_audio_success(mock_subprocess, temp_dir):
    """Test successful YouTube audio download"""
    with patch('app.download.VENV_DIR', os.path.join(temp_dir, "venv")), \
         patch('app.download.MEDIA_DIR', os.path.join(temp_dir, "media")), \
         patch('app.download.LOG_FILE', os.path.join(temp_dir, "test.log")), \
         patch('app.download.log') as mock_log:
        
        # Create media directory
        os.makedirs(os.path.join(temp_dir, "media"), exist_ok=True)
        
        # Mock the first call (title extraction) to return success with title
        mock_subprocess['run'].side_effect = [
            Mock(returncode=0, stdout="Test Video Title\n"),  # Title extraction
            Mock(returncode=0)  # Download
        ]
        
        # Create the expected downloaded file
        with open(os.path.join(temp_dir, "media", "Test_Video_Title.mp3"), 'w') as f:
            f.write("fake audio")
        
        result = download_youtube_audio("https://youtube.com/watch?v=test")
        
        assert result == "Test_Video_Title.mp3"

def test_download_youtube_audio_failure(mock_subprocess, temp_dir):
    """Test YouTube audio download failure"""
    with patch('app.download.VENV_DIR', os.path.join(temp_dir, "venv")), \
         patch('app.download.MEDIA_DIR', os.path.join(temp_dir, "media")), \
         patch('app.download.LOG_FILE', os.path.join(temp_dir, "test.log")), \
         patch('app.download.log') as mock_log:
        
        # Mock failed download
        mock_subprocess['run'].side_effect = [
            Mock(returncode=0, stdout="Test Video Title\n"),  # Title extraction succeeds
            Mock(returncode=1)  # Download fails
        ]
        
        result = download_youtube_audio("https://youtube.com/watch?v=test")
        
        assert result is None

def test_download_direct_audio_success(mock_urllib, temp_dir):
    """Test successful direct audio download"""
    with patch('app.download.MEDIA_DIR', os.path.join(temp_dir, "media")), \
         patch('app.download.log') as mock_log:
        
        # Create media directory
        os.makedirs(os.path.join(temp_dir, "media"), exist_ok=True)
        
        # Mock successful download - create the file
        def mock_urlretrieve(url, filepath):
            with open(filepath, 'w') as f:
                f.write("fake audio content")
        
        mock_urllib.side_effect = mock_urlretrieve
        
        result = download_direct_audio("https://example.com/audio.mp3")
        
        mock_urllib.assert_called_once()
        assert result == "audio.mp3"

def test_download_direct_audio_with_timestamp(mock_urllib, temp_dir):
    """Test direct audio download with timestamp filename"""
    with patch('app.download.MEDIA_DIR', os.path.join(temp_dir, "media")), \
         patch('app.download.log') as mock_log:
        
        # Create media directory
        os.makedirs(os.path.join(temp_dir, "media"), exist_ok=True)
        
        # Mock successful download - create the file
        def mock_urlretrieve(url, filepath):
            with open(filepath, 'w') as f:
                f.write("fake audio content")
        
        mock_urllib.side_effect = mock_urlretrieve
        
        result = download_direct_audio("https://example.com/")
        
        mock_urllib.assert_called_once()
        assert result.startswith("audio_")
        assert result.endswith(".mp3")

def test_download_direct_audio_failure(mock_urllib, temp_dir):
    """Test direct audio download failure"""
    with patch('app.download.MEDIA_DIR', os.path.join(temp_dir, "media")), \
         patch('app.download.log') as mock_log:
        
        # Mock failed download
        mock_urllib.side_effect = Exception("Download failed")
        
        result = download_direct_audio("https://example.com/audio.mp3")
        
        assert result is None 