#!/usr/bin/env python3
import asyncio
import logging
import os
from dotenv import load_dotenv

from config.loader import load_config
from core.agent import Agent
from channels.web_ui import start_web_ui
from channels.telegram_bot import TelegramBot

logging.basicConfig(level=logging.INFO)
load_dotenv()

async def main():
    print("🚀 Запуск LightweightClaw...")
    
    # Загружаем полную конфигурацию из файлов
    config = load_config("config/config.yaml")
    agent = Agent(config)
    
    tasks = [
        start_web_ui(agent)
    ]
    
    tg_token = os.getenv("TELEGRAM_BOT_TOKEN")
    if tg_token and "твой_токен" not in tg_token:
        bot = TelegramBot(agent, tg_token)
        tasks.append(bot.start_bot())
        print("📱 Модуль Telegram подключен.")
        
    await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(main())