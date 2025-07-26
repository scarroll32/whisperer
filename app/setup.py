import os
import subprocess
import venv
from .config import VENV_DIR, LOG_FILE
from .utils import log

def create_venv():
    """Create a new virtual environment"""
    print("Creating virtual environment...")
    log("Creating virtual environment...")
    venv.create(VENV_DIR, with_pip=True)

def install_whisper():
    """Install Whisper in the virtual environment"""
    print("Installing Whisper (this may take a minute)...")
    log("Installing Whisper...")

    pip_bin = os.path.join(VENV_DIR, "bin", "pip")

    with open(LOG_FILE, "a", encoding="utf-8") as logf:
        subprocess.check_call(
            [pip_bin, "install", "--upgrade", "pip", "setuptools", "wheel"],
            stdout=logf, stderr=logf
        )
        subprocess.check_call(
            [pip_bin, "install", "git+https://github.com/openai/whisper.git"],
            stdout=logf, stderr=logf
        )

def install_yt_dlp():
    """Install yt-dlp in the virtual environment"""
    print("Installing yt-dlp for YouTube downloads...")
    log("Installing yt-dlp...")

    pip_bin = os.path.join(VENV_DIR, "bin", "pip")

    with open(LOG_FILE, "a", encoding="utf-8") as logf:
        subprocess.check_call(
            [pip_bin, "install", "yt-dlp"],
            stdout=logf, stderr=logf
        )

def ensure_venv_and_whisper():
    """Ensure virtual environment exists and Whisper is installed"""
    if not os.path.exists(VENV_DIR):
        create_venv()

    python_bin = os.path.join(VENV_DIR, "bin", "python")

    try:
        subprocess.run(
            [python_bin, "-c", "import whisper"],
            check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
        )
    except subprocess.CalledProcessError:
        install_whisper()

def ensure_yt_dlp():
    """Ensure yt-dlp is installed"""
    python_bin = os.path.join(VENV_DIR, "bin", "python")

    try:
        subprocess.run(
            [python_bin, "-c", "import yt_dlp"],
            check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
        )
    except subprocess.CalledProcessError:
        install_yt_dlp() 