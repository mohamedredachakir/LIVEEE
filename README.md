# Real-Time Speech Translation Engine

A lightweight, real-time speech-to-text and translation engine designed to run locally on your machine. It captures audio from your microphone, transcribes it instantly using `faster-whisper`, translates it to your target language using `deep-translator`, and displays the result in a floating, always-on-top subtitle overlay.

Perfect for live meetings on Microsoft Teams, Google Meet, or Zoom.

## Features
- **Local Transcription:** Uses `faster-whisper` on your CPU for blazing-fast, private transcription.
- **Instant Translation:** Uses `deep-translator` (Google Translate) for high-speed, accurate translations.
- **Floating Overlay:** A semi-transparent `tkinter` UI that stays on top of your meeting window.
- **Auto-Clearing Captions:** Subtitles disappear after 4 seconds of silence to keep your screen uncluttered.
- **Dynamic Language Switching:** Change your target language on the fly directly from the UI.

## Prerequisites

Before installing the Python packages, you may need to install audio and UI dependencies depending on your OS.

### Windows
No additional system dependencies are usually required.

### macOS
You will need `portaudio` for microphone capture:
```bash
brew install portaudio
```

### Linux (Ubuntu/Debian)
You will need `portaudio` and `tkinter`:
```bash
sudo apt-get update
sudo apt-get install -y portaudio19-dev python3-tk
```

## Installation

1. **Clone the repository (or download the source code):**
   ```bash
   git clone <repository-url>
   cd <repository-directory>
   ```

2. **(Optional but recommended) Create a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   ```

3. **Install the required Python packages:**
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Run the main application script:
   ```bash
   python src/main.py
   ```

2. A floating window will appear at the bottom of your screen.
3. Select your desired **Target Language** from the dropdown menu.
4. Start speaking into your microphone. You will see the original text (in grey) and the translated text (in bright green) appear in real-time.

## Configuration

If you want to adjust the microphone sensitivity or silence duration, you can tweak the parameters in `src/main.py` where `AudioCapture` is initialized:

```python
# Increase energy_threshold if your environment is noisy
# Increase silence_duration if you speak slowly
audio_capture = AudioCapture(sample_rate=16000, chunk_size=1024, energy_threshold=300, silence_duration=0.5)
```

## Privacy Note
The audio transcription happens **100% locally** on your machine using the Whisper model. Only the raw transcribed text is sent to the Google Translate API for translation. No audio is ever uploaded to the cloud.
