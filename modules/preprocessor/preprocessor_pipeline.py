# preprocessor/preprocessor_pipeline.py
"""
Preprocessor Pipeline
=====================

Unified entry point that handles the entire preprocessing flow:
1. Ingestion (input, transcription, translation)
2. Text cleaning (normalization, tokenization, stopword removal)
3. Linguistics (lemmatization, stemming, tagging)

Outputs structured, cleaned text ready for feature extraction or classification.
"""

from typing import Dict, Any, Optional
from .ingestion.input_handler import InputHandler
# from .ingestion.audio_transcriber import AudioTranscriber
from .ingestion.translator import Translator
from .text_cleaning.normalizer import TextNormalizer
from .text_cleaning.tokenizer import Tokenizer
from .text_cleaning.stopwords_remover import StopwordsRemover
from .linguistics.lemmatizer_stemmer import LemmatizerStemmer
from .linguistics.pos_tagger import POSTagger


class PreprocessorPipeline:
    """
    Unified preprocessing pipeline for raw text or audio inputs.
    """

    def __init__(
        self,
        lang: str = "en",
        enable_translation: bool = True,
        target_lang: str = "en",
    ):
        # Core language settings
        self.lang = lang
        self.enable_translation = enable_translation
        self.target_lang = target_lang

        # Ingestion components
        self.input_handler = InputHandler()
        # self.audio_transcriber = AudioTranscriber()
        self.translator = Translator()

        # Text cleaning components
        self.normalizer = TextNormalizer()
        self.tokenizer = Tokenizer()
        self.stopwords_remover = StopwordsRemover(lang=lang)

        # Linguistic components
        self.lemmatizer = LemmatizerStemmer(lang=lang)
        self.tagger = POSTagger(lang=lang)

    # -------------------------------------------------------
    # Main Orchestration
    # -------------------------------------------------------
    def process_input(
        self,
        source: Any,
        source_type: str = "text",
        metadata: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Orchestrates preprocessing based on input type (text/audio).

        Parameters
        ----------
        source : str | file
            Input data (raw text or audio path)
        source_type : str
            Either 'text' or 'audio'
        metadata : dict
            Optional metadata (speaker info, timestamp, etc.)

        Returns
        -------
        dict
            {
                "raw_text": ...,
                "translated_text": ...,
                "clean_text": ...,
                "tokens": ...,
                "lemmas": ...,
                "pos_tags": ...
            }
        """
        # Step 1. Ingestion
        if source_type == "audio":
            # text = self.audio_transcriber.transcribe(source)
            pass
        elif source_type == "text":
            text = self.input_handler.handle(source)
        else:
            raise ValueError("Unsupported source_type. Use 'text' or 'audio'.")

        # Step 2. Optional translation
        if self.enable_translation and self.lang != self.target_lang:
            translated_text = self.translator.translate(text, target_lang=self.target_lang)
        else:
            translated_text = text

        # Step 3. Text cleaning
        clean_text = self.normalizer.clean(translated_text)
        tokens = self.tokenizer.tokenize(clean_text)
        filtered_tokens = self.stopwords_remover.remove(tokens)

        # Step 4. Linguistics
        lemmas = self.lemmatizer.process(" ".join(filtered_tokens))
        pos_tags = self.tagger.tag(lemmas)

        return {
            "raw_text": text,
            "translated_text": translated_text,
            "clean_text": clean_text,
            "tokens": filtered_tokens,
            "lemmas": lemmas,
            "pos_tags": pos_tags,
            "metadata": metadata or {},
        }

    # -------------------------------------------------------
    # Batch Processing
    # -------------------------------------------------------
    def process_batch(self, items: list, source_type: str = "text") -> list:
        """Batch-process multiple inputs."""
        return [self.process_input(item, source_type) for item in items]
