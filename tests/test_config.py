"""
Tests for config module
"""
import pytest
import os
from app.config import BASE_DIR, VENV_DIR, MEDIA_DIR, LOG_DIR, LOG_FILE, DEFAULT_LANGUAGE

def test_base_dir():
    """Test BASE_DIR is correctly set"""
    assert BASE_DIR == os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def test_venv_dir():
    """Test VENV_DIR path construction"""
    expected = os.path.join(BASE_DIR, "venv")
    assert VENV_DIR == expected

def test_media_dir():
    """Test MEDIA_DIR path construction"""
    expected = os.path.join(BASE_DIR, "media")
    assert MEDIA_DIR == expected

def test_log_dir():
    """Test LOG_DIR path construction"""
    expected = os.path.join(BASE_DIR, "logs")
    assert LOG_DIR == expected

def test_log_file():
    """Test LOG_FILE path construction"""
    expected = os.path.join(BASE_DIR, "logs", "whisperer.log")
    assert LOG_FILE == expected

def test_default_language():
    """Test DEFAULT_LANGUAGE is set"""
    assert DEFAULT_LANGUAGE == "fr" 