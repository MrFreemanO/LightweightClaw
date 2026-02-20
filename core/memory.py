from collections import deque
from pathlib import Path
from datetime import datetime
import json
import os

class MemoryManager:
    def __init__(self):
        # 1. Short Term (Оперативная, последние 50)
        self.short_term = deque(maxlen=50)
        
        # 2. Mid Term (Файловая, логи дня)
        os.makedirs("memory", exist_ok=True)
        self.mid_term_path = Path(f"memory/mid_term_{datetime.now().strftime('%Y-%m-%d')}.log")
        
        # 3. Long Term (Еженедельные сводки)
        self.long_term_path = Path("memory/long_term_summaries")
        os.makedirs(self.long_term_path, exist_ok=True)
    
    def add(self, user_id, msg, response):
        interaction = {"user": msg, "agent": response, "time": datetime.now().isoformat()}
        self.short_term.append(interaction)
        
        # Автоквантизация - сброс старых токенов если контекст переполнен (>4000)
        if len(str(self.short_term)) > 4000:
            self.short_term.popleft()
            
        # Запись в Mid-Term (Диск)
        with open(self.mid_term_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(interaction) + "\n")
