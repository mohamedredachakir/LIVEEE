import time
from src.audio_capture import AudioCapture
from src.transcriber import Transcriber
from src.translator import Translator
from src.ui_overlay import UIOverlay

def main():
    print("Starting Real-Time Speech Translation Engine...")

    # 1. Initialize modules
    # Audio capture (VAD + PyAudio)
    audio_capture = AudioCapture(sample_rate=16000, chunk_size=1024)

    # Transcriber (faster-whisper, tiny, cpu)
    transcriber = Transcriber(model_size="tiny", device="cpu")

    # Translator (deep-translator, default target english)
    translator = Translator(target_lang="en")

    # 2. Setup the UI Overlay
    # Callback when user changes target language in UI
    def on_language_change(new_lang_code):
        translator.set_target_language(new_lang_code)

    ui = UIOverlay(on_lang_change_callback=on_language_change)

    # 3. Start the pipelines
    try:
        # Start background threads
        audio_capture.start_listening()
        transcriber.start(audio_capture.audio_queue)
        translator.start(transcriber.text_queue)

        # 4. Main Event Loop
        # We manually process UI events while checking our translation queue
        # so we don't freeze the tkinter thread.
        while True:
            try:
                # Update UI internally
                ui.root.update()

                # Check for new translations
                translation_data = translator.get_translation()

                if translation_data:
                    ui.update_captions(
                        original_text=translation_data["original_text"],
                        translated_text=translation_data["translated_text"]
                    )

                # Small sleep to prevent CPU hogging by the while loop
                time.sleep(0.05)

            except Exception as e:
                # If window is closed (TclError), we break out
                if "invalid command name" in str(e) or "application has been destroyed" in str(e):
                    print("UI Window closed. Shutting down...")
                    break

    except KeyboardInterrupt:
        print("\nKeyboard interrupt received. Shutting down...")
    finally:
        # Graceful shutdown
        print("Cleaning up...")
        translator.stop()
        transcriber.stop()
        audio_capture.stop_listening()
        print("Shutdown complete.")

if __name__ == "__main__":
    main()
