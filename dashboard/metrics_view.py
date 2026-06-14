# fse/dashboard/metrics_view.py

import time


# =========================
# TRADE HISTORY TRACKER
# =========================
class TradeHistory:
    def __init__(self):
        self.trades = []

    def log_trade(self, trade):
        trade["timestamp"] = time.time()
        self.trades.append(trade)

    def get_trades(self):
        return self.trades

    def get_stats(self):
        total = len(self.trades)
        profit_trades = len([t for t in self.trades if t.get("profit", 0) > 0])

        win_rate = (profit_trades / total) * 100 if total > 0 else 0

        return {
            "total_trades": total,
            "win_rate": round(win_rate, 2)
        }


# =========================
# DASHBOARD VIEW
# =========================
class Dashboard:
    def show(self, tg, status, profit, trades, win_rate=None):

        msg = (
            f"📊 FSE DASHBOARD\n\n"
            f"💰 Balance: {status['balance']}\n"
            f"📦 Open Positions: {status['open_positions']}\n"
            f"📈 Profit: {profit}\n"
            f"📊 Total Trades: {len(trades)}\n"
        )

        if win_rate is not None:
            msg += f"🎯 Win Rate: {win_rate}%\n"

        msg += f"⚙️ Status: {status['status']}"

        tg.send(msg)
