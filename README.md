# Whisperer: manage audio transcriptions in your terminal

Lightweight CLI for transcribing audio files using [OpenAI Whisper](https://github.com/openai/whisper). It automatically sets up a Python virtual environment, installs Whisper, and generates `.txt` transcripts.

## Folder Structure

```
whisperer/
  ├── app.py          # Main script
  ├── media/          # Audio files
  └── venv/           # Auto-created virtual environment
```

## Features

- Lists audio files in `media/` and lets you choose
- Transcribes using Whisper and saves as `.txt`
- Skips files that are already transcribed
- Automatically creates a Python venv
- Installs Whisper if not present
- Default language: French (`fr`)

## Requirements

- Python 3.8 to 3.11 (Whisper is incompatible with 3.12+)
- `ffmpeg` installed and available in your system path

## Installation (macOS)

1. Install Homebrew (https://brew.sh)
2. Run:

   ```bash
   brew install python@3.11 ffmpeg
   ```

3. Verify:

   ```bash
   python3 --version
   ffmpeg -version
   ```

## How to Run

1. Place your audio files (`.mp3`, `.wav`, `.m4a`, `.flac`, etc.) in the `media/` folder.
2. From terminal:

   ```bash
   cd whisperer
   ./whisperer
   ```

On first run, the script will:
- Create `venv/`
- Install Whisper
- Prompt to select a file
- Generate a `.txt` transcript

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

## License

MIT
