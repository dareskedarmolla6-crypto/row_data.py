import time


# =========================
# BALANCE TRACKER CORE
# =========================
class BalanceTracker:
    def __init__(self, initial_balance=1000):
        self.initial_balance = initial_balance
        self.balance = initial_balance
        self.equity_peak = initial_balance
        self.drawdown = 0
        self.history = []

    # -------------------------
    # UPDATE BALANCE (PnL APPLY)
    # -------------------------
    def update(self, pnl, metadata=None):
        self.balance += pnl

        if self.balance > self.equity_peak:
            self.equity_peak = self.balance

        self.drawdown = self.equity_peak - self.balance

        record = {
            "time": time.time(),
            "pnl": pnl,
            "balance": self.balance,
            "drawdown": self.drawdown,
            "metadata": metadata or {}
        }

        self.history.append(record)
        return record

    # -------------------------
    # GET CURRENT STATUS
    # -------------------------
    def status(self):
        return {
            "balance": round(self.balance, 2),
            "equity_peak": round(self.equity_peak, 2),
            "drawdown": round(self.drawdown, 2),
            "drawdown_percent": round((self.drawdown / self.equity_peak) * 100, 2) if self.equity_peak else 0
        }

    # -------------------------
    # RISK ALERT CHECK
    # -------------------------
    def risk_flag(self, max_drawdown_percent=20):
        dd_percent = (self.drawdown / self.equity_peak) * 100 if self.equity_peak else 0

        if dd_percent >= max_drawdown_percent:
            return {
                "status": "RISK_BREACH",
                "drawdown_percent": round(dd_percent, 2)
            }

        return {
            "status": "OK",
            "drawdown_percent": round(dd_percent, 2)
        }

    # -------------------------
    # RESET (FOR BACKTEST)
    # -------------------------
    def reset(self):
        self.balance = self.initial_balance
        self.equity_peak = self.initial_balance
        self.drawdown = 0
        self.history.clear()
