# input_handler.py

import os
from typing import Union, Optional
from .audio_transcriber import AudioTranscriber

class InputHandler:
    """
    Handles text or audio input for preprocessing.
    """

    def __init__(self, default_lang: str = "en", transcriber_backend: str = "whisper"):
        self.default_lang = default_lang
        self.transcriber = AudioTranscriber(backend=transcriber_backend)

    def load(self, data: Union[str, bytes], file_type: Optional[str] = None) -> str:
        """
        Load and process input.
        :param data: Path, text, or binary audio data.
        :param file_type: 'text' or 'audio'. If None, inferred automatically.
        """
        if isinstance(data, str) and os.path.isfile(data):
            ext = os.path.splitext(data)[1].lower()
            file_type = file_type or ("audio" if ext in [".mp3", ".wav", ".m4a"] else "text")
        else:
            file_type = file_type or "text"

        if file_type == "audio":
            print("[INFO] Processing audio input ...")
            return self.transcriber.transcribe(data, lang=self.default_lang)
        elif file_type == "text":
            print("[INFO] Text input detected.")
            return data.strip()
        else:
            raise ValueError(f"Unsupported file type: {file_type}")
