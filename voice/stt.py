import logging
logger = logging.getLogger(__name__)

class SpeechToText:
    def __init__(self, config):
        self.provider = config.get("provider", "whisper")
        self.language = config.get("language", "ru")

    async def transcribe(self, audio_bytes):
        logger.info("Распознавание речи (STT) запущено...")
        # Интеграция openai-whisper
        return "[Распознанный текст]"