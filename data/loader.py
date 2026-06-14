import random
import time
from datetime import datetime


# =========================
# CANDLE MODEL
# =========================
class Candle:
    def __init__(self, open_, high, low, close, volume):
        self.open = open_
        self.high = high
        self.low = low
        self.close = close
        self.volume = volume
        self.timestamp = datetime.utcnow()


# =========================
# MARKET DATA LOADER (SIMULATED)
# =========================
class MarketDataLoader:
    def __init__(self):
        self.last_price = 100

    def fetch_price(self, symbol):
        # simulate market movement
        change = random.uniform(-2, 2)
        self.last_price += change
        return round(self.last_price, 4)

    def generate_candle(self, symbol):
        open_price = self.fetch_price(symbol)
        high = open_price + random.uniform(0, 2)
        low = open_price - random.uniform(0, 2)
        close = self.fetch_price(symbol)
        volume = random.uniform(10, 1000)

        return Candle(open_price, high, low, close, volume)


# =========================
# STREAM LOADER
# =========================
class MarketStream:
    def __init__(self, symbol="DOGEUSDT"):
        self.symbol = symbol
        self.loader = MarketDataLoader()

    def stream(self):
