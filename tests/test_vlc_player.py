"""
Tests for VLC player module
"""
import pytest
import os
from unittest.mock import Mock, patch
from app.vlc_player import is_vlc_installed, is_vlc_running, add_to_vlc_playlist, play_audio_with_vlc
import subprocess

def test_is_vlc_installed_macos_app_exists():
    """Test VLC detection when VLC.app exists"""
    with patch('os.path.exists', return_value=True):
        
        result = is_vlc_installed()
        assert result == "/Applications/VLC.app/Contents/MacOS/VLC"

def test_is_vlc_installed_macos_homebrew():
    """Test VLC detection when installed via Homebrew"""
    with patch('os.path.exists', return_value=False), \
         patch('subprocess.run') as mock_run:
        
        mock_run.return_value = Mock(returncode=0, stdout="/usr/local/bin/vlc\n")
        
        result = is_vlc_installed()
        assert result == "/usr/local/bin/vlc"

def test_is_vlc_installed_not_found():
    """Test VLC detection when not installed"""
    with patch('os.path.exists', return_value=False), \
         patch('subprocess.run') as mock_run:
        
        mock_run.return_value = Mock(returncode=1)
        
        result = is_vlc_installed()
        assert result is None

def test_is_vlc_running():
    """Test VLC running detection"""
    with patch('subprocess.run') as mock_run:
        
        mock_run.return_value = Mock(returncode=0)  # VLC is running
        
        result = is_vlc_running()
        assert result is True

def test_is_vlc_not_running():
    """Test VLC running detection when not running"""
    with patch('subprocess.run') as mock_run:
        
        mock_run.return_value = Mock(returncode=1)  # VLC is not running
        
        result = is_vlc_running()
        assert result is False

def test_add_to_vlc_playlist_success(temp_dir):
    """Test adding to VLC playlist"""
    with patch('app.vlc_player.MEDIA_DIR', os.path.join(temp_dir, "media")), \
         patch('subprocess.run') as mock_run, \
         patch('app.vlc_player.log') as mock_log:
        
        # Create media directory and audio file
        os.makedirs(os.path.join(temp_dir, "media"), exist_ok=True)
        with open(os.path.join(temp_dir, "media", "test.mp3"), 'w') as f:
            f.write("fake audio")
        
        mock_run.return_value = Mock(returncode=0)
        
        result = add_to_vlc_playlist("test.mp3")
        
        assert result is True
        mock_run.assert_called_once()
        mock_log.assert_called_with("Added to VLC playlist: test.mp3")

def test_add_to_vlc_playlist_file_not_found(temp_dir):
    """Test adding to VLC playlist when file doesn't exist"""
    with patch('app.vlc_player.MEDIA_DIR', os.path.join(temp_dir, "media")), \
         patch('app.vlc_player.log') as mock_log:
        
        result = add_to_vlc_playlist("nonexistent.mp3")
        
        assert result is False
        mock_log.assert_called_with("Audio file not found for VLC playlist: nonexistent.mp3")

def test_add_to_vlc_playlist_timeout(temp_dir):
    """Test adding to VLC playlist with timeout"""
    with patch('app.vlc_player.MEDIA_DIR', os.path.join(temp_dir, "media")), \
         patch('subprocess.run', side_effect=subprocess.TimeoutExpired("vlc", 5)), \
         patch('app.vlc_player.log') as mock_log:
        
        # Create media directory and audio file
        os.makedirs(os.path.join(temp_dir, "media"), exist_ok=True)
        with open(os.path.join(temp_dir, "media", "test.mp3"), 'w') as f:
            f.write("fake audio")
        
        result = add_to_vlc_playlist("test.mp3")
        
        assert result is False
        mock_log.assert_called_with("VLC remote control timeout, launching new instance")

def test_play_audio_with_vlc_running_add_to_playlist(temp_dir):
    """Test playing audio when VLC is running - add to playlist"""
    with patch('app.vlc_player.is_vlc_installed', return_value="/usr/bin/vlc"), \
         patch('app.vlc_player.is_vlc_running', return_value=True), \
         patch('app.vlc_player.add_to_vlc_playlist', return_value=True), \
         patch('app.vlc_player.MEDIA_DIR', os.path.join(temp_dir, "media")), \
         patch('app.vlc_player.log') as mock_log:
        
        # Create media directory and audio file
        os.makedirs(os.path.join(temp_dir, "media"), exist_ok=True)
        with open(os.path.join(temp_dir, "media", "test.mp3"), 'w') as f:
            f.write("fake audio")
        
        result = play_audio_with_vlc("test.mp3")
        
        assert result is True
        mock_log.assert_called_with("VLC is running, attempting to add to playlist")

def test_play_audio_with_vlc_running_playlist_fails(temp_dir):
    """Test playing audio when VLC is running but playlist add fails"""
    with patch('app.vlc_player.is_vlc_installed', return_value="/usr/bin/vlc"), \
         patch('app.vlc_player.is_vlc_running', return_value=True), \
         patch('app.vlc_player.add_to_vlc_playlist', return_value=False), \
         patch('app.vlc_player.MEDIA_DIR', os.path.join(temp_dir, "media")), \
         patch('subprocess.Popen') as mock_popen, \
         patch('app.vlc_player.log') as mock_log:
        
        # Create media directory and audio file
        os.makedirs(os.path.join(temp_dir, "media"), exist_ok=True)
        with open(os.path.join(temp_dir, "media", "test.mp3"), 'w') as f:
            f.write("fake audio")
        
        result = play_audio_with_vlc("test.mp3")
        
        assert result is True
        mock_popen.assert_called_once()  # Should launch new instance
        mock_log.assert_any_call("Failed to add to playlist, launching new VLC instance")

def test_play_audio_with_vlc_not_running(temp_dir):
    """Test playing audio when VLC is not running - launch new instance"""
    with patch('app.vlc_player.is_vlc_installed', return_value="/usr/bin/vlc"), \
         patch('app.vlc_player.is_vlc_running', return_value=False), \
         patch('app.vlc_player.MEDIA_DIR', os.path.join(temp_dir, "media")), \
         patch('subprocess.Popen') as mock_popen, \
         patch('app.vlc_player.log') as mock_log:
        
        # Create media directory and audio file
        os.makedirs(os.path.join(temp_dir, "media"), exist_ok=True)
        with open(os.path.join(temp_dir, "media", "test.mp3"), 'w') as f:
            f.write("fake audio")
        
        result = play_audio_with_vlc("test.mp3")
        
        assert result is True
        mock_popen.assert_called_once()  # Should launch new instance
        mock_log.assert_called_with("Started VLC playback: test.mp3")

def test_play_audio_with_vlc_not_installed(temp_dir):
    """Test VLC playback when VLC is not installed"""
    with patch('app.vlc_player.is_vlc_installed', return_value=None), \
         patch('app.vlc_player.log') as mock_log:
        
        result = play_audio_with_vlc("test.mp3")
        
        assert result is False
        mock_log.assert_called_with("VLC not found, skipping audio playback")

def test_play_audio_with_vlc_file_not_found(temp_dir):
    """Test VLC playback when audio file doesn't exist"""
    with patch('app.vlc_player.is_vlc_installed', return_value="/usr/bin/vlc"), \
         patch('app.vlc_player.MEDIA_DIR', os.path.join(temp_dir, "media")), \
         patch('app.vlc_player.log') as mock_log:
        
        result = play_audio_with_vlc("nonexistent.mp3")
        
        assert result is False
        mock_log.assert_called_with("Audio file not found for VLC playback: nonexistent.mp3")

def test_play_audio_with_vlc_launch_error(temp_dir):
    """Test VLC playback when launch fails"""
    with patch('app.vlc_player.is_vlc_installed', return_value="/usr/bin/vlc"), \
         patch('app.vlc_player.is_vlc_running', return_value=False), \
         patch('app.vlc_player.MEDIA_DIR', os.path.join(temp_dir, "media")), \
         patch('subprocess.Popen', side_effect=Exception("Launch failed")), \
         patch('app.vlc_player.log') as mock_log:
        
        # Create media directory and audio file
        os.makedirs(os.path.join(temp_dir, "media"), exist_ok=True)
        with open(os.path.join(temp_dir, "media", "test.mp3"), 'w') as f:
            f.write("fake audio")
        
        result = play_audio_with_vlc("test.mp3")
        
        assert result is False
        mock_log.assert_called_with("Error launching VLC: Launch failed") 