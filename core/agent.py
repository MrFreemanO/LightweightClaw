import yaml
from pathlib import Path
from .memory import MemoryManager
from .tools import TOOL_REGISTRY
from .llm_router import LLMRouter
from .security import SecurityManager

class Agent:
    def __init__(self, config=None):
        self.config = config or {}
        self.memory = MemoryManager()
        self.llm = LLMRouter(self.config.get("llm", {}))
        self.security = SecurityManager(self.config.get("security", {}))
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
        
        # Добавляем в память
        self.memory.add("user", text)
        context = self.memory.get_context()
        
        prompt = {
            "system": system_prompt,
            "messages": context
        }
        
        prefix = "🎩 [J.A.R.V.I.S]:" if persona_name == "jarvis" else "✨ [Mira]:"
        
        # Простая эвристика для инструментов (пока нет full tool calling)
        if "цена btc" in text.lower() and self.security.is_tool_allowed("crypto_price"):
            price = await self.security.run_with_limits(TOOL_REGISTRY["crypto_price"], {"symbol": "BTC"}, "crypto_price")
            reply = f"{prefix} Цена Bitcoin сейчас: {price} USD."
        elif "pump.fun" in text.lower() and self.security.is_tool_allowed("memecoin_sniper"):
            sniper = await self.security.run_with_limits(TOOL_REGISTRY["memecoin_sniper"], {"dry_run": True}, "memecoin_sniper")
            reply = f"{prefix} {sniper.get('message', '')} Цели: {sniper.get('targets', [])}."
        elif "инфо" in text.lower() and self.security.is_tool_allowed("system_info"):
            sys_info = await self.security.run_with_limits(TOOL_REGISTRY["system_info"], {}, "system_info")
            reply = f"{prefix} Загрузка CPU: {sys_info.get('cpu_percent')}%, ОЗУ: {sys_info.get('ram_percent')}%."
        else:
            # Запрос к LLM (Jan)
            llm_reply, _ = await self.llm.chat(prompt)
            reply = f"{prefix} {llm_reply}"

        self.memory.add("agent", reply)
        return reply