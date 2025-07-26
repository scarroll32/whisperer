"""
VLC Player integration for Whisperer
"""
import os
import subprocess
import platform
from .utils import log

def is_vlc_installed():
    """Check if VLC is installed on the system"""
    try:
        if platform.system() == "Darwin":  # macOS
            # Check if VLC.app exists in Applications
            vlc_path = "/Applications/VLC.app/Contents/MacOS/VLC"
            if os.path.exists(vlc_path):
                return vlc_path
            
            # Check if installed via Homebrew
            result = subprocess.run(["which", "vlc"], capture_output=True, text=True)
            if result.returncode == 0:
                return result.stdout.strip()
                
        elif platform.system() == "Linux":
            # Check if VLC is in PATH
            result = subprocess.run(["which", "vlc"], capture_output=True, text=True)
            if result.returncode == 0:
                return result.stdout.strip()
                
        elif platform.system() == "Windows":
            # Check common VLC installation paths on Windows
            vlc_paths = [
                "C:\\Program Files\\VideoLAN\\VLC\\vlc.exe",
                "C:\\Program Files (x86)\\VideoLAN\\VLC\\vlc.exe"
            ]
            for path in vlc_paths:
                if os.path.exists(path):
                    return path
                    
    except Exception as e:
        log(f"Error checking VLC installation: {e}")
    
    return None

def play_audio_with_vlc(audio_file):
    """Play audio file with VLC if available"""
    vlc_path = is_vlc_installed()
    
    if not vlc_path:
        print("VLC not found. Audio downloaded but not played.")
        log("VLC not found, skipping audio playback")
        return False
    
    try:
        audio_path = os.path.join(MEDIA_DIR, audio_file)
        
        if not os.path.exists(audio_path):
            print(f"Audio file not found: {audio_file}")
            log(f"Audio file not found for VLC playback: {audio_file}")
            return False
        
        # Launch VLC with the audio file
        if platform.system() == "Darwin":  # macOS
            subprocess.Popen([vlc_path, audio_path], 
                           stdout=subprocess.DEVNULL, 
                           stderr=subprocess.DEVNULL)
        else:  # Linux and Windows
            subprocess.Popen([vlc_path, audio_path], 
                           stdout=subprocess.DEVNULL, 
                           stderr=subprocess.DEVNULL)
        
        print(f"Playing audio with VLC: {audio_file}")
        log(f"Started VLC playback: {audio_file}")
        return True
        
    except Exception as e:
        print(f"Error launching VLC: {e}")
        log(f"Error launching VLC: {e}")
        return False 