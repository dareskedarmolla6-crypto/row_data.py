import time
import uuid
import hashlib


# =========================================================
# IDEMPOTENCY KEY
# =========================================================
def generate_idempotency_key(symbol, side, qty, strategy_id, bucket):
    raw = f"{symbol}:{side}:{qty}:{strategy_id}:{bucket}"
    return hashlib.sha256(raw.encode()).hexdigest()


# =========================================================
# LIVE EXECUTOR (DIRECT EXECUTION LAYER)
# =========================================================
class LiveExecutor:
    def __init__(self, exchange):
        self.exchange = exchange

    def execute_trade(self, decision, symbol, size):

        if decision == "LONG":
            return self.exchange.place_order(symbol, "BUY", size)

        elif decision == "SHORT":
            return self.exchange.place_order(symbol, "SELL", size)

        elif decision == "GRID":
            orders = []
            step = size / 3

            for _ in range(3):
                orders.append(
                    self.exchange.place_order(symbol, "BUY", step)
                )

            return orders

        elif decision == "HEDGE":
            return {
                "LONG": self.exchange.place_order(symbol, "BUY", size / 2),
                "SHORT": self.exchange.place_order(symbol, "SELL", size / 2)
            }

        return None


# =========================================================
# EXCHANGE EXECUTOR (LOW-LEVEL API WRAPPER)
# =========================================================
class ExchangeExecutor:
    def __init__(self, api):
        self.api = api

    def open_order(self, symbol, side, quantity):
        try:
            order = self.api.create_order(
                symbol=symbol,
                side=side,
                type="MARKET",
                quantity=quantity
            )
            return {
                "status": "OPENED",
                "order": order
            }

        except Exception as e:
            return {
                "status": "ERROR",
                "message": str(e)
            }


# =========================================================
# POSITION MANAGER
# =========================================================
class PositionManager:
    def __init__(self):
        self.positions = []

    def add_position(self, order):
        self.positions.append(order)

    def close_position(self, position_id):
        for p in self.positions:
            if p.get("id") == position_id:
                p["status"] = "CLOSED"
                return p
        return "NOT_FOUND"


# =========================================================
# EXECUTION COORDINATOR (RISK + EXECUTION ORCHESTRATION)
# =========================================================
class ExecutionCoordinator:
    def __init__(self, risk_engine, gateway, store, verifier, lock_mgr):
        self.risk = risk_engine
        self.gateway = gateway
        self.store = store
        self.verifier = verifier
        self.lock = lock_mgr

    def execute_signal(self, signal):

        if self.store.get("system_status") in ["STOP", "EMERGENCY"]:
            raise Exception("SYSTEM HALTED")

        with self.lock.acquire(signal["portfolio_id"]):

            if not self.risk.validate_new_position(signal):
                return None

            trade_id = f"BOT_{uuid.uuid4().hex[:16]}"

            trade = {
                "trade_id": trade_id,
                "symbol": signal["symbol"],
                "side": signal["side"],
                "status": "CREATED",
                "repair_attempts": 0,
                "ts": time.time()
            }

            self.store.save(trade)

            key = generate_idempotency_key(
                signal["symbol"],
                signal["side"],
                signal["qty"],
                signal["strategy_id"],
                int(time.time() // 60)
            )

            resp = self.gateway.place_order(
                signal,
                idempotency_key=key
            )

            return self.verifier.verify_order(
                trade_id,
                signal["symbol"],
                resp["orderId"]
            )


# =========================================================
# MULTI MARKET EXECUTION ENGINE
# =========================================================
class MultiMarketExecutionEngine:
    def __init__(self, router, notifier, controller):
        self.router = router
        self.notifier = notifier
        self.controller = controller

    def execute(self, signal):
        result = self.controller.place_order(
            signal["symbol"],
            signal["side"],
            signal["qty"]
        )

        return self.notifier.notify_and_return(
            signal["symbol"],
            signal["side"],
            result
        )
