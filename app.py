import os
import subprocess
import sys
import venv

BASE_DIR = os.path.dirname(__file__)
VENV_DIR = os.path.join(BASE_DIR, "venv")
MEDIA_DIR = os.path.join(BASE_DIR, "media")
DEFAULT_LANGUAGE = "fr"

def create_venv():
    print("Creating virtual environment...")
    venv.create(VENV_DIR, with_pip=True)

def install_whisper():
    print("Installing Whisper...")
    subprocess.check_call([os.path.join(VENV_DIR, "bin", "pip"), "install", "--upgrade", "pip", "setuptools", "wheel"])
    subprocess.check_call([os.path.join(VENV_DIR, "bin", "pip"), "install", "git+https://github.com/openai/whisper.git"])

def ensure_venv_and_whisper():
    if not os.path.exists(VENV_DIR):
        create_venv()
    python_bin = os.path.join(VENV_DIR, "bin", "python")
    try:
        subprocess.run([python_bin, "-c", "import whisper"], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except subprocess.CalledProcessError:
        install_whisper()

def list_audio_files():
    return [f for f in os.listdir(MEDIA_DIR) if f.lower().endswith((".mp3", ".wav", ".m4a", ".flac"))]

def print_menu(files):
    print("Select an audio file to transcribe:")
    for i, file in enumerate(files, start=1):
        print(f"{i}. {file}")
    print("0. Exit")

def get_choice(files):
    while True:
        try:
            choice = int(input("Enter your choice: "))
            if 0 <= choice <= len(files):
                return choice
        except ValueError:
            pass
        print("Invalid input. Try again.")

def transcribe(file_name, language):
    print(f"Transcribing '{file_name}' to text in {language}...")
    whisper_cmd = os.path.join(VENV_DIR, "bin", "whisper")
    result = subprocess.run([whisper_cmd, file_name, "--language", language, "--task", "transcribe", "--output_format", "txt"], cwd=MEDIA_DIR)
    if result.returncode != 0:
        print("Error during transcription.")
        sys.exit(1)

def main():
    ensure_venv_and_whisper()
    if not os.path.exists(MEDIA_DIR):
        print(f"Media directory does not exist: {MEDIA_DIR}")
        return
    files = list_audio_files()
    if not files:
        print("No audio files found in the media directory.")
        return
    print_menu(files)
    choice = get_choice(files)
    if choice == 0:
        print("Goodbye!")
        return
    selected_file = files[choice - 1]
    base_name = os.path.splitext(selected_file)[0]
    txt_path = os.path.join(MEDIA_DIR, base_name + ".txt")
    if os.path.exists(txt_path):
        print(f"\nTranscription already exists for '{selected_file}':\n")
        with open(txt_path, "r", encoding="utf-8") as f:
            print(f.read())
    else:
        transcribe(selected_file, DEFAULT_LANGUAGE)
        with open(txt_path, "r", encoding="utf-8") as f:
            print(f.read())

if __name__ == "__main__":
    main()
