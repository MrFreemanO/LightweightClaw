import asyncio
import logging

logger = logging.getLogger(__name__)

class SecurityManager:
    def __init__(self, config):
        self.allowed_tools = set(config.get("allowed_tools", []))
        self.max_runtime = 30
        self.max_concurrent = 3
        self.task_count = 0
    
    def is_tool_allowed(self, tool_name):
        return tool_name in self.allowed_tools
    
    async def run_with_limits(self, tool_func, args, tool_name):
        if self.task_count >= self.max_concurrent:
            return {"error": "Достигнут лимит параллельных задач"}
        self.task_count += 1
        try:
            return await asyncio.wait_for(tool_func(**args), timeout=self.max_runtime)
        except asyncio.TimeoutError:
            return {"error": f"Превышено время выполнения инструмента {tool_name}"}
        except Exception as e:
            return {"error": str(e)}
        finally:
            self.task_count -= 1