from faster_whisper import WhisperModel
import threading
import queue

class Transcriber:
    def __init__(self, model_size="tiny", device="cpu", compute_type="int8"):
        """
        Initializes the Faster-Whisper transcriber.
        For blazing speed locally, we use 'tiny' and CPU int8 by default.
        """
        print(f"Loading Whisper model '{model_size}' on {device}...")
        self.model = WhisperModel(model_size, device=device, compute_type=compute_type)
        self.text_queue = queue.Queue()
        self.is_transcribing = False

    def start(self, audio_queue):
        """
        Starts the transcription loop on a background thread.
        """
        self.is_transcribing = True
        self.audio_queue = audio_queue
        self.thread = threading.Thread(target=self._transcribe_loop, daemon=True)
        self.thread.start()
        print("Transcriber started.")

    def stop(self):
        """
        Stops the transcription loop.
        """
        self.is_transcribing = False
        print("Transcriber stopped.")

    def _transcribe_loop(self):
        while self.is_transcribing:
            try:
                # Wait for audio chunks
                audio_data = self.audio_queue.get(timeout=0.5)

                # Transcribe the chunk
                segments, info = self.model.transcribe(
                    audio_data,
                    beam_size=1,            # beam_size=1 for maximum speed
                    vad_filter=True,        # enable built-in VAD for cleaner audio
                    without_timestamps=True # skip timestamps to speed up inference
                )

                # Collect the text
                text = "".join(segment.text for segment in segments).strip()

                if text:
                    self.text_queue.put({
                        "original_text": text,
                        "language": info.language
                    })

            except queue.Empty:
                continue
            except Exception as e:
                print(f"Transcription error: {e}")

    def get_transcription(self):
        """
        Retrieves the next available transcription from the queue.
        """
        try:
            return self.text_queue.get(timeout=0.1)
        except queue.Empty:
            return None
