
# fse/utils/validators.py
import re
import logging

logger = logging.getLogger("FSE.Validators")

# =========================
# VALIDATORS (CORE INTEGRITY)
# =========================

def validate_symbol(symbol: str) -> bool:
    """መርህ #1 እና #3፦ የሲምቦል ቅርጸት ማረጋገጥ።"""
    if not isinstance(symbol, str):
        logger.error("Validation Error: Symbol must be a string.")
        return False
    # BTCUSDT, ETHUSDT ወዘተ እንዲያልፉ የተስተካከለ RegEx
    if not re.match(r"^[A-Z0-9]{5,15}$", symbol):
        logger.error(f"Validation Error: Invalid symbol format: {symbol}")
        return False
    return True

def validate_side(side: str) -> bool:
    """የንግድ አቅጣጫ ማረጋገጥ።"""
    if side not in ["LONG", "SHORT", "HEDGE"]:
        logger.error(f"Validation Error: Invalid side '{side}'.")
        return False
    return True

def validate_quantity(qty: float) -> bool:
    """መርህ #4 እና #9፦ የንግድ መጠን ደህንነት ማረጋገጥ።"""
    try:
        q = float(qty)
        if 0 < q <= 1_000_000:
            return True
        logger.error(f"Validation Error: Quantity {q} out of safe bounds.")
    except (ValueError, TypeError):
        logger.error("Validation Error: Quantity must be numeric.")
    return False

def validate_confidence(confidence: float) -> bool:
    """መርህ #4፦ የሲግናል አስተማማኝነት ማረጋገጥ።"""
    try:
        c = float(confidence)
        if 0 <= c <= 100:
            return True
        logger.error(f"Validation Error: Confidence {c} invalid.")
    except (ValueError, TypeError):
        logger.error("Validation Error: Confidence must be numeric.")
    return False

# =========================
# CENTRAL VALIDATION (MAIN)
# =========================
def validate_signal(signal: dict) -> bool:
    """
    መርህ #11 (Liquidity & Volume Guard):- 
    ሁሉም ሲግናሎች ወደ አፈጻጸም ከመላካቸው በፊት የሚጣሩበት ማዕከል ነው።
    """
    if not isinstance(signal, dict):
        return False
    
    # የ필ዱ መስፈርቶች (Required Fields)
    required = ["symbol", "side", "qty", "confidence"]
    if not all(k in signal for k in required):
        logger.error("Validation Error: Missing required signal fields.")
        return False
    
    # ሁሉንም ማጣሪያዎች ማለፍ አለባቸው
    is_valid = (
        validate_symbol(signal["symbol"]) and
        validate_side(signal["side"]) and
        validate_quantity(signal["qty"]) and
        validate_confidence(signal["confidence"])
    )
    
    if is_valid:
        logger.info(f"Signal validated for {signal['symbol']} [{signal['side']}]")
    return is_valid
