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
        
        # Добавляем сообщение пользователя в память
        self.memory.add("user", text)
        context = self.memory.get_context()
        
        prompt = {
            "system": system_prompt,
            "messages": context
        }
        
        prefix = "🎩 [J.A.R.V.I.S]:" if persona_name == "jarvis" else "✨ [Mira]:"
        
        # Интеллектуальный роутинг инструментов (замена мокапов на рабочую логику вызова)
        text_lower = text.lower()
        tool_result = None

        if "цена" in text_lower or "price" in text_lower:
            # Простейшее извлечение тикера (для легковесности локальных моделей)
            words = text_lower.replace("?", "").split()
            target_coin = "BTC" # Fallback
            for w in words:
                if w in ["btc", "eth", "sol", "doge", "ton", "wif"]:
                    target_coin = w.upper()
                    break
                    
            if self.security.is_tool_allowed("crypto_price"):
                price = await self.security.run_with_limits(TOOL_REGISTRY["crypto_price"], {"symbol": target_coin}, "crypto_price")
                tool_result = f"Данные рынка: {target_coin} = {price} USD."

        elif "снайпер" in text_lower or "pump.fun" in text_lower:
            if self.security.is_tool_allowed("memecoin_sniper"):
                sniper_data = await self.security.run_with_limits(TOOL_REGISTRY["memecoin_sniper"], {"dry_run": True}, "memecoin_sniper")
                tool_result = f"Отчет снайпера: {sniper_data.get('message')} Найдены: {', '.join(sniper_data.get('targets', []))}."

        elif "поиск" in text_lower or "найди" in text_lower:
            query = text.replace("найди", "").replace("поиск", "").strip()
            if query and self.security.is_tool_allowed("web_search"):
                search_data = await self.security.run_with_limits(TOOL_REGISTRY["web_search"], {"query": query}, "web_search")
                tool_result = f"Результаты поиска: {search_data}"

        elif "система" in text_lower or "статус" in text_lower:
            if self.security.is_tool_allowed("system_info"):
                sys_info = await self.security.run_with_limits(TOOL_REGISTRY["system_info"], {}, "system_info")
                tool_result = f"Система: CPU {sys_info.get('cpu_percent')}%, RAM {sys_info.get('ram_percent')}%, Свободно на диске {sys_info.get('disk_free_gb')} ГБ."

        # Если инструмент был вызван, добавляем его результат в контекст для LLM
        if tool_result:
            prompt["messages"].append({"role": "system", "content": f"Результат выполнения внутреннего инструмента: {tool_result}. Ответь пользователю, опираясь на эти данные."})

        # Отправляем весь контекст (вместе с результатами тулов) в Jan LLM / DeepSeek
        llm_reply, _ = await self.llm.chat(prompt)
        reply = f"{prefix} {llm_reply}"

        # Сохраняем ответ агента
        self.memory.add("agent", reply)
        return reply