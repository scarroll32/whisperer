import os
import json

# Base directories
BASE_DIR = os.path.dirname(os.path.dirname(__file__))  # Go up one level from py/ folder
VENV_DIR = os.path.join(BASE_DIR, "venv")
MEDIA_DIR = os.path.join(BASE_DIR, "media")
LOG_DIR = os.path.join(BASE_DIR, "logs")
LOG_FILE = os.path.join(LOG_DIR, "whisperer.log")
SETTINGS_FILE = os.path.join(BASE_DIR, "settings.json")

# Default settings
DEFAULT_LANGUAGE = "fr"
SUPPORTED_LANGUAGES = ["fr", "en", "it", "de"]

def load_language():
    """Load language from settings file, fallback to default"""
    try:
        if os.path.exists(SETTINGS_FILE):
            with open(SETTINGS_FILE, 'r') as f:
                settings = json.load(f)
                language = settings.get('language', DEFAULT_LANGUAGE)
                # Validate language is supported
                if language in SUPPORTED_LANGUAGES:
                    return language
    except Exception:
        pass
    return DEFAULT_LANGUAGE

def save_language(language):
    """Save language to settings file"""
    try:
        settings = {}
        if os.path.exists(SETTINGS_FILE):
            with open(SETTINGS_FILE, 'r') as f:
                settings = json.load(f)
        
        settings['language'] = language
        
        with open(SETTINGS_FILE, 'w') as f:
            json.dump(settings, f, indent=2)
        return True
    except Exception:
        return False

# Create necessary directories
os.makedirs(LOG_DIR, exist_ok=True)
os.makedirs(MEDIA_DIR, exist_ok=True) 