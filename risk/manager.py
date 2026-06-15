
# fse/risk/risk_manager.py
import logging

logger = logging.getLogger(__name__)

# =========================
# RISK MANAGER (CAPITAL PROTECTION)
# =========================
class RiskManager:
    """ዋና የካፒታል ጥበቃ ክፍል (መርህ #9)።"""
    def __init__(self, max_daily_loss=0.05, max_exposure=0.3):
        self.max_daily_loss = max_daily_loss
        self.max_exposure = max_exposure

    def check_trade(self, balance, position_size, open_positions_sum):
        exposure = open_positions_sum / balance if balance > 0 else 0
        if (position_size / balance) > 0.02: return "REJECT: RISK TOO HIGH"
        if exposure > self.max_exposure: return "REJECT: EXPOSURE LIMIT"
        return "APPROVED"

    def emergency_stop(self, drawdown):
        return drawdown >= self.max_daily_loss

# =========================
# RISK ENGINE & ADJUSTER
# =========================
class RiskEngine:
    """የንግድ ማጽደቂያ እና የኪሳራ መቆጣጠሪያ።"""
    def __init__(self, max_loss=0.05, max_leverage=5):
        self.max_loss = max_loss
        self.max_leverage = max_leverage
        self.daily_loss = 0.0

    def approve_trade(self, signal, confidence, leverage):
        if confidence < 60: return False, "LOW CONFIDENCE"
        if leverage > self.max_leverage: return False, "LEVERAGE TOO HIGH"
        if self.daily_loss >= self.max_loss: return False, "DAILY LOSS LIMIT HIT"
        if signal not in ["LONG", "SHORT", "HEDGE"]: return False, "INVALID SIGNAL"
        return True, "APPROVED"

    def update_loss(self, loss): self.daily_loss += float(loss)

# =========================
# EMERGENCY & PROFIT MANAGEMENT
# =========================
class EmergencyStopEngine:
    """የከባድ አደጋ መከላከያ (Hard Protection)።"""
    def check(self, drawdown):
        if drawdown >= 0.15: return "STOP_ALL_TRADING"
        if drawdown >= 0.10: return "REDUCE_RISK"
        return "OK"

class ProfitLock:
    """ትርፍን መቆለፊያ እና አደጋን መቀነስ።"""
    def lock(self, position, profit):
        if profit > 0.05: position["stop_loss"] = profit * 0.5
        return position

# =========================
# SIGNAL VALIDATION & SCORING
# =========================
class SignalValidator:
    """የሲግናል ትክክለኛነት እና አዝማሚያ መፈተሻ።"""
    def validate(self, signal, market_data, higher_tf_trend):
        if market_data.get("volume", 0) < 100000: return False
        if signal.get("flip_count", 0) > 3: return False
        if higher_tf_trend and higher_tf_trend != signal.get("side"): return False
        return True

class SignalQualityScorer:
    """የሲግናል ጥራትን በቁጥር መለኪያ።"""
    def score(self, signal, market_data):
        vol = market_data.get("volume", 0)
        volat = market_data.get("volatility", 0)
        spr = market_data.get("spread", 0)
        score = min(vol / 10000, 50) + (volat * 100) - (spr * 20)
        return round(score, 2)

class AdvancedSignalValidationEngine:
    """የሲግናል ጥራት ማረጋገጫ ዋና ሞተር።"""
    def __init__(self):
        self.validator = SignalValidator()
        self.scorer = SignalQualityScorer()

    def process(self, signal, market_data, higher_tf_trend):
        return {
            "valid": self.validator.validate(signal, market_data, higher_tf_trend),
            "quality_score": self.scorer.score(signal, market_data)
        }
