#!/usr/bin/env python3
import asyncio
import logging
from core.agent import Agent
from channels.web_ui import start_web_ui
# from channels.telegram_bot import TelegramBot # Раскомментируй, если настроен токен

logging.basicConfig(level=logging.INFO)

async def main():
    print("🚀 Запуск LightweightClaw...")
    agent = Agent()
    
    tasks = [
        start_web_ui(agent),
        # TelegramBot(agent, "твой_токен").start() 
    ]
    await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(main())
