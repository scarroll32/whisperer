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
    expected = "Line 1. Line 2. Line 3."
    assert clean_transcript(input_text) == expected

def test_clean_transcript_with_extra_whitespace():
    """Test transcript cleaning removes extra whitespace"""
    input_text = "  Line 1.  \n  Line 2.  \n  Line 3.  "
    expected = "Line 1. Line 2. Line 3."
    assert clean_transcript(input_text) == expected

def test_clean_transcript_with_empty_lines():
    """Test transcript cleaning removes empty lines"""
    input_text = "Line 1.\n\nLine 2.\n\n\nLine 3."
    expected = "Line 1. Line 2. Line 3."
    assert clean_transcript(input_text) == expected

def test_clean_transcript_preserves_line_breaks():
    """Test transcript cleaning preserves lines without punctuation"""
    input_text = "Hello world\nHow are you\nI am fine\nThis is great"
    expected = "Hello world How are you I am fine This is great"
    assert clean_transcript(input_text) == expected

def test_clean_transcript_with_mixed_content():
    """Test transcript cleaning with mixed content including empty lines and whitespace"""
    input_text = "  First line.  \n\n  Second line.  \n  \n  Third line.  "
    expected = "First line. Second line. Third line."
    assert clean_transcript(input_text) == expected

def test_clean_transcript_with_commas():
    """Test transcript cleaning joins lines ending with commas"""
    input_text = "This is a sentence,\nthat continues,\nwith commas."
    expected = "This is a sentence, that continues, with commas."
    assert clean_transcript(input_text) == expected

def test_clean_transcript_with_connecting_words():
    """Test transcript cleaning joins lines with connecting words"""
    input_text = "This is a sentence.\nqui continue.\navec des mots de liaison."
    expected = "This is a sentence. qui continue.\navec des mots de liaison."
    assert clean_transcript(input_text) == expected 