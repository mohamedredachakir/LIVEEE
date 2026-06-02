import tkinter as tk
from tkinter import ttk

# Common languages mapping for the UI
LANGUAGES = {
    "English": "en",
    "French": "fr",
    "Spanish": "es",
    "Arabic": "ar",
    "German": "de",
    "Italian": "it",
    "Japanese": "ja",
    "Korean": "ko",
    "Chinese (Simplified)": "zh-CN"
}

class UIOverlay:
    def __init__(self, on_lang_change_callback):
        self.root = tk.Tk()
        self.root.title("Real-Time Speech Translator")
        self.on_lang_change_callback = on_lang_change_callback

        # Make the window stay on top of other windows (for meetings)
        self.root.attributes("-topmost", True)
        # Attempt to make window semi-transparent
        self.root.attributes("-alpha", 0.9)

        # Start in a small floating window mode at the bottom center
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        window_width = 800
        window_height = 150
        x = (screen_width // 2) - (window_width // 2)
        y = screen_height - window_height - 50
        self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")

        # Configure layout and styling
        self.root.configure(bg="#1e1e1e")
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.style.configure("TFrame", background="#1e1e1e")
        self.style.configure("TLabel", background="#1e1e1e", foreground="#ffffff", font=("Helvetica", 14))

        # Setup UI Elements
        self._setup_ui()

        # To auto-clear captions after a few seconds
        self._clear_caption_job = None
        self._clear_delay_ms = 4000 # 4 seconds

    def _setup_ui(self):
        # Top controls frame (Language selector)
        self.controls_frame = ttk.Frame(self.root)
        self.controls_frame.pack(fill=tk.X, padx=10, pady=5)

        ttk.Label(self.controls_frame, text="Target Language:", font=("Helvetica", 10)).pack(side=tk.LEFT, padx=(0, 5))

        self.lang_var = tk.StringVar(value="English")
        self.lang_dropdown = ttk.Combobox(
            self.controls_frame,
            textvariable=self.lang_var,
            values=list(LANGUAGES.keys()),
            state="readonly",
            width=15
        )
        self.lang_dropdown.pack(side=tk.LEFT)
        self.lang_dropdown.bind("<<ComboboxSelected>>", self._on_lang_changed)

        # Close button
        close_btn = ttk.Button(self.controls_frame, text="Close", command=self.root.destroy, width=6)
        close_btn.pack(side=tk.RIGHT)

        # Captions display area
        self.captions_frame = ttk.Frame(self.root)
        self.captions_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))

        self.original_label = tk.Label(
            self.captions_frame,
            text="",
            bg="#1e1e1e",
            fg="#aaaaaa", # grey for original text
            font=("Helvetica", 12, "italic"),
            wraplength=780,
            justify="center"
        )
        self.original_label.pack(fill=tk.X, expand=True)

        self.translation_label = tk.Label(
            self.captions_frame,
            text="Waiting for speech...",
            bg="#1e1e1e",
            fg="#00ff00", # bright green for translation
            font=("Helvetica", 18, "bold"),
            wraplength=780,
            justify="center"
        )
        self.translation_label.pack(fill=tk.X, expand=True)

    def _on_lang_changed(self, event=None):
        selected_lang_name = self.lang_var.get()
        lang_code = LANGUAGES.get(selected_lang_name, "en")
        if self.on_lang_change_callback:
            self.on_lang_change_callback(lang_code)

    def update_captions(self, original_text, translated_text):
        """
        Updates the UI with new text and schedules an auto-clear.
        """
        self.original_label.config(text=original_text)
        self.translation_label.config(text=translated_text)

        # Cancel any pending clear job
        if self._clear_caption_job is not None:
            self.root.after_cancel(self._clear_caption_job)

        # Schedule the text to clear after a few seconds of silence
        self._clear_caption_job = self.root.after(self._clear_delay_ms, self.clear_captions)

    def clear_captions(self):
        """
        Clears the current captions from the screen.
        """
        self.original_label.config(text="")
        self.translation_label.config(text="")
        self._clear_caption_job = None

    def mainloop(self):
        self.root.mainloop()

    def process_events(self):
        """
        Manually process tkinter events (useful if integrating with a custom event loop).
        """
        try:
            self.root.update()
        except tk.TclError:
            pass # Window was closed
