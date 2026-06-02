import pyaudio
import numpy as np
import threading
import queue
import time
import math

class AudioCapture:
    def __init__(self, sample_rate=16000, chunk_size=1024, energy_threshold=300, silence_duration=0.5):
        self.sample_rate = sample_rate
        self.chunk_size = chunk_size
        self.format = pyaudio.paInt16
        self.channels = 1
        self.energy_threshold = energy_threshold
        self.silence_duration = silence_duration

        self.audio = pyaudio.PyAudio()
        self.stream = None
        self.is_listening = False
        self.audio_queue = queue.Queue()

    def start_listening(self):
        self.stream = self.audio.open(
            format=self.format,
            channels=self.channels,
            rate=self.sample_rate,
            input=True,
            frames_per_buffer=self.chunk_size
        )
        self.is_listening = True
        self.capture_thread = threading.Thread(target=self._capture_loop, daemon=True)
        self.capture_thread.start()
        print("Microphone listening started...")

    def stop_listening(self):
        self.is_listening = False
        if self.stream:
            self.stream.stop_stream()
            self.stream.close()
        self.audio.terminate()
        print("Microphone listening stopped.")

    def _get_rms(self, frame):
        # Calculate Root Mean Square energy of the frame
        count = len(frame) / 2
        format = "%dh" % (count)
        import struct
        shorts = struct.unpack(format, frame)
        sum_squares = sum(s**2 for s in shorts)
        return math.sqrt(sum_squares / count) if count > 0 else 0

    def _capture_loop(self):
        audio_buffer = []
        silence_start = None

        while self.is_listening:
            try:
                data = self.stream.read(self.chunk_size, exception_on_overflow=False)
                energy = self._get_rms(data)

                # Simple Voice Activity Detection (VAD)
                if energy > self.energy_threshold:
                    audio_buffer.append(data)
                    silence_start = None
                else:
                    if len(audio_buffer) > 0:
                        audio_buffer.append(data) # Keep appending soft trailing audio
                        if silence_start is None:
                            silence_start = time.time()

                        # If silence has lasted longer than threshold, yield the chunk
                        if time.time() - silence_start > self.silence_duration:
                            self._flush_buffer(audio_buffer)
                            audio_buffer = []
                            silence_start = None

                # Force flush if buffer gets too large (e.g. max 5 seconds)
                if len(audio_buffer) * self.chunk_size / self.sample_rate > 5.0:
                    self._flush_buffer(audio_buffer)
                    audio_buffer = []
                    silence_start = None

            except Exception as e:
                print(f"Error capturing audio: {e}")
                time.sleep(0.1)

    def _flush_buffer(self, buffer):
        if len(buffer) == 0:
            return

        # Combine chunks into a single byte string
        audio_bytes = b"".join(buffer)

        # Convert to numpy array of float32 for Whisper
        audio_data = np.frombuffer(audio_bytes, dtype=np.int16).astype(np.float32) / 32768.0

        # Put the raw audio array in the queue
        self.audio_queue.put(audio_data)

    def get_audio_chunk(self):
        try:
            return self.audio_queue.get(timeout=0.1)
        except queue.Empty:
            return None
