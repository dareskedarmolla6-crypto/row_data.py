# ==========================================================
# FSE GLOBAL SETTINGS
# ==========================================================

class Settings:

    # Market Scan Interval (seconds)
    INTERVAL = 180  # 3 minutes

    # Maximum simultaneous open positions
    MAX_OPEN_POSITIONS = 18

    # Minimum confidence required to allow a trade
    CONFIDENCE_THRESHOLD = 15

    # Trading mode
    MODE = "ALPHA_ONLY"

    # Focus only on high volatility coins
    MIN_VOLATILITY_PERCENT = 15

    # Supported trading styles
    ENABLE_LONG = True
    ENABLE_SHORT = True
    ENABLE_HEDGE = True
    ENABLE_GRID = True

    # Leverage limits
    MIN_LEVERAGE = 5
    MAX_LEVERAGE = 30

    # FSE confidence-based leverage map
    LEVERAGE_LEVELS = {
        (15, 25): 5,
        (26, 35): 8,
        (36, 55): 10,
        (56, 75): 15,
        (76, 85): 20,
        (86, 100): 30
    }
# Safety guard: ensure settings align with core constants (prevents mismatch bugs)
assert MIN_LEVERAGE == 5
assert MAX_LEVERAGE == 30
assert CONFIDENCE_THRESHOLD >= 15
