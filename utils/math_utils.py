import math


# =========================
# BASIC MATH HELPERS
# =========================
def clamp(value, min_value, max_value):
    """Limits a value between min and max"""
    return max(min_value, min(value, max_value))


def safe_div(a, b, default=0.0):
    """Safe division to avoid ZeroDivisionError"""
    return a / b if b != 0 else default


# =========================
# PERCENTAGE UTILITIES
# =========================
def pct_change(old, new):
    """Percentage change between two values"""
    if old == 0:
        return 0.0
    return ((new - old) / old) * 100


def normalize(value, min_value, max_value):
    """Normalize value between 0 and 1"""
    if max_value == min_value:
        return 0.0
    return (value - min_value) / (max_value - min_value)


# =========================
# RISK / POSITION SIZING HELPERS
# =========================
def position_size(balance, risk_pct, confidence):
    """
    Dynamic position sizing:
    - risk_pct: percent of balance to risk
    - confidence: 0–100
    """
    confidence_factor = clamp(confidence / 100, 0.1, 1.5)
    base = balance * (risk_pct / 100)

    return base * confidence_factor


def leverage_by_confidence(confidence):
    """
    Confidence-based leverage mapping (safe version)
    """
    if confidence < 15:
        return 0

    if confidence <= 25:
        return 5
    elif confidence <= 35:
        return 8
    elif confidence <= 55:
        return 10
    elif confidence <= 75:
        return 15
    elif confidence <= 85:
        return 20
    else:
        return 30


# =========================
# VOLATILITY HELPERS
# =========================
def volatility_score(prices):
    """
    Simple volatility estimator using price movement
    """
    if len(prices) < 2:
        return 0.0

    changes = []
    for i in range(1, len(prices)):
        changes.append(abs(prices[i] - prices[i - 1]))

    return sum(changes) / len(changes)


def is_high_volatility(score, threshold=1.5):
    return score >= threshold


# =========================
# TREND HELPERS
# =========================
def simple_trend(prices):
    """
    Returns:
    - "UP"
    - "DOWN"
    - "SIDEWAYS"
    """
    if len(prices) < 3:
        return "SIDEWAYS"

    start = prices[0]
    end = prices[-1]

    change = pct_change(start, end)

    if change > 1:
        return "UP"
    elif change < -1:
        return "DOWN"
    return "SIDEWAYS"


# =========================
# RISK SCORE COMPOSER
# =========================
def risk_score(confidence, volatility):
    """
    Combines confidence and volatility into a single score
    """
    return clamp(confidence - (volatility * 10), 0, 100)
