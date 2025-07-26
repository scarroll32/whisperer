"""
Tests for UI module
"""
import pytest
import os
from unittest.mock import patch, Mock
from app.ui import list_audio_files, print_menu, get_choice, get_url_input

def test_list_audio_files_empty(mock_media_dir):
    """Test listing audio files when directory is empty"""
    with patch('app.ui.MEDIA_DIR', mock_media_dir):
        files = list_audio_files()
        assert files == []

def test_list_audio_files_with_files(mock_media_dir):
    """Test listing audio files with various file types"""
    with patch('app.ui.MEDIA_DIR', mock_media_dir):
        # Create test audio files
        test_files = [
            "audio1.mp3",
            "audio2.wav", 
            "audio3.m4a",
            "audio4.flac",
            "document.txt",  # Should be ignored
            "image.jpg"      # Should be ignored
        ]
        
        for filename in test_files:
            with open(os.path.join(mock_media_dir, filename), 'w') as f:
                f.write("test content")
        
        files = list_audio_files()
        
        # Should only return audio files
        expected = ["audio1.mp3", "audio2.wav", "audio3.m4a", "audio4.flac"]
        assert sorted(files) == sorted(expected)

def test_list_audio_files_case_insensitive(mock_media_dir):
    """Test that audio file detection is case insensitive"""
    with patch('app.ui.MEDIA_DIR', mock_media_dir):
        # Create test files with different cases
        test_files = [
            "audio1.MP3",
            "audio2.WAV",
            "audio3.M4A",
            "audio4.FLAC"
        ]
        
        for filename in test_files:
            with open(os.path.join(mock_media_dir, filename), 'w') as f:
                f.write("test content")
        
        files = list_audio_files()
        
        # Should return all audio files regardless of case
        expected = ["audio1.MP3", "audio2.WAV", "audio3.M4A", "audio4.FLAC"]
        assert sorted(files) == sorted(expected)

def test_print_menu(capsys):
    """Test menu printing"""
    files = ["audio1.mp3", "audio2.wav"]
    
    print_menu(files)
    
    captured = capsys.readouterr()
    output = captured.out
    
    assert "Select an option:" in output
    assert "1. Download audio from URL" in output
    assert "2. audio1.mp3" in output
    assert "3. audio2.wav" in output
    assert "0. Exit" in output

def test_print_menu_empty(capsys):
    """Test menu printing with no files"""
    files = []
    
    print_menu(files)
    
    captured = capsys.readouterr()
    output = captured.out
    
    assert "Select an option:" in output
    assert "1. Download audio from URL" in output
    assert "0. Exit" in output
    # Should not have any file options
    assert "2." not in output

@patch('builtins.input')
def test_get_choice_valid(mock_input):
    """Test getting valid user choice"""
    files = ["audio1.mp3", "audio2.wav"]
    mock_input.return_value = "2"
    
    choice = get_choice(files)
    
    assert choice == 2
    mock_input.assert_called_once_with("Enter your choice: ")

@patch('builtins.input')
def test_get_choice_invalid_then_valid(mock_input):
    """Test getting choice with invalid input first"""
    files = ["audio1.mp3"]
    mock_input.side_effect = ["invalid", "5", "2"]
    
    choice = get_choice(files)
    
    assert choice == 2
    assert mock_input.call_count == 3

@patch('builtins.input')
def test_get_choice_zero(mock_input):
    """Test getting choice zero (exit)"""
    files = ["audio1.mp3"]
    mock_input.return_value = "0"
    
    choice = get_choice(files)
    
    assert choice == 0

@patch('builtins.input')
def test_get_url_input_valid(mock_input):
    """Test getting valid URL input"""
    mock_input.return_value = "https://example.com/audio.mp3"
    
    url = get_url_input()
    
    assert url == "https://example.com/audio.mp3"
    mock_input.assert_called_once_with("Enter the URL (YouTube or direct audio link): ")

@patch('builtins.input')
def test_get_url_input_empty_then_valid(mock_input):
    """Test getting URL input with empty input first"""
    mock_input.side_effect = ["", "https://example.com/audio.mp3"]
    
    url = get_url_input()
    
    assert url == "https://example.com/audio.mp3"
    assert mock_input.call_count == 2

@patch('builtins.input')
def test_get_url_input_whitespace_then_valid(mock_input):
    """Test getting URL input with whitespace input first"""
    mock_input.side_effect = ["   ", "https://example.com/audio.mp3"]
    
    url = get_url_input()
    
    assert url == "https://example.com/audio.mp3"
    assert mock_input.call_count == 2 