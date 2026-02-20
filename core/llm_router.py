import aiohttp
import logging

logger = logging.getLogger(__name__)

class LLMRouter:
    def __init__(self, config):
        self.config = config
        self.primary = config.get("primary", "jan")
    
    async def chat(self, prompt, context=None):
        if self.primary == "jan":
            return await self._call_jan(prompt)
        return "LLM не настроена", []

    async def _call_jan(self, prompt):
        url = self.config.get("jan", {}).get("base_url", "http://127.0.0.1:1337/v1")
        model = self.config.get("jan", {}).get("model", "local-gguf")
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{url}/chat/completions",
                    json={"model": model, "messages": prompt["messages"], "temperature": 0.7},
                    timeout=30
                ) as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        return data["choices"][0]["message"]["content"], []
                    return f"[Jan API Error {resp.status}]: Убедитесь, что сервер запущен", []
        except Exception as e:
            logger.error(f"Jan API Error: {e}")
            return f"[Ошибка соединения с Jan API по адресу {url}]: {str(e)}", []