from collections import deque
from pathlib import Path
from datetime import datetime
import json
import os

class MemoryManager:
    def __init__(self):
        # 1. Short Term
        self.short_term = deque(maxlen=50)
        
        # 2. Mid Term
        os.makedirs("memory", exist_ok=True)
        self.mid_term_path = Path(f"memory/mid_term_{datetime.now().strftime('%Y-%m-%d')}.log")
        
        # 3. Long Term
        self.long_term_path = Path("memory/long_term_summaries")
        os.makedirs(self.long_term_path, exist_ok=True)
    
    def add(self, role, msg):
        interaction = {"role": role, "content": msg, "time": datetime.now().isoformat()}
        self.short_term.append(interaction)
        
        # Автоквантизация (лимит 4000 символов)
        if sum(len(str(m)) for m in self.short_term) > 4000:
            self.short_term.popleft()
            
        # Дамп в Mid-Term
        with open(self.mid_term_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(interaction) + "\n")
            
    def get_context(self):
        return [{"role": item["role"], "content": item["content"]} for item in self.short_term]