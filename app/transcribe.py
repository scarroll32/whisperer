import os
import subprocess
import sys
from .config import VENV_DIR, MEDIA_DIR, LOG_FILE, DEFAULT_LANGUAGE
from .utils import log

def transcribe(file_name, language=DEFAULT_LANGUAGE):
    """Transcribe an audio file using Whisper"""
    print(f"Transcribing '{file_name}' to text in {language}...")
    log(f"Transcribing '{file_name}' to text in {language}...")

    whisper_cmd = os.path.join(VENV_DIR, "bin", "whisper")
    with open(LOG_FILE, "a", encoding="utf-8") as logf:
        result = subprocess.run(
            [whisper_cmd, file_name, "--language", language, "--task", "transcribe", "--output_format", "txt"],
            cwd=MEDIA_DIR,
            stdout=logf,
            stderr=logf
        )

    if result.returncode != 0:
        print("Error during transcription. Check logs/whisperer.log for details.")
        log(f"Transcription failed for {file_name} with exit code {result.returncode}")
        sys.exit(1) 