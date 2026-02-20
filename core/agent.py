import yaml
from pathlib import Path
from .memory import MemoryManager
from .tools import TOOL_REGISTRY

class Agent:
    def __init__(self):
        self.memory = MemoryManager()
        self.personas = self._load_personas()
        
    def _load_personas(self):
        path = Path("config/personas.yaml")
        if path.exists():
            with open(path, "r", encoding="utf-8") as f:
                return yaml.safe_load(f).get("personas", {})
        return {}

    async def process(self, text: str, persona_name: str = "mira", channel: str = "web"):
        persona = self.personas.get(persona_name, {})
        system_prompt = persona.get("system_prompt", "You are LightweightClaw.")
        
        # Интеграция с трехуровневой памятью (PiecesOS-style)
        self.memory.add("user", text, "agent_response_placeholder")
        
        # Здесь должна быть логика отправки запроса в LLM (Jan/DeepSeek)
        # Пока возвращаем заглушку с учетом выбранной персоны
        
        prefix = "🎩 [J.A.R.V.I.S]:" if persona_name == "jarvis" else "✨ [Mira]:"
        
        if "цена btc" in text.lower():
            price = await TOOL_REGISTRY["crypto_price"]("BTC")
            return f"{prefix} Цена Bitcoin сейчас: {price} USD."
            
        if "pump.fun" in text.lower():
            sniper = await TOOL_REGISTRY["memecoin_sniper"](dry_run=True)
            return f"{prefix} {sniper['message']} Цели: {sniper['targets']}."

        return f"{prefix} Запрос принят. Моя оперативная память сейчас: {len(self.memory.short_term)} токенов."
