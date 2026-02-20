from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import logging

logger = logging.getLogger(__name__)

class TelegramBot:
    def __init__(self, agent, token):
        self.agent = agent
        self.token = token
        self.app = Application.builder().token(self.token).build()
        
        self.app.add_handler(CommandHandler("start", self.start_cmd))
        self.app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_message))
    
    async def start_cmd(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text("🤖 LightweightClaw запущен! Выберите персону в Web UI или общайтесь здесь (по умолчанию активна Mira).")
    
    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        text = update.message.text
        await update.message.chat.send_action("typing")
        
        # В Telegram по умолчанию общаемся с Мирой
        reply = await self.agent.process(text, persona_name="mira", channel="telegram")
        await update.message.reply_text(reply)
        
    async def start_bot(self):
        await self.app.initialize()
        await self.app.start()
        await self.app.updater.start_polling()