# app/services/tts_engine.py

"""
TTS Engine Service
------------------
Handles real-time text-to-speech using pyttsx3 with support for start/stop control.
"""

import pyttsx3
import threading
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class TTSEngineService:
    def __init__(self):
        self.engine = pyttsx3.init()
        self.reading_thread = None
        self._is_reading = False

    def _speak(self, text: str):
        logger.info("TTS started speaking...")
        self._is_reading = True
        self.engine.say(text)
        self.engine.runAndWait()
        self._is_reading = False
        logger.info("TTS finished speaking.")

    def start_reading(self, text: str):
        """
        Starts reading the provided text in a separate thread.

        Args:
            text (str): Full text to be read aloud.
        """
        if self._is_reading:
            logger.warning("Already reading. Ignoring new request.")
            return

        self.reading_thread = threading.Thread(target=self._speak, args=(text,), daemon=True)
        self.reading_thread.start()

    def stop_reading(self):
        """
        Stops the current TTS playback.
        """
        if self._is_reading:
            logger.info("TTS stopping...")
            self.engine.stop()
            self._is_reading = False

    def is_reading(self) -> bool:
        """
        Returns:
            bool: True if currently reading.
        """
        return self._is_reading


# Singleton instance for reuse
tts_engine = TTSEngineService()