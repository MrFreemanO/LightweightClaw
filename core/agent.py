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
        
        self.memory.add("user", text)
        context = self.memory.get_context()
        
        prompt = {
            "system": system_prompt,
            "messages": context
        }
        
        prefix = "🎩 [J.A.R.V.I.S]:" if persona_name == "jarvis" else "✨ [Mira]:"
        
        text_lower = text.lower()
        tool_result = None

        if "price" in text_lower or "цена" in text_lower:
            words = text_lower.replace("?", "").split()
            target_coin = "BTC"
            for w in words:
                if w in ["btc", "eth", "sol", "doge", "ton", "wif"]:
                    target_coin = w.upper()
                    break
                    
            if self.security.is_tool_allowed("crypto_price"):
                price = await self.security.run_with_limits(TOOL_REGISTRY["crypto_price"], {"symbol": target_coin}, "crypto_price")
                tool_result = f"Market data: {target_coin} = {price} USD."

        elif "search" in text_lower or "поиск" in text_lower or "найди" in text_lower:
            query = text_lower.replace("найди", "").replace("поиск", "").replace("search", "").strip()
            if query and self.security.is_tool_allowed("web_search"):
                search_data = await self.security.run_with_limits(TOOL_REGISTRY["web_search"], {"query": query}, "web_search")
                tool_result = f"Search results: {search_data}"

        elif "system" in text_lower or "status" in text_lower or "система" in text_lower:
            if self.security.is_tool_allowed("system_info"):
                sys_info = await self.security.run_with_limits(TOOL_REGISTRY["system_info"], {}, "system_info")
                tool_result = f"System: CPU {sys_info.get('cpu_percent')}%, RAM {sys_info.get('ram_percent')}%, Disk Free {sys_info.get('disk_free_gb')} GB."

        if tool_result:
            prompt["messages"].append({"role": "system", "content": f"Internal tool execution result: {tool_result}. Answer the user based on this data."})

        llm_reply, _ = await self.llm.chat(prompt)
        reply = f"{prefix} {llm_reply}"

        self.memory.add("agent", reply)
        return reply