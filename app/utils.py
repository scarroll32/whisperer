from datetime import datetime
from .config import LOG_FILE

def log(msg):
    """Log a message with timestamp to the log file"""
    timestamp = datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"{timestamp} {msg}\n")

def clean_transcript(text):
    """Clean and format transcript text"""
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    joined = " ".join(lines)
    # Add newline after sentence-ending punctuation
    import re
    split_sentences = re.split(r'(?<=[.!?]) +', joined)
    return "\n".join(split_sentences) 