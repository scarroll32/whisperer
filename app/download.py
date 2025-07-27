import os
import subprocess
import urllib.parse
import urllib.request
from datetime import datetime
import re
from .config import VENV_DIR, MEDIA_DIR, LOG_FILE
from .utils import log
# yt-dlp is now installed via requirements.txt, so no need to ensure it separately
from .vlc_player import play_audio_with_vlc

def is_youtube_url(url):
    """Check if URL is a YouTube URL"""
    youtube_domains = ['youtube.com', 'youtu.be', 'm.youtube.com']
    parsed_url = urllib.parse.urlparse(url)
    return any(domain in parsed_url.netloc for domain in youtube_domains)

def download_from_url(url):
    """Download audio from URL (YouTube or direct link)"""
    if is_youtube_url(url):
        return download_youtube_audio(url)
    else:
        return download_direct_audio(url)

def download_youtube_audio(url):
    """Download audio from YouTube URL using yt-dlp"""
    # yt-dlp is now installed via requirements.txt
    
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
        downloaded_file = downloaded_files[0]
        # Don't play audio here - let the main function handle it
        return downloaded_file
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
            # Don't play audio here - let the main function handle it
            return filename
        else:
            print("Download failed: file is empty or doesn't exist")
            log("Download failed: file is empty or doesn't exist")
            return None
            
    except Exception as e:
        print(f"Error downloading file: {e}")
        log(f"Error downloading file: {e}")
        return None 