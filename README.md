# Whisperer: manage audio transcriptions in your terminal

![Example](example.png)

Lightweight CLI for transcribing audio files using [OpenAI Whisper](https://github.com/openai/whisper) on OS X. It automatically sets up a Python virtual environment, installs Whisper, and generates `.txt` transcripts.

## Folder Structure

```
whisperer/
  ├── app.py          # Main script
  ├── media/          # Audio files
  └── venv/           # Auto-created virtual environment
```

## Features

- Lists audio files in `media/` and lets you choose
- Download audio from URLs (direct audio links or YouTube videos)
- VLC integration - Adds audio to existing VLC playlist or launches new instance (if installed)
- Transcribes using Whisper and saves as `.txt`
- Skips files that are already transcribed
- Automatically creates a Python venv
- Installs Whisper and yt-dlp if not present
- Default language: French (`fr`)

## Requirements

- Python 3.8 to 3.11 (Whisper is incompatible with 3.12+)
- `ffmpeg` installed and available in your system path
- **VLC** (optional) - For automatic audio playback

## Installation (macOS)

1. Install [Homebrew](https://brew.sh)
2. Run:

   ```bash
   brew install python@3.11 ffmpeg
   ```

3. Verify:

   ```bash
   python3 --version
   ffmpeg -version
   ```

4. (Optional) Install VLC for audio playback:

   ```bash
   brew install --cask vlc
   ```

## How to Run

1. Place your audio files (`.mp3`, `.wav`, `.m4a`, `.flac`, etc.) in the `media/` folder, or use the URL download feature.
2. From terminal:

   ```bash
   cd whisperer
   ./whisperer
   ```

On first run, the script will:
- Create `venv/`
- Install Whisper and yt-dlp
- Show menu with options to download from URL or select existing files
- Generate a `.txt` transcript

## URL Download Feature

The app now supports downloading audio from URLs:

### Direct Audio Links
- Supports direct links to audio files (`.mp3`, `.wav`, `.m4a`, `.flac`, etc.)
- Downloads the file directly to the `media/` folder
- Automatically generates filenames if none are provided

### YouTube Videos
- Supports YouTube URLs (youtube.com, youtu.be, etc.)
- Uses yt-dlp to extract audio tracks
- Converts to MP3 format for optimal compatibility
- Downloads to the `media/` folder with timestamped filenames

### Usage
1. Run the app: `./whisperer`
2. Select option "1. Download audio from URL"
3. Enter the URL (YouTube or direct audio link)
4. The file will be downloaded, automatically added to VLC playlist (or launched if not running), and transcribed

## Changing the Language

Edit this line in `app.py`:

```python
DEFAULT_LANGUAGE = "fr"
```

Replace `"fr"` with any ISO code, like `"en"`, `"it"`, `"es"`, etc.

## Troubleshooting

### `ffmpeg not found`

Install via Homebrew:

```bash
brew install ffmpeg
```

### Python 3.12+ causes errors

Whisper supports Python up to 3.11. Use:

```bash
brew install python@3.11
```

Run with:

```bash
/opt/homebrew/bin/python3.11 app.py
```

### YouTube download issues

If YouTube downloads fail:
1. Check your internet connection
2. Verify the YouTube URL is valid and accessible
3. Check the logs in `logs/whisperer.log` for detailed error messages
4. Some videos may be restricted or unavailable in your region

### Direct URL download issues

If direct audio downloads fail:
1. Verify the URL is accessible and points to an audio file
2. Check that the server allows direct downloads
3. Ensure the file format is supported (`.mp3`, `.wav`, `.m4a`, `.flac`)

## Running Tests

```bash
# Run all tests
python tests/runners/tests.py
```

## License

MIT
