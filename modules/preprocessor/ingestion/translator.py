# translator.py

from typing import List, Optional, Literal

try:
    from googletrans import Translator as GoogleTranslator
except ImportError:
    GoogleTranslator = None

class Translator:
    """
    Translates text between languages.
    """

    def __init__(self, backend: Literal["google", "none"] = "google", target_lang: str = "en"):
        self.backend = backend
        self.target_lang = target_lang
        if backend == "google" and GoogleTranslator:
            self.translator = GoogleTranslator()
        elif backend == "none":
            self.translator = None
        else:
            raise ImportError("Please install googletrans or choose backend='none'.")

    def translate(self, text: str, src: Optional[str] = None) -> str:
        if self.backend == "none":
            return text
        result = self.translator.translate(text, src=src, dest=self.target_lang)
        return result.text

    def batch_translate(self, texts: List[str], src: Optional[str] = None) -> List[str]:
        return [self.translate(t, src) for t in texts]
