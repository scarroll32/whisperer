"""
Tests for config module
"""
import os
import json
import tempfile
import shutil
from unittest.mock import patch
from app.config import BASE_DIR, VENV_DIR, MEDIA_DIR, LOG_DIR, LOG_FILE, DEFAULT_LANGUAGE, load_language, save_language, SUPPORTED_LANGUAGES

def test_base_dir():
    """Test BASE_DIR is set correctly"""
    expected = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    assert BASE_DIR == expected

def test_venv_dir():
    """Test VENV_DIR is set correctly"""
    expected = os.path.join(BASE_DIR, "venv")
    assert VENV_DIR == expected

def test_media_dir():
    """Test MEDIA_DIR is set correctly"""
    expected = os.path.join(BASE_DIR, "media")
    assert MEDIA_DIR == expected

def test_log_dir():
    """Test LOG_DIR is set correctly"""
    expected = os.path.join(BASE_DIR, "logs")
    assert LOG_DIR == expected

def test_log_file():
    """Test LOG_FILE is set correctly"""
    expected = os.path.join(LOG_DIR, "whisperer.log")
    assert LOG_FILE == expected

def test_default_language():
    """Test DEFAULT_LANGUAGE is set"""
    assert DEFAULT_LANGUAGE == "fr"

def test_supported_languages():
    """Test SUPPORTED_LANGUAGES contains expected languages"""
    expected = ["fr", "en", "it", "de"]
    assert SUPPORTED_LANGUAGES == expected

def test_load_language_default():
    """Test load_language returns default when no settings file exists"""
    with patch('app.config.SETTINGS_FILE', '/nonexistent/file.json'):
        language = load_language()
        assert language == DEFAULT_LANGUAGE

def test_load_language_from_file():
    """Test load_language loads from settings file"""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        json.dump({"language": "en"}, f)
        settings_file = f.name
    
    try:
        with patch('app.config.SETTINGS_FILE', settings_file):
            language = load_language()
            assert language == "en"
    finally:
        os.unlink(settings_file)

def test_load_language_invalid_file():
    """Test load_language handles invalid JSON gracefully"""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        f.write("invalid json")
        settings_file = f.name
    
    try:
        with patch('app.config.SETTINGS_FILE', settings_file):
            language = load_language()
            assert language == DEFAULT_LANGUAGE
    finally:
        os.unlink(settings_file)

def test_load_language_unsupported_language():
    """Test load_language ignores unsupported languages"""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        json.dump({"language": "es"}, f)  # Spanish not supported
        settings_file = f.name
    
    try:
        with patch('app.config.SETTINGS_FILE', settings_file):
            language = load_language()
            assert language == DEFAULT_LANGUAGE
    finally:
        os.unlink(settings_file)

def test_save_language_new_file():
    """Test save_language creates new settings file"""
    with tempfile.TemporaryDirectory() as temp_dir:
        settings_file = os.path.join(temp_dir, "settings.json")
        
        with patch('app.config.SETTINGS_FILE', settings_file):
            result = save_language("en")
            assert result == True
            
            # Check file was created with correct content
            assert os.path.exists(settings_file)
            with open(settings_file, 'r') as f:
                settings = json.load(f)
                assert settings["language"] == "en"

def test_save_language_existing_file():
    """Test save_language updates existing settings file"""
    with tempfile.TemporaryDirectory() as temp_dir:
        settings_file = os.path.join(temp_dir, "settings.json")
        
        # Create existing settings file
        with open(settings_file, 'w') as f:
            json.dump({"other_setting": "value"}, f)
        
        with patch('app.config.SETTINGS_FILE', settings_file):
            result = save_language("it")
            assert result == True
            
            # Check file was updated with correct content
            with open(settings_file, 'r') as f:
                settings = json.load(f)
                assert settings["language"] == "it"
                assert settings["other_setting"] == "value"  # Preserved existing setting

def test_save_language_permission_error():
    """Test save_language handles permission errors gracefully"""
    with patch('app.config.SETTINGS_FILE', '/root/inaccessible/settings.json'):
        result = save_language("en")
        assert result == False 