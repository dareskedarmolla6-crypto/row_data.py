# fse/execution/order_manager.py

import uuid


# =========================
# SIMPLE PAPER / LOG EXECUTION
# =========================
class ExecutionLogger:
    def open_long(self, symbol, size):
        print(f"📈 LONG OPEN: {symbol} | SIZE: {size}")

    def open_short(self, symbol, size):
        print(f"📉 SHORT OPEN: {symbol} | SIZE: {size}")


# =========================
# BINANCE REAL EXECUTOR
# =========================
class ExecutionEngine:
    def __init__(self, binance_client):
        self.client = binance_client

    def open_long(self, symbol, quantity):
        order = self.client.client.order_market_buy(
            symbol=symbol,
            quantity=quantity
        )
        print("📈 REAL LONG OPENED")
        return order

    def open_short(self, symbol, quantity):
        order = self.client.client.order_market_sell(
            symbol=symbol,
            quantity=quantity
        )
        print("📉 REAL SHORT OPENED")
        return order


# =========================
# HEDGE POSITION MODEL
# =========================
class HedgePosition:
    def __init__(self, symbol):
        self.symbol = symbol
        self.long_position = None
        self.short_position = None


# =========================
# HEDGE EXECUTION ENGINE
# =========================
class HedgeExecutionEngine:
    def __init__(self):
        self.registry = {}

    def hedge_open(self, symbol, long_trade, short_trade):
        hedge = HedgePosition(symbol)
        hedge.long_position = long_trade
        hedge.short_position = short_trade

        self.registry[symbol] = hedge
        return hedge


# =========================
# UNIFIED ORDER MANAGER
# =========================
class OrderManager:
    def __init__(self, execution_engine, hedge_engine):
        self.execution = execution_engine
        self.hedge = hedge_engine

    def execute(self, signal):
        symbol = signal["symbol"]
        side = signal["side"]
        qty = signal["qty"]

        if side == "LONG":
            return self.execution.open_long(symbol, qty)

        if side == "SHORT":
            return self.execution.open_short(symbol, qty)

        if side == "HEDGE":
            long_trade = self.execution.open_long(symbol, qty / 2)
            short_trade = self.execution.open_short(symbol, qty / 2)

            return self.hedge.hedge_open(symbol, long_trade, short_trade)

        return {"status": "NO_ACTION", "reason": "Unknown signal"}
