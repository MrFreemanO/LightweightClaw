import os
import subprocess
import logging

logger = logging.getLogger(__name__)

class TextToSpeech:
    def __init__(self, config):
        self.provider = config.get("provider", "piper")
        # ВАЖНО: Путь к локальным моделям голосов. 
        # Модели (.onnx) скачиваются с официального репозитория Piper.
        self.models_dir = os.path.join(os.getcwd(), "models", "piper")
        os.makedirs(self.models_dir, exist_ok=True)

    async def synthesize(self, text, voice_id="ru_RU-irina-medium"):
        """
        Реальный синтез речи с использованием локального движка Piper TTS.
        """
        model_path = os.path.join(self.models_dir, f"{voice_id}.onnx")
        output_wav = os.path.join(os.getcwd(), "memory", "tts_output.wav")
        
        # Если модель не установлена, возвращаем None (Web UI использует встроенный в браузер Fallback)
        if not os.path.exists(model_path):
            logger.error(f"[TTS] ОШИБКА: Файл модели {model_path} не найден! Загрузите .onnx в папку models/piper/")
            return None

        logger.info(f"Синтез речи (TTS) запущен: {text[:20]}...")
        
        try:
            # Вызов бинарника piper (должен быть установлен в системе: `pip install piper-tts` или скачан билд)
            command = f'echo "{text}" | piper --model {model_path} --output_file {output_wav}'
            subprocess.run(command, shell=True, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            
            with open(output_wav, "rb") as f:
                audio_data = f.read()
            return audio_data
        except Exception as e:
            logger.error(f"[TTS] Ошибка генерации аудио: {e}")
            return None
