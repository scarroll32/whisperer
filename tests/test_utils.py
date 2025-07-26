"""
Tests for utils module
"""
import pytest
import tempfile
import os
from app.utils import log, clean_transcript

def test_log_creates_file(temp_dir):
    """Test that log function creates log file"""
    log_file = os.path.join(temp_dir, "test.log")
    
    with pytest.MonkeyPatch().context() as m:
        m.setattr('app.utils.LOG_FILE', log_file)
        log("Test message")
    
    assert os.path.exists(log_file)
    
    with open(log_file, 'r', encoding='utf-8') as f:
        content = f.read()
        assert "Test message" in content
        assert "[20" in content  # Timestamp format

def test_clean_transcript_single_line():
    """Test transcript cleaning with single line"""
    input_text = "This is a test transcript."
    expected = "This is a test transcript."
    assert clean_transcript(input_text) == expected

def test_clean_transcript_multiple_lines():
    """Test transcript cleaning with multiple lines"""
    input_text = "Line 1.\nLine 2.\nLine 3."
    expected = "Line 1.\nLine 2.\nLine 3."
    assert clean_transcript(input_text) == expected

def test_clean_transcript_with_extra_whitespace():
    """Test transcript cleaning removes extra whitespace"""
    input_text = "  Line 1.  \n  Line 2.  \n  Line 3.  "
    expected = "Line 1.\nLine 2.\nLine 3."
    assert clean_transcript(input_text) == expected

def test_clean_transcript_with_empty_lines():
    """Test transcript cleaning removes empty lines"""
    input_text = "Line 1.\n\nLine 2.\n\n\nLine 3."
    expected = "Line 1.\nLine 2.\nLine 3."
    assert clean_transcript(input_text) == expected

def test_clean_transcript_with_sentence_endings():
    """Test transcript cleaning handles sentence endings properly"""
    input_text = "Hello world. How are you? I am fine! This is great."
    expected = "Hello world.\nHow are you?\nI am fine!\nThis is great."
    assert clean_transcript(input_text) == expected 