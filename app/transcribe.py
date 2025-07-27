import os
import subprocess
import sys
from .config import VENV_DIR, MEDIA_DIR, LOG_FILE, DEFAULT_LANGUAGE
from .utils import log

def transcribe(file_name, language=DEFAULT_LANGUAGE, detect_speakers=False):
    """Transcribe an audio file using Whisper"""
    print(f"Transcribing '{file_name}' to text in {language}...")
    log(f"Transcribing '{file_name}' to text in {language}...")

    base_name = os.path.splitext(file_name)[0]
    noformat_path = os.path.join(MEDIA_DIR, base_name + ".noformat.txt")
    
    # Check if .noformat.txt exists and use it instead
    if os.path.exists(noformat_path):
        print(f"Using existing unformatted transcription: {noformat_path}")
        return

    whisper_cmd = os.path.join(VENV_DIR, "bin", "whisper")
    
    # Use CPU for transcription
    device = "cpu"
    
    if detect_speakers:
        # Use speaker detection with real-time progress
        process = subprocess.Popen(
            [whisper_cmd, file_name, "--language", language, "--task", "transcribe", "--output_format", "txt", "--word_timestamps", "True", "--device", device, "--verbose", "True"],
            cwd=MEDIA_DIR,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,
            universal_newlines=True
        )
        
        # Capture output in real-time and display progress
        output_lines = []
        while True:
            line = process.stdout.readline()
            if not line and process.poll() is not None:
                break
            if line:
                line = line.strip()
                output_lines.append(line)
                # Display progress lines (timestamps and transcription progress)
                if line.startswith('[') and '-->' in line:
                    print(".", end="", flush=True)  # Show dot for each completed block
                elif line.startswith('Loading'):
                    print(f"  {line}")
                elif line.startswith('Detecting') or line.startswith('Processing'):
                    print(f"  {line}")
        
        result = process.wait()
        
        # Add newline after progress dots
        print()  # New line after progress dots
        
        # Log the output
        with open(LOG_FILE, "a", encoding="utf-8") as logf:
            logf.write('\n'.join(output_lines) + '\n')
        
        if result == 0:
            # Process the output to add speaker separation
            process_speaker_output(file_name)
            print()  # Extra blank line after successful transcription
        else:
            print("Error during transcription. Check logs/whisperer.log for details.")
            log(f"Transcription failed for {file_name} with exit code {result}")
            sys.exit(1)
    else:
        # Standard transcription with real-time progress
        process = subprocess.Popen(
            [whisper_cmd, file_name, "--language", language, "--task", "transcribe", "--output_format", "txt", "--device", device, "--verbose", "True"],
            cwd=MEDIA_DIR,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,
            universal_newlines=True
        )
        
        # Capture output in real-time and display progress
        output_lines = []
        while True:
            line = process.stdout.readline()
            if not line and process.poll() is not None:
                break
            if line:
                line = line.strip()
                output_lines.append(line)
                # Display progress lines (timestamps and transcription progress)
                if line.startswith('[') and '-->' in line:
                    print(".", end="", flush=True)  # Show dot for each completed block
                elif line.startswith('Transcribing') or line.startswith('Loading'):
                    print(f"  {line}")
                elif line.startswith('Detecting') or line.startswith('Processing'):
                    print(f"  {line}")
        
        result = process.wait()
        
        # Add newline after progress dots
        print()  # New line after progress dots
        
        # Log the output
        with open(LOG_FILE, "a", encoding="utf-8") as logf:
            logf.write('\n'.join(output_lines) + '\n')

        if result == 0:
            print()  # Extra blank line after successful transcription
        else:
            print("Error during transcription. Check logs/whisperer.log for details.")
            log(f"Transcription failed for {file_name} with exit code {result}")
            sys.exit(1)

def process_speaker_output(file_name):
    """Process Whisper output to add speaker separation"""
    base_name = os.path.splitext(file_name)[0]
    txt_path = os.path.join(MEDIA_DIR, base_name + ".txt")
    
    if not os.path.exists(txt_path):
        print("Error: Transcription file not found")
        return
    
    # Read the original transcription
    with open(txt_path, "r", encoding="utf-8") as f:
        content = f.read()
    
    # Simple speaker detection based on line breaks and content patterns
    # This is a basic implementation - for more accurate detection, you'd need
    # to use Whisper's word timestamps or a dedicated speaker diarization tool
    lines = content.split('\n')
    speaker_lines = []
    current_speaker = 1
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
        
        # Check if this looks like a new speaker (short phrases, questions, etc.)
        if (len(line.split()) <= 5 or 
            line.endswith('?') or 
            line.startswith(('–', '-', '—')) or
            any(word in line.lower() for word in ['oui', 'non', 'merci', 'bonjour', 'au revoir'])):
            current_speaker = 2 if current_speaker == 1 else 1
        
        speaker_lines.append(line)
    
    # Write speaker-separated output (overwrite the original .txt file)
    with open(txt_path, "w", encoding="utf-8") as f:
        f.write('\n'.join(speaker_lines)) 