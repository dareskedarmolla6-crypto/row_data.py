
# fse/execution/sl_tp_handler.py
import logging

logger = logging.getLogger(__name__)

# =========================================================
# SMART ORDER ENHANCER
# =========================================================
class SmartOrderEnhancer:
    """በገበያ መዋዠቅ (Volatility) መሰረት የትዕዛዝ መጠኑን የሚያስተካክል (መርህ #4)።"""
    
    def enhance(self, signal, market_data):
        volatility = market_data.get("volatility", 0.5)
        # ከፍተኛ መዋዠቅ ሲኖር የትዕዛዝ መጠኑን መቀነስ (Risk Protection)
        original_qty = signal.get("qty", 1.0)
        signal["qty"] = max(0.01, original_qty * (1 - min(volatility, 0.9)))
        return signal

# =========================================================
# TRAILING STOP CONFIG
# =========================================================
class TrailingConfig:
    """የTrailing Stop መቼቶች (Activation & Distance)።"""
    
    def __init__(self, activation=0.05, distance=0.02):
        self.activation = activation  # 5% ትርፍ ሲደርስ ይነቃቃል
        self.distance = distance      # 2% የኋላ ርቀት (Trailing step)

# =========================================================
# TRAILING STOP ENGINE
# =========================================================
class TrailingEngine:
    """ትርፍን ለመቆለፍ እና ኪሳራን ለመቀነስ የሚረዳ ስልት (መርህ #9)።"""
    
    def __init__(self, config=None):
        self.config = config or TrailingConfig()

    def update(self, position, current_price):
        """ለLONG እና SHORT ቦታዎች የስታፕ-ሎስ ዋጋን ማዘመን።"""
        try:
            # LONG POSITION (BUY)
            if position.side == "BUY":
                trigger_price = position.entry_price * (1 + self.config.activation)
                if current_price > trigger_price:
                    new_sl = current_price * (1 - self.config.distance)
                    if new_sl > position.stop_loss:
                        position.stop_loss = new_sl
                        return new_sl

            # SHORT POSITION (SELL)
            elif position.side == "SELL":
                trigger_price = position.entry_price * (1 - self.config.activation)
                if current_price < trigger_price:
                    new_sl = current_price * (1 + self.config.distance)
                    if new_sl < position.stop_loss or position.stop_loss == 0:
                        position.stop_loss = new_sl
                        return new_sl
        except Exception as e:
            logger.error(f"❌ Trailing Stop Error: {e}")
            
        return None
