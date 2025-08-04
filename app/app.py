#!/usr/bin/env python3
"""
Whisperer - Audio transcription tool
Main application entry point
"""

import os
import sys
from .config import MEDIA_DIR, load_language
from .setup import ensure_venv_and_dependencies
from .download import download_from_url
from .transcribe import transcribe
from .ui import list_audio_files, print_menu, get_choice, get_url_input, change_language
from .utils import clean_transcript
from .vlc_player import play_audio_with_vlc

def main():
    """Main application function"""
    # Ensure dependencies are installed
    ensure_venv_and_dependencies()

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
            # Refresh the file list
            files = list_audio_files()
            # Find the downloaded file in the new list
            try:
                file_index = files.index(downloaded_file) + 3  # +3 because choice 1 is URL download, 2 is language change
                choice = file_index
            except ValueError:
                print("Error: Downloaded file not found in media directory")
                return
        else:
            print("Failed to download audio from URL")
            return
    
    if choice == 2:
        # Change language option
        change_language()
        return

    # Process the selected file (choice >= 3)
    selected_file = files[choice - 3]  # -3 because choice 1 is URL download, 2 is language change
    
    print(f"\nSelected file: {selected_file}")
    
    # Get current language setting
    current_language = load_language()
    
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
        # Play audio after showing existing transcript
        play_audio_with_vlc(selected_file)
    elif os.path.exists(txt_path):
        print(f"\nTranscription exists for '{selected_file}':\n")
        with open(txt_path, "r", encoding="utf-8") as f:
            raw_text = f.read()
            print(raw_text)  # Speaker-separated format (no formatting applied)
        # Play audio after showing existing transcript
        play_audio_with_vlc(selected_file)
    else:
        # Transcribe first, then play audio
        transcribe(selected_file, language=current_language, detect_speakers=True)  # Use selected language
        with open(txt_path, "r", encoding="utf-8") as f:
            raw_text = f.read()
            print(raw_text)  # Speaker-separated format
        # Play audio after transcription is complete
        play_audio_with_vlc(selected_file)

if __name__ == "__main__":
    main() 