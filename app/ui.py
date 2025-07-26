import os
from .config import MEDIA_DIR

def list_audio_files():
    """List all audio files in the media directory"""
    return [f for f in os.listdir(MEDIA_DIR) if f.lower().endswith((".mp3", ".wav", ".m4a", ".flac"))]

def print_menu(files):
    """Print the main menu"""
    print("Select an option:")
    print("1. Download audio from URL")
    for i, file in enumerate(files, start=2):
        print(f"{i}. {file}")
    print("0. Exit")

def get_choice(files):
    """Get user choice from menu"""
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