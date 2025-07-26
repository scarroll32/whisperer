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
    
    # Ask if user wants to play the audio
    print(f"\nSelected file: {selected_file}")
    play_choice = input("Play audio with VLC? (y/n): ").strip().lower()
    
    if play_choice in ['y', 'yes']:
        play_audio_with_vlc(selected_file)
    
    # Continue with transcription
    base_name = os.path.splitext(selected_file)[0]
    txt_path = os.path.join(MEDIA_DIR, base_name + ".txt")

    if os.path.exists(txt_path):
        print(f"\nTranscription already exists for '{selected_file}':\n")
        with open(txt_path, "r", encoding="utf-8") as f:
            raw_text = f.read()
            print(clean_transcript(raw_text))
    else:
        transcribe(selected_file)
        with open(txt_path, "r", encoding="utf-8") as f:
            raw_text = f.read()
            print(clean_transcript(raw_text))

if __name__ == "__main__":
    main() 