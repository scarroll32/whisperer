from datetime import datetime
from .config import LOG_FILE

def log(msg):
    """Log a message with timestamp to the log file"""
    timestamp = datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"{timestamp} {msg}\n")

def clean_transcript(text):
    """Clean and format transcript text while preserving line breaks"""
    # Split into lines and clean each line
    lines = []
    for line in text.splitlines():
        line = line.strip()
        if line:  # Only add non-empty lines
            lines.append(line)
    
    # Join lines with proper line breaks
    return "\n".join(lines) 