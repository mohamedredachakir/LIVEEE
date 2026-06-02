from deep_translator import GoogleTranslator
import threading
import queue

class Translator:
    def __init__(self, target_lang="en"):
        """
        Initializes the Translation module.
        Defaults to English ('en') but can be updated on the fly.
        """
        self.target_lang = target_lang
        self.translator = GoogleTranslator(source='auto', target=self.target_lang)
        self.translation_queue = queue.Queue()
        self.is_translating = False

    def set_target_language(self, lang_code):
        """
        Update the target language dynamically.
        """
        self.target_lang = lang_code
        self.translator = GoogleTranslator(source='auto', target=self.target_lang)
        print(f"Target language changed to: {self.target_lang}")

    def start(self, text_queue):
        """
        Starts the translation loop on a background thread.
        """
        self.is_translating = True
        self.text_queue = text_queue
        self.thread = threading.Thread(target=self._translate_loop, daemon=True)
        self.thread.start()
        print("Translator started.")

    def stop(self):
        """
        Stops the translation loop.
        """
        self.is_translating = False
        print("Translator stopped.")

    def _translate_loop(self):
        while self.is_translating:
            try:
                # Wait for transcribed text
                data = self.text_queue.get(timeout=0.5)
                original_text = data.get("original_text", "").strip()
                detected_lang = data.get("language", "auto")

                if not original_text:
                    continue

                # If the detected language is the same as the target, we can skip translation
                # However, deep_translator handles this gracefully usually.
                try:
                    translated_text = self.translator.translate(original_text)

                    self.translation_queue.put({
                        "original_text": original_text,
                        "translated_text": translated_text,
                        "detected_language": detected_lang
                    })
                except Exception as e:
                    print(f"API Translation error: {e}")
                    # Fallback: Just push the original text if translation fails
                    self.translation_queue.put({
                        "original_text": original_text,
                        "translated_text": "[Translation Error] " + original_text,
                        "detected_language": detected_lang
                    })

            except queue.Empty:
                continue

    def get_translation(self):
        """
        Retrieves the next available translation from the queue.
        """
        try:
            return self.translation_queue.get(timeout=0.1)
        except queue.Empty:
            return None
