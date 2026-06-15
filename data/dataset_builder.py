
# fse/data/dataset_builder.py
import random
import logging

logger = logging.getLogger(__name__)

# =========================
# MARKET DATA SOURCE (MOCK / REAL READY)
# =========================
class FakeMarketSource:
    """የገበያ መረጃ ምንጭ (ሲሙሌሽን)።"""
    
    def __init__(self, coins=None):
        self.coins = coins or [
            "BTCUSDT", "ETHUSDT", "SOLUSDT",
            "DOGEUSDT", "PEPEUSDT", "ARBUSDT"
        ]

    def get_all(self):
        """ለሁሉም ኮይኖች የገበያ መረጃን ማመንጨት።"""
        data = {}
        for coin in self.coins:
            data[coin] = {
                "volatility": round(random.uniform(0.1, 2.5), 4),
                "volume": round(random.uniform(1_000, 1_000_000), 2),
                "momentum": round(random.uniform(-1, 1), 4),
                "price_change": round(random.uniform(-5, 5), 2)
            }
        return data

# =========================
# MARKET FEED WRAPPER
# =========================
class MarketFeed:
    """የገበያ መረጃን ለማደራጀት እና ለማቅረብ የሚያገለግል ክፍል (መርህ #3)።"""
    
    def __init__(self, market_data_source):
        self.source = market_data_source

    def get_snapshot(self):
        return self.source.get_all()

    def get_symbol_data(self, symbol):
        """የአንድ የተወሰነ ምልክት መረጃን ማግኘት።"""
        data = self.source.get_all()
        return data.get(symbol)

    def safe_get_symbol_data(self, symbol):
        """None እንዳይመለስ እና ሲስተሙ እንዳይበላሽ መከላከል (Safety Guard)።"""
        data = self.get_symbol_data(symbol)
        if data is None:
            logger.warning(f"⚠️ Market data missing for {symbol}. Returning default values.")
            return {
                "volatility": 0.0,
                "volume": 0.0,
                "momentum": 0.0,
                "price_change": 0.0
            }
        return data
