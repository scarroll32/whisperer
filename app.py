import os
import subprocess
import sys
import venv
from datetime import datetime
import re
import urllib.parse
import urllib.request
from pathlib import Path

BASE_DIR = os.path.dirname(__file__)
VENV_DIR = os.path.join(BASE_DIR, "venv")
MEDIA_DIR = os.path.join(BASE_DIR, "media")
LOG_DIR = os.path.join(BASE_DIR, "logs")
LOG_FILE = os.path.join(LOG_DIR, "whisperer.log")
DEFAULT_LANGUAGE = "fr"

os.makedirs(LOG_DIR, exist_ok=True)
os.makedirs(MEDIA_DIR, exist_ok=True)

def log(msg):
    timestamp = datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"{timestamp} {msg}\n")

def create_venv():
    print("Creating virtual environment...")
    log("Creating virtual environment...")
    venv.create(VENV_DIR, with_pip=True)

def install_whisper():
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
    print("Installing yt-dlp for YouTube downloads...")
    log("Installing yt-dlp...")

    pip_bin = os.path.join(VENV_DIR, "bin", "pip")

    with open(LOG_FILE, "a", encoding="utf-8") as logf:
        subprocess.check_call(
            [pip_bin, "install", "yt-dlp"],
            stdout=logf, stderr=logf
        )

def ensure_venv_and_whisper():
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
    python_bin = os.path.join(VENV_DIR, "bin", "python")

    try:
        subprocess.run(
            [python_bin, "-c", "import yt_dlp"],
            check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
        )
    except subprocess.CalledProcessError:
        install_yt_dlp()

def is_youtube_url(url):
    """Check if the URL is a YouTube URL"""
    youtube_domains = ['youtube.com', 'youtu.be', 'www.youtube.com', 'm.youtube.com']
    parsed = urllib.parse.urlparse(url)
    return any(domain in parsed.netloc for domain in youtube_domains)

def download_from_url(url):
    """Download audio from URL (direct audio or YouTube)"""
    print(f"Downloading audio from: {url}")
    log(f"Downloading audio from: {url}")

    if is_youtube_url(url):
        return download_youtube_audio(url)
    else:
        return download_direct_audio(url)

def download_youtube_audio(url):
    """Download audio from YouTube URL using yt-dlp"""
    ensure_yt_dlp()
    
    yt_dlp_bin = os.path.join(VENV_DIR, "bin", "yt-dlp")
    
    # First, get the video title
    print("Getting video information...")
    log("Getting video information...")
    
    # Get video title
    title_result = subprocess.run([
        yt_dlp_bin,
        "--get-title",
        "--no-playlist",
        url
    ], capture_output=True, text=True)
    
    # Log the title extraction attempt
    with open(LOG_FILE, "a", encoding="utf-8") as logf:
        logf.write(f"Title extraction stdout: {title_result.stdout}\n")
        logf.write(f"Title extraction stderr: {title_result.stderr}\n")
    
    if title_result.returncode != 0:
        print("Error getting video title. Using timestamp filename.")
        log("Error getting video title, using timestamp filename")
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"youtube_{timestamp}"
    else:
        # Clean and truncate title to 30 characters
        title = title_result.stdout.strip()
        # Remove invalid filename characters
        title = re.sub(r'[<>:"/\\|?*]', '', title)
        # Replace spaces with underscores
        title = title.replace(' ', '_')
        # Truncate to 30 characters
        filename = title[:30]
        # Remove trailing underscores
        filename = filename.rstrip('_')
        
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"youtube_{timestamp}"
    
    output_template = os.path.join(MEDIA_DIR, f"{filename}.%(ext)s")
    
    print(f"Downloading audio from YouTube: {filename}")
    log(f"Downloading audio from YouTube: {filename}")
    
    with open(LOG_FILE, "a", encoding="utf-8") as logf:
        result = subprocess.run([
            yt_dlp_bin,
            "--extract-audio",
            "--audio-format", "mp3",
            "--audio-quality", "0",
            "--output", output_template,
            url
        ], stdout=logf, stderr=logf)
    
    if result.returncode != 0:
        print("Error downloading from YouTube. Check logs/whisperer.log for details.")
        log(f"YouTube download failed for {url} with exit code {result.returncode}")
        return None
    
    # Find the downloaded file
    downloaded_files = [f for f in os.listdir(MEDIA_DIR) if f.startswith(filename) and f.endswith('.mp3')]
    if downloaded_files:
        return downloaded_files[0]
    return None

def download_direct_audio(url):
    """Download audio from direct URL"""
    try:
        # Generate filename from URL
        parsed_url = urllib.parse.urlparse(url)
        filename = os.path.basename(parsed_url.path)
        
        if not filename or '.' not in filename:
            # Generate filename with timestamp if no proper filename found
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"audio_{timestamp}.mp3"
        
        filepath = os.path.join(MEDIA_DIR, filename)
        
        print(f"Downloading audio file: {filename}")
        log(f"Downloading audio file: {filename}")
        
        # Download the file
        urllib.request.urlretrieve(url, filepath)
        
        if os.path.exists(filepath) and os.path.getsize(filepath) > 0:
            print(f"Successfully downloaded: {filename}")
            log(f"Successfully downloaded: {filename}")
            return filename
        else:
            print("Download failed: file is empty or doesn't exist")
            log("Download failed: file is empty or doesn't exist")
            return None
            
    except Exception as e:
        print(f"Error downloading file: {e}")
        log(f"Error downloading file: {e}")
        return None

def list_audio_files():
    return [f for f in os.listdir(MEDIA_DIR) if f.lower().endswith((".mp3", ".wav", ".m4a", ".flac"))]

def print_menu(files):
    print("Select an option:")
    print("1. Download audio from URL")
    for i, file in enumerate(files, start=2):
        print(f"{i}. {file}")
    print("0. Exit")

def get_choice(files):
    while True:
        try:
            choice = int(input("Enter your choice: "))
            if 0 <= choice <= len(files) + 1:  # +1 for the URL download option
                return choice
        except ValueError:
            pass
        print("Invalid input. Try again.")

def get_url_input():
    """Get URL input from user"""
    while True:
        url = input("Enter the URL (YouTube or direct audio link): ").strip()
        if url:
            return url
        print("Please enter a valid URL.")

def transcribe(file_name, language):
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

def clean_transcript(text):
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    joined = " ".join(lines)
    # Add newline after sentence-ending punctuation
    split_sentences = re.split(r'(?<=[.!?]) +', joined)
    return "\n".join(split_sentences)

def main():
    ensure_venv_and_whisper()

    files = list_audio_files()
    
    print_menu(files)
    choice = get_choice(files)

    if choice == 0:
        print("Goodbye!")
        return
    
    if choice == 1:
        # Download from URL option
        url = get_url_input()
        downloaded_file = download_from_url(url)
        
        if downloaded_file:
            print(f"Successfully downloaded: {downloaded_file}")
            # Refresh the file list
            files = list_audio_files()
            # Find the downloaded file in the new list
            try:
                file_index = files.index(downloaded_file) + 2  # +2 because choice 1 is URL download
                choice = file_index
            except ValueError:
                print("Error: Downloaded file not found in media directory")
                return
        else:
            print("Failed to download audio from URL")
            return

    selected_file = files[choice - 2]  # -2 because choice 1 is URL download
    base_name = os.path.splitext(selected_file)[0]
    txt_path = os.path.join(MEDIA_DIR, base_name + ".txt")

    if os.path.exists(txt_path):
        print(f"\nTranscription already exists for '{selected_file}':\n")
        with open(txt_path, "r", encoding="utf-8") as f:
            raw_text = f.read()
            print(clean_transcript(raw_text))
    else:
        transcribe(selected_file, DEFAULT_LANGUAGE)
        with open(txt_path, "r", encoding="utf-8") as f:
            raw_text = f.read()
            print(clean_transcript(raw_text))

if __name__ == "__main__":
    main()

