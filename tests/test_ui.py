"""
Tests for UI module
"""
import pytest
import os
from unittest.mock import patch, Mock
from app.ui import list_audio_files, print_menu, get_choice, get_url_input, change_language

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
    assert "2. Change language (currently '" in output
    assert "3. audio1.mp3" in output
    assert "4. audio2.wav" in output
    assert "0. Exit" in output

def test_print_menu_empty(capsys):
    """Test menu printing with no files"""
    files = []
    
    print_menu(files)
    
    captured = capsys.readouterr()
    output = captured.out
    
    assert "Select an option:" in output
    assert "1. Download audio from URL" in output
    assert "2. Change language (currently '" in output
    assert "0. Exit" in output
    # Should not have any file options (files start at 3)
    assert "3." not in output

@patch('builtins.input')
def test_get_choice_valid(mock_input):
    """Test getting valid user choice"""
    files = ["audio1.mp3", "audio2.wav"]
    mock_input.return_value = "3"  # Changed from 2 to 3 due to language option
    
    choice = get_choice(files)
    
    assert choice == 3
    mock_input.assert_called_once_with("Enter your choice: ")

@patch('builtins.input')
def test_get_choice_invalid_then_valid(mock_input):
    """Test getting choice with invalid input first"""
    files = ["audio1.mp3"]
    mock_input.side_effect = ["invalid", "5", "3"]  # Changed from 2 to 3
    
    choice = get_choice(files)
    
    assert choice == 3
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

@patch('app.ui.load_language')
@patch('app.ui.save_language')
@patch('builtins.input')
def test_change_language_success(mock_input, mock_save_language, mock_load_language):
    """Test successful language change"""
    mock_load_language.return_value = "fr"
    mock_save_language.return_value = True
    mock_input.return_value = "2"  # Select English
    
    change_language()
    
    mock_save_language.assert_called_once_with("en")

@patch('app.ui.load_language')
@patch('app.ui.save_language')
@patch('builtins.input')
def test_change_language_same_language(mock_input, mock_save_language, mock_load_language):
    """Test changing to the same language"""
    mock_load_language.return_value = "fr"
    mock_input.return_value = "1"  # Select French (current)
    
    change_language()
    
    # Should not call save_language since it's the same
    mock_save_language.assert_not_called()

@patch('app.ui.load_language')
@patch('app.ui.save_language')
@patch('builtins.input')
def test_change_language_save_failure(mock_input, mock_save_language, mock_load_language):
    """Test language change when save fails"""
    mock_load_language.return_value = "fr"
    mock_save_language.return_value = False
    mock_input.return_value = "2"  # Select English
    
    change_language()
    
    mock_save_language.assert_called_once_with("en")

@patch('app.ui.load_language')
@patch('builtins.input')
def test_change_language_invalid_input_then_valid(mock_input, mock_load_language):
    """Test language change with invalid input first"""
    mock_load_language.return_value = "fr"
    mock_input.side_effect = ["invalid", "5", "2"]  # Invalid, out of range, then valid
    
    change_language()
    
    assert mock_input.call_count == 3 