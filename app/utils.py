from datetime import datetime
from .config import LOG_FILE

def log(msg):
    """Log a message with timestamp to the log file"""
    timestamp = datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"{timestamp} {msg}\n")

def clean_transcript(text):
    """Clean and format transcript text while intelligently joining sentence fragments"""
    # Split into lines and clean each line
    lines = []
    for line in text.splitlines():
        line = line.strip()
        if line:  # Only add non-empty lines
            lines.append(line)
    
    # Intelligently join lines that are part of the same sentence
    joined_lines = []
    current_line = ""
    
    for i, line in enumerate(lines):
        if not current_line:
            current_line = line
        elif line.startswith(('–', '-', '—')):  # New speaker or section
            # Start a new line
            if current_line:
                joined_lines.append(current_line)
            current_line = line
        elif (line.endswith(',') or  # Lines ending with comma should be joined
              any(word in line.lower() for word in ['qui', 'que', 'dont', 'où', 'quand', 'si', 'et', 'ou', 'mais', 'donc', 'car', 'ni', 'or']) or  # Lines with connecting words
              len(line.split()) <= 3):  # Very short lines are likely fragments
            # Join to current line
            current_line += " " + line
        else:
            # Start a new line
            if current_line:
                joined_lines.append(current_line)
            current_line = line
    
    # Add the last line
    if current_line:
        joined_lines.append(current_line)
    
    return "\n".join(joined_lines) 