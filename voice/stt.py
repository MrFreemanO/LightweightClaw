import os
import tempfile
import logging

logger = logging.getLogger(__name__)

class SpeechToText:
    def __init__(self, config):
        self.provider = config.get("provider", "whisper")
        self.language = config.get("language", "ru")
        self.model = None

    def _load_model(self):
        """Ленивая загрузка модели (только при первом обращении, чтобы не забивать RAM на старте)"""
        if self.model is None:
            import whisper
            logger.info("⏳ Загрузка модели Whisper (STT) в память... Это займет пару секунд.")
            # Используем base или tiny для легковесности
            self.model = whisper.load_model("base") 

    async def transcribe(self, audio_bytes):
        """
        Реальное распознавание речи с помощью локального OpenAI Whisper.
        """
        try:
            self._load_model()
            
            # Сохраняем входящие байты (например, из Telegram voice message) во временный файл
            with tempfile.NamedTemporaryFile(suffix=".ogg", delete=False) as f:
                f.write(audio_bytes)
                tmp_path = f.name
                
            logger.info("Распознавание аудио (STT)...")
            result = self.model.transcribe(tmp_path, language=self.language)
            
            # Удаляем временный файл
            os.unlink(tmp_path)
            
            return result.get("text", "")
        except ImportError:
            logger.error("Библиотека whisper не установлена! Сделайте: pip install openai-whisper")
            return "[Ошибка: STT модуль не установлен]"
        except Exception as e:
            logger.error(f"Ошибка распознавания речи: {e}")
            return f"[Ошибка STT: {e}]"