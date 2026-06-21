import time
import uuid
import hashlib
import logging
from execution.connection_tester import test_api_connection

logger = logging.getLogger(__name__)

# ==========================================================
# IDEMPOTENCY KEY (የተባዙ ትዕዛዞችን ለመከላከል)
# ==========================================================
def generate_idempotency_key(symbol, side, qty, strategy_id, bucket):
    raw = f"{symbol}:{side}:{qty}:{strategy_id}:{bucket}"
    return hashlib.sha256(raw.encode()).hexdigest()

# ==========================================================
# BINANCE GATEWAY
# ==========================================================
class BinanceGateway:
    """ከBinance API ጋር የሚገናኝ የትዕዛዝ መፈጸሚያ።"""
    
    def __init__(self, client):
        self.client = client

    def place_order(self, symbol, side, qty, leverage=20, idempotency_key=None):
        try:
            self.client.futures_change_leverage(symbol=symbol, leverage=min(leverage, 20))
            return self.client.futures_create_order(
                symbol=symbol,
                side=side,
                type="MARKET",
                quantity=qty,
                newClientOrderId=idempotency_key
            )
        except Exception as e:
            logger.error(f"❌ Order placement failed: {e}")
            return None

    def query_order(self, symbol, order_id):
        try:
            return self.client.futures_get_order(symbol=symbol, orderId=order_id)
        except Exception:
            return None

    def close_position(self, symbol):
        pos = self.client.futures_position_information(symbol=symbol)
        if not pos or float(pos[0]["positionAmt"]) == 0:
            return None
        
        qty = abs(float(pos[0]["positionAmt"]))
        side = "SELL" if float(pos[0]["positionAmt"]) > 0 else "BUY"
        return self.client.futures_create_order(symbol=symbol, side=side, type="MARKET", quantity=qty)

# ==========================================================
# EXECUTION COORDINATOR
# ==========================================================
class ExecutionCoordinator:
    """የትዕዛዝ ፍሰትን የሚቆጣጠር እና የሚያስተባብር ክፍል (መርህ #11)።"""
    
    def __init__(self, risk_engine, gateway, store, verifier, lock):
        self.risk = risk_engine
        self.gateway = gateway
        self.store = store
        self.verifier = verifier
        self.lock = lock

    def execute_signal(self, signal):
        # [Fail-Safe Check] ቦቱ ትሬድ ከመፈጸሙ በፊት ሰርቨሩ መኖሩን ያረጋግጣል
        if not test_api_connection():
            logger.critical("🚨 CONNECTION LOST: ትዕዛዝ መላክ አልተቻለም፣ ስራው ቆሟል!")
            raise Exception("SYSTEM HALTED - NO CONNECTION TO EXCHANGE")

        if self.store.get("system_status") in ["STOP", "EMERGENCY"]:
            raise Exception("SYSTEM HALTED - EMERGENCY STOP")

        with self.lock.acquire(signal["portfolio_id"]):
            if not self.risk.validate_new_position(signal):
                logger.warning("⚠️ Signal rejected by Risk Engine.")
                return None

            trade_id = f"BOT_{uuid.uuid4().hex[:16]}"
            key = generate_idempotency_key(
                signal["symbol"], signal["side"], signal["qty"], 
                signal["strategy_id"], int(time.time() // 60)
            )

            resp = self.gateway.place_order(
                signal["symbol"], signal["side"], signal["qty"], 
                signal.get("leverage", 20), key
            )

            if resp:
                self.store.save({
                    "trade_id": trade_id, "order_id": resp["orderId"],
                    "symbol": signal["symbol"], "status": "OPEN", "ts": time.time()
                })
                return self.verifier.verify_order(trade_id, signal["symbol"], resp["orderId"])
            return None

# ==========================================================
# LIVE SYNC ENGINE
# ==========================================================
class LiveSyncEngine:
    """ከትክክለኛው የልውውጥ ሁኔታ ጋር ቦቱን የሚያመሳስል (Sync) ክፍል (መርህ #6)።"""
    
    def __init__(self, gateway, store):
        self.gateway = gateway
        self.store = store

    def sync(self):
        for trade in self.store.get_active_trades():
            order = self.gateway.query_order(trade["symbol"], trade["order_id"])
            if order and order["status"] == "FILLED":
                logger.info(f"✅ Trade {trade['trade_id']} synced as FILLED.")
