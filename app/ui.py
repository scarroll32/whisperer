import os
from .config import MEDIA_DIR, load_language, save_language, SUPPORTED_LANGUAGES

def list_audio_files():
    """List all audio files in the media directory"""
    return [f for f in os.listdir(MEDIA_DIR) if f.lower().endswith((".mp3", ".wav", ".m4a", ".flac"))]

def print_menu(files):
    """Print the main menu"""
    current_language = load_language()
    print("Select an option:")
    print("1. Download audio from URL")
    print(f"2. Change language (currently '{current_language}')")
    for i, file in enumerate(files, start=3):
        print(f"{i}. {file}")
    print("0. Exit")

def get_choice(files):
    """Get user choice from menu"""
    while True:
        try:
            choice = int(input("Enter your choice: "))
            if 0 <= choice <= len(files) + 2:  # +2 for URL download and language change
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

def change_language():
    """Handle language change menu"""
    current_language = load_language()
    print(f"\nCurrent language: {current_language}")
    print("Available languages:")
    
    for i, lang in enumerate(SUPPORTED_LANGUAGES, 1):
        marker = " (current)" if lang == current_language else ""
        print(f"{i}. {lang}{marker}")
    
    while True:
        try:
            choice = int(input("Select language (1-4): "))
            if 1 <= choice <= len(SUPPORTED_LANGUAGES):
                selected_language = SUPPORTED_LANGUAGES[choice - 1]
                if selected_language == current_language:
                    print("Language is already set to this option.")
                    return
                
                if save_language(selected_language):
                    print(f"Language changed to '{selected_language}'")
                else:
                    print("Failed to save language setting")
                return
        except ValueError:
            pass
        print("Invalid input. Please enter a number between 1 and 4.") 