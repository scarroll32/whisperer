"""
VLC Player integration for Whisperer
"""
import os
import subprocess
import time
from .utils import log
from .config import MEDIA_DIR

def is_vlc_installed():
    """Check if VLC is installed on the system"""
    try:
        # Check if VLC.app exists in Applications
        vlc_path = "/Applications/VLC.app/Contents/MacOS/VLC"
        if os.path.exists(vlc_path):
            return vlc_path
        
        # Check if installed via Homebrew
        result = subprocess.run(["which", "vlc"], capture_output=True, text=True)
        if result.returncode == 0:
            return result.stdout.strip()
                
    except Exception as e:
        log(f"Error checking VLC installation: {e}")
    
    return None

def is_vlc_running():
    """Check if VLC is currently running"""
    try:
        # Check for VLC process
        result = subprocess.run(["pgrep", "-f", "VLC"], capture_output=True, text=True)
        return result.returncode == 0
    except Exception as e:
        log(f"Error checking if VLC is running: {e}")
    
    return False

def add_to_vlc_playlist(audio_file):
    """Add audio file to existing VLC playlist using VLC's remote control interface"""
    try:
        audio_path = os.path.join(MEDIA_DIR, audio_file)
        
        if not os.path.exists(audio_path):
            print(f"Audio file not found: {audio_file}")
            log(f"Audio file not found for VLC playlist: {audio_file}")
            return False
        
        # Use osascript to control VLC
        script = f'''
        tell application "VLC"
            open POSIX file "{audio_path}"
        end tell
        '''
        result = subprocess.run(["osascript", "-e", script], 
                              capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"Added to VLC playlist: {audio_file}")
            log(f"Added to VLC playlist: {audio_file}")
            return True
        else:
            print(f"Failed to add to VLC playlist: {result.stderr}")
            log(f"Failed to add to VLC playlist: {result.stderr}")
            return False
                
    except subprocess.TimeoutExpired:
        print("VLC remote control timeout - launching new instance")
        log("VLC remote control timeout, launching new instance")
        return False
    except Exception as e:
        print(f"Error adding to VLC playlist: {e}")
        log(f"Error adding to VLC playlist: {e}")
        return False

def play_audio_with_vlc(audio_file):
    """Play audio file with VLC - add to existing playlist or launch new instance"""
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
        
        # Check if VLC is already running
        if is_vlc_running():
            print("\nVLC is running - adding to existing playlist...")
            log("VLC is running, attempting to add to playlist")
            
            # Try to add to existing VLC playlist
            if add_to_vlc_playlist(audio_file):
                return True
            else:
                print("Launching VLC")
                log("Failed to add to playlist, launching new VLC instance")
        
        # Launch new VLC instance with the audio file
        subprocess.Popen([vlc_path, audio_path], 
                       stdout=subprocess.DEVNULL, 
                       stderr=subprocess.DEVNULL)
        
        #print(f"Playing audio with VLC: {audio_file}")
        log(f"Started VLC playback: {audio_file}")
        return True
        
    except Exception as e:
        print(f"Error launching VLC: {e}")
        log(f"Error launching VLC: {e}")
        return False 