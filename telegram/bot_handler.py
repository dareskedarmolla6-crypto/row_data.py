import requests
import asyncio
import random


# =========================
# TELEGRAM SIMPLE SENDER
# =========================
class TelegramBot:
    def __init__(self, token: str = None, chat_id: str = None):
        self.token = token
        self.chat_id = chat_id
        self.base_url = f"https://api.telegram.org/bot{token}" if token else None

    async def send_message(self, msg: str):
        print(f"📲 TELEGRAM: {msg}")

        # real telegram send (if configured)
        if self.base_url and self.chat_id:
            try:
                requests.post(
                    f"{self.base_url}/sendMessage",
                    json={"chat_id": self.chat_id, "text": msg},
                    timeout=5
                )
            except Exception as e:
                print("Telegram Error:", e)


# =========================
# SIMPLE BOT STATE
# =========================
class BotState:
    def __init__(self):
        self.running = False
        self.total_profit = 0.0


state = BotState()


# =========================
# SIMPLE MARKET + BRAIN MOCK
# =========================
def market_feed(symbol):
    return {
        "symbol": symbol,
        "price_change": random.uniform(-3, 3)
    }


def brain(data):
    if data["price_change"] > 1:
        return "LONG", 80
    elif data["price_change"] < -1:
        return "SHORT", 80
    return "HEDGE", 55


# =========================
# TRADING LOOP
# =========================
async def trading_loop(telegram: TelegramBot):
    symbol = "DOGEUSDT"

    while state.running:
        data = market_feed(symbol)
        signal, confidence = brain(data)

        pnl = random.uniform(-2, 3)
        state.total_profit += pnl

        await telegram.send_message(
            f"📊 {symbol} | {signal} | CONF: {confidence} | PnL: {round(pnl,2)}"
        )

        await asyncio.sleep(3)


# =========================
# TELEGRAM COMMAND HANDLERS
# =========================
async def start(update, context):
    await update.message.reply_text("🚀 FSE READY")


async def run_bot(update, context):
    if state.running:
        await update.message.reply_text("⚠️ BOT ALREADY RUNNING")
        return

    state.running = True
    await update.message.reply_text("🟢 TRADING STARTED")

    telegram = TelegramBot()
    asyncio.create_task(trading_loop(telegram))


async def stop_bot(update, context):
    state.running = False
    await update.message.reply_text("🔴 TRADING STOPPED")


async def status(update, context):
    status_text = "RUNNING 🟢" if state.running else "STOPPED 🔴"
    await update.message.reply_text(f"📊 STATUS: {status_text}")


async def profit(update, context):
    await update.message.reply_text(
        f"💰 TOTAL PROFIT: {round(state.total_profit, 2)}$"
    )
