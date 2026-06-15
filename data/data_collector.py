
# fse/data/data_collector.py
import random
import logging

logger = logging.getLogger(__name__)

# =========================
# LIVE MARKET DATA
# =========================
def get_market_data():
    """የቀጥታ ገበያ መረጃን ማስመሰል (ሲሙሌሽን)።"""
    return {
        "price_change": round(random.uniform(-5, 5), 2),
        "volume": round(random.uniform(0, 100), 2),
        "volatility": round(random.uniform(0, 1), 4)
    }

# =========================
# HISTORICAL DATA LOADER
# =========================
class DataLoader:
    """ታሪካዊ መረጃዎችን ለመጫን የሚያገለግል ክፍል (መርህ #3)።"""
    
    def load(self, historical_data):
        if not historical_data:
            logger.warning("⚠️ No historical data provided.")
            return []
        return historical_data

# =========================
# MARKET STREAM WRAPPER
# =========================
class MarketDataStream:
    """ከምንጭ መረጃን ለማግኘት የሚያገለግል መጠቅለያ (Wrapper)።"""
    
    def __init__(self, source):
        self.source = source

    def get(self, symbol):
        """ከምንጩ መረጃን ማምጣት።"""
        try:
            return self.source.get(symbol)
        except Exception as e:
            logger.error(f"❌ Data fetch error for {symbol}: {e}")
            return None

    def safe_get(self, symbol):
        """None እንዳይመለስ መከላከል (Safety Guard)።"""
        data = self.get(symbol)
        if data is None:
            logger.warning(f"⚠️ Safe mode: Defaulting data for {symbol}")
            return {
                "price_change": 0.0,
                "volume": 0.0,
                "volatility": 0.0
            }
        return data
