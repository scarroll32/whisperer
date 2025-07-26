import os

# Base directories
BASE_DIR = os.path.dirname(os.path.dirname(__file__))  # Go up one level from py/ folder
VENV_DIR = os.path.join(BASE_DIR, "venv")
MEDIA_DIR = os.path.join(BASE_DIR, "media")
LOG_DIR = os.path.join(BASE_DIR, "logs")
LOG_FILE = os.path.join(LOG_DIR, "whisperer.log")

# Default settings
DEFAULT_LANGUAGE = "fr"

# Create necessary directories
os.makedirs(LOG_DIR, exist_ok=True)
os.makedirs(MEDIA_DIR, exist_ok=True) 