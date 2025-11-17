# # audio_transcriber.py

# import os
# import tempfile
# from typing import Optional

# class AudioTranscriber:
#     """
#     Transcribes audio files (MP3/WAV) to text using Whisper or SpeechRecognition.
#     """

#     def __init__(self, model_name: str = "base", backend: str = "whisper"):
#         self.backend = backend
#         self.model_name = model_name

#         if backend == "whisper":
#             import whisper
#             print(f"[INFO] Loading Whisper model: {model_name} ...")
#             self.model = whisper.load_model(model_name)
#             print("[INFO] Whisper model loaded successfully.")
#         elif backend == "speechrecognition":
#             import speech_recognition as sr
#             self.recognizer = sr.Recognizer()
#         else:
#             raise ValueError("Unsupported backend. Choose 'whisper' or 'speechrecognition'.")

#     def transcribe(self, audio_path: str, lang: Optional[str] = None) -> str:
#         if self.backend == "whisper":
#             result = self.model.transcribe(audio_path, language=lang)
#             return result["text"]
#         else:
#             import speech_recognition as sr
#             with sr.AudioFile(audio_path) as source:
#                 audio = self.recognizer.record(source)
#             return self.recognizer.recognize_google(audio, language=lang or "en-US")
