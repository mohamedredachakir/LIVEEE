# Real-Time Speech Translation Engine

A lightweight, real-time speech-to-text and translation engine designed to run locally on your machine. It captures audio from your microphone, transcribes it instantly using `faster-whisper`, translates it to your target language using `deep-translator`, and displays the result in a floating, always-on-top subtitle overlay.

Perfect for live meetings on Microsoft Teams, Google Meet, or Zoom.

## Features
- **Local Transcription:** Uses `faster-whisper` on your CPU for blazing-fast, private transcription.
- **Instant Translation:** Uses `deep-translator` (Google Translate) for high-speed, accurate translations.
- **Floating Overlay:** A semi-transparent `tkinter` UI that stays on top of your meeting window.
- **Auto-Clearing Captions:** Subtitles disappear after 4 seconds of silence to keep your screen uncluttered.
- **Dynamic Language Switching:** Change your target language on the fly directly from the UI.

## Microsoft Teams / Windows Desktop Setup

By default, the engine captures audio from your **default microphone**. If you want to translate what *other people* are saying in a Microsoft Teams meeting (i.e., capturing incoming system audio), you need to route your system audio to your microphone input.

**Method 1: Windows Stereo Mix (Built-in)**
1. Right-click the Sound icon in your Windows taskbar and select **Sound Settings**.
2. Go to **More sound settings** -> **Recording** tab.
3. Right-click anywhere and check **Show Disabled Devices**.
4. Right-click **Stereo Mix**, select **Enable**, and then **Set as Default Device**.
5. *Note: If Stereo Mix is not available, use Method 2.*

**Method 2: Virtual Audio Cable (Recommended)**
1. Download and install [VB-Cable (Virtual Audio Cable)](https://vb-audio.com/Cable/).
2. Restart your computer if prompted.
3. In **Windows Sound Settings**, set your Output (Playback) to `CABLE Input`.
4. In **Windows Sound Settings**, set your Input (Recording) to `CABLE Output`.
5. Open **Microsoft Teams**, go to Device Settings, and ensure the speaker is set to `CABLE Input`.
6. Run the translator application. It will now "hear" everything happening in the meeting!

*(To hear the meeting yourself while routing audio, open the properties of `CABLE Output` in Windows Recording settings, go to the "Listen" tab, check "Listen to this device", and select your real headphones/speakers).*

---

## Prerequisites

Before installing the Python packages, you may need to install audio and UI dependencies depending on your OS.

### Windows
No additional system dependencies are usually required. Python 3.10+ is recommended.

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
