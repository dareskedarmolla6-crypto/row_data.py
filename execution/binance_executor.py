
# fse/execution/binance_executor.py
import logging
import uuid
import hashlib

# ለሎግ (Logging) ማዋቀር
logger = logging.getLogger(__name__)

# =========================
# IDEMPOTENCY KEY
# =========================
def generate_idempotency_key(symbol, side, qty, strategy_id, bucket):
    raw = f"{symbol}:{side}:{qty}:{strategy_id}:{bucket}"
    return hashlib.sha256(raw.encode()).hexdigest()

# =========================
# BINANCE EXECUTOR CORE
# =========================
class BinanceExecutor:
    """ከBinance Futures API ጋር በቀጥታ የሚገናኝ ዋና መፈጸሚያ።"""
    
    def __init__(self, client):
        self.client = client

    def open_long(self, symbol, quantity, leverage=20):
        try:
            self.client.futures_change_leverage(symbol=symbol, leverage=min(leverage, 20))
            order = self.client.futures_create_order(
                symbol=symbol, side="BUY", type="MARKET", quantity=quantity
            )
            logger.info(f"📈 LONG OPENED: {symbol} | Qty: {quantity}")
            return order
        except Exception as e:
            logger.error(f"❌ LONG ERROR for {symbol}: {e}")
            return {"status": "ERROR", "message": str(e)}

    def open_short(self, symbol, quantity, leverage=20):
        try:
            self.client.futures_change_leverage(symbol=symbol, leverage=min(leverage, 20))
            order = self.client.futures_create_order(
                symbol=symbol, side="SELL", type="MARKET", quantity=quantity
            )
            logger.info(f"📉 SHORT OPENED: {symbol} | Qty: {quantity}")
            return order
        except Exception as e:
            logger.error(f"❌ SHORT ERROR for {symbol}: {e}")
            return {"status": "ERROR", "message": str(e)}

    def close_position(self, symbol):
        try:
            positions = self.client.futures_position_information(symbol=symbol)
            if not positions or float(positions[0]["positionAmt"]) == 0:
                return {"status": "ALREADY_FLAT"}

            pos = positions[0]
            qty = abs(float(pos["positionAmt"]))
            side = "SELL" if float(pos["positionAmt"]) > 0 else "BUY"

            order = self.client.futures_create_order(
                symbol=symbol, side=side, type="MARKET", quantity=qty
            )
            logger.info(f"🔴 POSITION CLOSED: {symbol}")
            return order
        except Exception as e:
            logger.error(f"❌ CLOSE ERROR for {symbol}: {e}")
            return {"status": "ERROR", "message": str(e)}

# =========================
# EXECUTION ROUTER
# =========================
class BinanceExecutionRouter:
    """ሲግናሎችን ተቀብሎ ወደBinance ትዕዛዝ የሚቀይር ማዕከል (Orchestrator)።"""
    
    def __init__(self, executor):
        self.executor = executor

    def execute(self, signal):
        symbol = signal.get("symbol")
        side = signal.get("side")
        qty = signal.get("qty", 0)

        if side == "LONG":
            return self.executor.open_long(symbol, qty)
        elif side == "SHORT":
            return self.executor.open_short(symbol, qty)
        elif side == "CLOSE":
            return self.executor.close_position(symbol)
        elif side == "HEDGE":
            return {
                "symbol": symbol,
                "long": self.executor.open_long(symbol, qty / 2),
                "short": self.executor.open_short(symbol, qty / 2),
                "status": "HEDGE_ACTIVE"
            }

        return {"status": "NO_ACTION", "reason": "Unknown signal"}
