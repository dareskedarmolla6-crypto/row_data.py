import random
import time


# =========================
# LIVE MARKET DATA
# =========================
def get_market_data():
    return {
        "price_change": random.uniform(-5, 5),
        "volume": random.uniform(0, 100),
        "volatility": random.uniform(0, 1)
    }


# =========================
# HISTORICAL DATA LOADER
# =========================
class DataLoader:
    def load(self, historical_data):
        return historical_data


# =========================
# MARKET STREAM WRAPPER
# =========================
class MarketDataStream:
    def __init__(self, source):
        self.source = source

    def get(self, symbol):
        return self.source.get(symbol)
# Safety improvement: prevent None returns breaking pipeline
def safe_get(self, symbol):
    data = self.get(symbol)
    return data if data is not None else {
        "price_change": 0,
        "volume": 0,
        "volatility": 0
    }
