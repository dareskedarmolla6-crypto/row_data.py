# fse/execution/trade_router.py


# =========================================================
# SIMPLE TRADE ROUTER (SMART EXECUTION ENTRY)
# =========================================================
class TradeRouter:
    def __init__(self, exchanges):
        self.exchanges = exchanges  # exchange connectors dict

    def execute_best(self, signal):
        target = self._select_best_exchange(signal)
        return target.place_order(
            symbol=signal["symbol"],
            side=signal["side"],
            qty=signal["qty"]
        )

    def _select_best_exchange(self, signal):
        # Placeholder smart logic (can later include fees, liquidity, latency)
        return self.exchanges.get("BINANCE")


# =========================================================
# EXECUTION CONTROL ENGINE
# =========================================================
class ExecutionControlEngine:
    def execute_trade(self, decision):
        if decision == "WAIT":
            return "NO_ACTION"

        if decision in ["BUY", "STRONG_BUY"]:
            return "OPEN_LONG"

        if decision in ["SELL", "STRONG_SELL"]:
            return "OPEN_SHORT"

        return "NO_ACTION"


# =========================================================
# TAKE PROFIT ENGINE
# =========================================================
class TakeProfitEngine:
    def manage_profit(self, position):
        profit = position.get("profit", 0)
        capital = position.get("capital", 1)

        if profit >= 0.25 * capital:
            return "LOCK_PROFIT"

        if profit >= 0.10 * capital:
            return "PARTIAL_TP"

        return "HOLD"


# =========================================================
# MULTI-EXCHANGE ROUTER
# =========================================================
class MultiExchangeRouter:
    def __init__(self, exchanges):
        self.exchanges = exchanges

    def best_price(self, symbol):
        best_price = None
        best_exchange = None

        for name, ex in self.exchanges.items():
            price = ex.get_price(symbol)

            if best_price is None or price < best_price:
                best_price = price
                best_exchange = name

        return best_exchange, best_price

    def place_order(self, symbol, side, qty):
        ex_name, price = self.best_price(symbol)

        return self.exchanges[ex_name].place_order({
            "symbol": symbol,
            "side": side,
            "qty": qty,
            "price": price
        })


# =========================================================
# UNIFIED MARKET CONTROLLER
# =========================================================
class UnifiedMarketController:
    def __init__(self, router):
        self.router = router

    def route(self, symbol, side, qty):
        ex_name, price = self.router.best_price(symbol)

        return self.router.exchanges[ex_name].place_order({
            "symbol": symbol,
            "side": side,
            "qty": qty,
            "price": price
        })
