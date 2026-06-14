import asyncio
import json
import random
import time


# =========================
# MOCK MARKET DATA STREAM
# =========================
class MarketWebSocketFeed:
    """
    Simulated websocket feed (later replace with Binance/Bybit WS)
    """

    def __init__(self, symbol="DOGEUSDT"):
        self.symbol = symbol
        self.running = False

    async def stream_price(self):
        """
        Generates fake live market ticks
        """
        while self.running:
            tick = {
                "symbol": self.symbol,
                "price": round(random.uniform(0.08, 0.12), 5),
                "volume": random.uniform(100, 1000),
                "timestamp": time.time()
            }

            yield tick
            await asyncio.sleep(1)


# =========================
# DASHBOARD FEED BROADCASTER
# =========================
class DashboardFeed:
    """
    Sends structured data to dashboard UI (WebSocket layer)
    """

    def __init__(self):
        self.clients = set()

    def register(self, client):
        self.clients.add(client)

    def unregister(self, client):
        self.clients.discard(client)

    async def broadcast(self, message: dict):
        """
        Send data to all connected dashboard clients
        """
        if not self.clients:
            return

        payload = json.dumps(message)

        for client in list(self.clients):
            try:
                await client.send(payload)
            except:
                self.unregister(client)


# =========================
# BOT STATUS STREAM
# =========================
class BotStatus:
    def __init__(self):
        self.balance = 1000
        self.open_positions = 0
        self.last_signal = None
        self.last_confidence = 0

    def update(self, signal, confidence, balance_change=0):
        self.last_signal = signal
        self.last_confidence = confidence
        self.balance += balance_change

    def snapshot(self):
        return {
            "balance": self.balance,
            "open_positions": self.open_positions,
            "last_signal": self.last_signal,
            "confidence": self.last_confidence,
            "timestamp": time.time()
        }


# =========================
# MAIN STREAM ENGINE
# =========================
class WebSocketFeedEngine:
    def __init__(self, feed: MarketWebSocketFeed, dashboard: DashboardFeed, status: BotStatus):
        self.feed = feed
        self.dashboard = dashboard
        self.status = status
        self.running = False

    async def run(self):
        self.running = True
        self.feed.running = True

        async for tick in self.feed.stream_price():
            if not self.running:
                break

            # simulate signal (later replace with brain)
            signal = random.choice(["LONG", "SHORT", "HEDGE", "NONE"])
            confidence = random.randint(10, 95)

            self.status.update(signal, confidence)

            message = {
                "market": tick,
                "bot": self.status.snapshot(),
                "signal": signal
            }

            await self.dashboard.broadcast(message)

    def stop(self):
        self.running = False
        self.feed.running = False
# Safety improvement: ensure stream stops cleanly on engine stop
def safe_stop(self):
    self.stop()
    self.feed.running = False
    self.dashboard.clients.clear()

# Optional safeguard: prevent NONE signal spam in production
MAX_NONE_SIGNALS = 3
