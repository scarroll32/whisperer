#!/usr/bin/env python3
"""
Whisperer - Audio transcription tool
Main application entry point
"""

import os
import sys
from .config import MEDIA_DIR
from .setup import ensure_venv_and_whisper
from .download import download_from_url
from .transcribe import transcribe
from .ui import list_audio_files, print_menu, get_choice, get_url_input
from .utils import clean_transcript
from .vlc_player import play_audio_with_vlc

def main():
    """Main application function"""
    # Ensure dependencies are installed
    ensure_venv_and_whisper()

    # Get list of audio files
    files = list_audio_files()
    
    # Show menu and get user choice
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

    # Process the selected file
    selected_file = files[choice - 2]  # -2 because choice 1 is URL download
    
    # Automatically play audio with VLC if available
    print(f"\nSelected file: {selected_file}")
    play_audio_with_vlc(selected_file)
    
    # Continue with transcription (speaker detection is now automatic)
    base_name = os.path.splitext(selected_file)[0]
    txt_path = os.path.join(MEDIA_DIR, base_name + ".txt")
    noformat_path = os.path.join(MEDIA_DIR, base_name + ".noformat.txt")

    # Check for existing transcriptions
    if os.path.exists(noformat_path):
        print(f"\nUnformatted transcription exists for '{selected_file}':\n")
        with open(noformat_path, "r", encoding="utf-8") as f:
            raw_text = f.read()
            print(raw_text)  # No formatting applied
    elif os.path.exists(txt_path):
        print(f"\nTranscription exists for '{selected_file}':\n")
        with open(txt_path, "r", encoding="utf-8") as f:
            raw_text = f.read()
            print(raw_text)  # Speaker-separated format (no formatting applied)
    else:
        transcribe(selected_file, detect_speakers=True)  # Always enable speaker detection
        with open(txt_path, "r", encoding="utf-8") as f:
            raw_text = f.read()
            print(raw_text)  # Speaker-separated format

if __name__ == "__main__":
    main() 