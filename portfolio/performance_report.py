# fse/portfolio/performance_report.py
import logging

logger = logging.getLogger(__name__)

# =========================
# PAPER TRADING ENGINE
# =========================
class PaperTradingEngine:
    """የንግድ ስራን የሚያስመስል (Simulation) ክፍል (መርህ #1)።"""
    
    def __init__(self, initial_capital=1000.0):
        self.balance = float(initial_capital)
        self.trades = []

    def simulate_trade(self, symbol, side, qty, price):
        """ለሙከራ ያህል የንግድ ልውውጥን መመዝገብ።"""
        trade = {
            "symbol": symbol, "side": side,
            "qty": qty, "price": price, "status": "SIMULATED"
        }
        self.trades.append(trade)
        logger.info(f"🧪 Simulated trade: {side} {symbol} at {price}")
        return trade

# =========================
# PERFORMANCE REPORT GENERATOR
# =========================
class PerformanceReport:
    """የንግድ ስራ አፈጻጸም ሪፖርት ማዘጋጃ ክፍል (መርህ #7)።"""
    
    def __init__(self, history):
        self.history = history

    def generate(self):
        """የንግድ ታሪክን መሰረት አድርጎ አጠቃላይ ሪፖርት ማዘጋጀት።"""
        total = len(self.history)
        if total == 0:
            return {"message": "No trades to report."}

        wins = len([t for t in self.history if t.get("pnl", 0) > 0])
        total_pnl = sum(t.get("pnl", 0) for t in self.history)
        win_rate = (wins / total) * 100

        report = {
            "total_trades": total,
            "win_rate_percent": round(win_rate, 2),
            "net_pnl": round(total_pnl, 2),
            "average_pnl": round(total_pnl / total, 2)
        }
        
        logger.info(f"📈 PERFORMANCE REPORT: {report}")
        return report
