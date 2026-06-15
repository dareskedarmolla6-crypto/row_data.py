
# fse/utils/math_utils.py
import math

# =========================
# MATHEMATICAL UTILITIES
# =========================

def clamp(value: float, min_val: float, max_val: float) -> float:
    """መርህ #4፦ የዋጋዎችን ክልል መቆጣጠሪያ።"""
    return max(min_val, min(value, max_val))

def safe_div(a: float, b: float, default: float = 0.0) -> float:
    """በዜሮ የመካፈል ስህተትን መከላከያ።"""
    return a / b if b != 0 else default

def pct_change(old: float, new: float) -> float:
    """የፐርሰንት ለውጥ መለኪያ።"""
    return ((new - old) / old * 100) if old != 0 else 0.0

# =========================
# TRADING DYNAMICS (CORE LOGIC)
# =========================

def position_size(balance: float, risk_pct: float, confidence: float) -> float:
    """መርህ #7 (Dynamic Capital Allocation): ካፒታልን እንደ ኮንፊደንስ ማከፋፈል።"""
    confidence_factor = clamp(confidence / 100, 0.1, 1.5)
    base = balance * (risk_pct / 100)
    return base * confidence_factor

def leverage_by_confidence(confidence: float) -> int:
    """መርህ #8 (Adaptive Leverage): ኮንፊደንስን መሰረት ያደረገ የሊቨሬጅ መጠን።"""
    if confidence < 15: return 0
    if confidence <= 25: return 5
    if confidence <= 35: return 8
    if confidence <= 55: return 10
    if confidence <= 75: return 15
    if confidence <= 85: return 20
    return 30

def volatility_score(prices: list) -> float:
    """መርህ #4: የገበያ መረጋጋት ወይም መወዛወዝ መለኪያ።"""
    if len(prices) < 2: return 0.0
    changes = [abs(prices[i] - prices[i - 1]) for i in range(1, len(prices))]
    return sum(changes) / len(changes)

def risk_score(confidence: float, volatility: float) -> float:
    """መርህ #4: የጋራ የሪስክ ነጥብ አሰጣጥ።"""
    return clamp(confidence - (volatility * 10), 0, 100)
