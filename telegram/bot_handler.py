# fse/telegram/bot_handler.py
import requests
import asyncio
import logging

logger = logging.getLogger(__name__)

# =========================
# TELEGRAM BOT HANDLER
# =========================
class TelegramBot:
    """የቴሌግራም መልዕክት አስተላላፊ ክፍል (መርህ #7)።"""
    def __init__(self, token: str = None, chat_id: str = None):
        self.token = token
        self.chat_id = chat_id
        self.base_url = f"https://api.telegram.org/bot{token}" if token else None

    async def send_message(self, msg: str):
        """መልዕክትን ወደ ቴሌግራም መላክ።"""
        if self.base_url and self.chat_id:
            try:
                # requests.post በአሲንክሮነስ ኮድ ውስጥ ለትንሽ ስራ ተቀባይነት አለው
                requests.post(
                    f"{self.base_url}/sendMessage",
                    json={"chat_id": self.chat_id, "text": msg},
                    timeout=5
                )
            except Exception as e:
                logger.error(f"❌ Telegram Error: {e}")
        else:
            logger.info(f"📲 Mock Telegram: {msg}")

# =========================
# BOT STATE MANAGER
# =========================
class BotState:
    """የቦቱን ሁኔታ መከታተያ።"""
    def __init__(self):
        self.running = False
        self.total_profit = 0.0

state = BotState()

# =========================
# COMMAND HANDLERS
# =========================
async def start_handler(update, context):
    await update.message.reply_text("🚀 FSE CORE SYSTEM READY")

async def run_bot_handler(update, context):
    if state.running:
        await update.message.reply_text("⚠️ BOT ALREADY RUNNING")
        return
    state.running = True
    await update.message.reply_text("🟢 TRADING STARTED")
    # የንግድ ሉፕ (Trading Loop) እዚህ ጋር ይጀመራል

async def stop_bot_handler(update, context):
    state.running = False
    await update.message.reply_text("🔴 TRADING STOPPED")

async def status_handler(update, context):
    s = "RUNNING 🟢" if state.running else "STOPPED 🔴"
    await update.message.reply_text(f"📊 SYSTEM STATUS: {s}")

async def profit_handler(update, context):
    await update.message.reply_text(f"💰 TOTAL PROFIT: ${round(state.total_profit, 2)}")

