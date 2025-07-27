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

def install_dependencies():
    """Install all dependencies from requirements.txt"""
    print("Installing dependencies (this may take a minute)...")
    log("Installing dependencies from requirements.txt...")

    pip_bin = os.path.join(VENV_DIR, "bin", "pip")
    requirements_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "requirements.txt")

    with open(LOG_FILE, "a", encoding="utf-8") as logf:
        subprocess.check_call(
            [pip_bin, "install", "--upgrade", "pip", "setuptools", "wheel"],
            stdout=logf, stderr=logf
        )
        # Install all dependencies from requirements.txt
        subprocess.check_call(
            [pip_bin, "install", "-r", requirements_path],
            stdout=logf, stderr=logf
        )

def ensure_venv_and_dependencies():
    """Ensure virtual environment exists and all dependencies are installed"""
    if not os.path.exists(VENV_DIR):
        create_venv()

    python_bin = os.path.join(VENV_DIR, "bin", "python")

    try:
        subprocess.run(
            [python_bin, "-c", "import whisper, yt_dlp"],
            check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
        )
    except subprocess.CalledProcessError:
        install_dependencies() 