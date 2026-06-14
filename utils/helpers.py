import time
import uuid
import hashlib
import random


# =========================
# ID GENERATION
# =========================
def generate_id():
    return str(uuid.uuid4())


def short_id(prefix="BOT"):
    return f"{prefix}_{uuid.uuid4().hex[:12]}"


# =========================
# IDEMPOTENCY KEY (VERY IMPORTANT FOR TRADING SAFETY)
# =========================
def generate_idempotency_key(symbol, side, qty, strategy_id, bucket=None):
    if bucket is None:
        bucket = int(time.time() // 60)  # 1-minute window

    raw = f"{symbol}:{side}:{qty}:{strategy_id}:{bucket}"
    return hashlib.sha256(raw.encode()).hexdigest()


# =========================
# SAFE NUMBER HELPERS
# =========================
def clamp(value, min_value, max_value):
    return max(min_value, min(value, max_value))


def normalize(value, min_value, max_value):
    if max_value == min_value:
        return 0
    return (value - min_value) / (max_value - min_value)


# =========================
# POSITION SIZE HELPERS
# =========================
def calculate_position_size(balance, risk_percent):
    """
    risk_percent: 0 - 100
    """
    return balance * (risk_percent / 100)


def safe_qty(qty, min_qty=0.001):
    return max(qty, min_qty)


# =========================
# MARKET HELPERS
# =========================
def is_volatile(price_change, threshold=2.0):
    return abs(price_change) >= threshold


def direction_from_change(price_change):
    if price_change > 0:
        return "UP"
    elif price_change < 0:
        return "DOWN"
    return "FLAT"


# =========================
# RANDOM MARKET SIM (FOR TESTING ONLY)
# =========================
def fake_market_data(symbol="DOGEUSDT"):
    return {
        "symbol": symbol,
        "price_change": random.uniform(-3, 3),
        "volume": random.uniform(10, 100)
    }


# =========================
# TIME HELPERS
# =========================
def current_timestamp():
    return int(time.time())


def sleep_seconds(sec):
    time.sleep(sec)
