# fse/dashboard/ui_state_manager.py
import logging

logger = logging.getLogger(__name__)

class SystemStatus:
    """የቦቱን የስርዓት ሁኔታ እና የሪስክ ደረጃ የሚቆጣጠር (መርህ #9)"""
    
    def get_status(self, balance, open_positions, running=True, system_error=None):
        # ബാലንስ שלילי እንዳይሆን መከላከል (Safety Guard)
        safe_balance = max(0.0, balance)
        risk_level = self._risk_level(safe_balance, open_positions)

        return {
            "balance": safe_balance,
            "open_positions": len(open_positions),
            "status": "RUNNING" if running and safe_balance > 0 else "STOPPED",
            "risk_level": risk_level,
            "system_error": system_error
        }

    def _risk_level(self, balance, open_positions):
        exposure = len(open_positions)
        if balance <= 0: return "CRITICAL"
        if exposure == 0: return "LOW"
        if exposure <= 5: return "MEDIUM" # መርህ #9: እስከ 5 ቦታዎች መካከለኛ ሪስክ
        return "HIGH" # ከዛ በላይ ከፍተኛ ሪስክ

# =========================
# PROFIT TRACKER (IMPROVED)
# =========================
class ProfitTracker:
    """የትርፍ እና የኪሳራ (Drawdown) መከታተያ (መርህ #7)"""
    
    def __init__(self):
        self.peak = None

    def calculate_profit(self, start_balance, current_balance):
        if start_balance <= 0:
            return {"profit": 0, "profit_percent": 0, "drawdown": 0, "peak_balance": current_balance}

        profit = current_balance - start_balance
        profit_percent = (profit / start_balance) * 100
        
        # የፒክ (Peak) መከታተያ ለ Drawdown ግንዛቤ
        if self.peak is None or current_balance > self.peak:
            self.peak = current_balance

        drawdown = max(0.0, self.peak - current_balance)

        return {
            "profit": round(profit, 2),
            "profit_percent": round(profit_percent, 2),
            "drawdown": round(drawdown, 2),
            "peak_balance": self.peak
        }

    def reset_peak(self):
        """ፒክ መለኪያውን ዳግም ማስጀመር"""
        self.peak = None
        logger.info("ℹ️ Peak balance reset.")
