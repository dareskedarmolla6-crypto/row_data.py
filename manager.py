# =========================
# RISK MANAGER (STANDALONE MODULE)
# =========================


class RiskAI:
    """
    Core decision + position sizing engine
    """

    def approve_trade(self, signal, confidence, leverage=3):
        if confidence < 55:
            return False, "LOW CONFIDENCE"

        if leverage > 20:
            return False, "LEVERAGE TOO HIGH"

        return True, "APPROVED"

    def position_size(self, balance, confidence):
        base_risk = 0.02
        multiplier = confidence / 100

        size = balance * base_risk * multiplier

        if size < 1:
            size = 1

        return round(size, 4)


# =========================
# PORTFOLIO CONTROL (OPTIONAL MODULE)
# =========================
class PortfolioManager:
    """
    Tracks exposure across trades
    """

    def __init__(self, max_exposure=0.3):
        self.max_exposure = max_exposure
        self.current_exposure = 0

    def can_allocate(self, size, balance):
        projected = (self.current_exposure + size) / balance
        return projected <= self.max_exposure

    def allocate(self, size):
        self.current_exposure += size
        return self.current_exposure

    def reset(self):
        self.current_exposure = 0


# =========================
# SAFETY / EMERGENCY STOP
# =========================
class SafetyEngine:
    """
    Stops trading under dangerous conditions
    """

    def __init__(self, max_drawdown=0.1):
        self.max_drawdown = max_drawdown

    def emergency_stop(self, drawdown):
        return drawdown >= self.max_drawdown


# =========================
# MAIN WRAPPER (USED BY MAIN.PY)
# =========================
class RiskEngine:
    """
    This is the ONLY class imported in main.py
    It wraps all risk logic cleanly
    """

    def __init__(self):
        self.ai = RiskAI()
        self.portfolio = PortfolioManager()
        self.safety = SafetyEngine()

    def approve_trade(self, signal, confidence, leverage=3):
        return self.ai.approve_trade(signal, confidence, leverage)

    def position_size(self, balance, confidence):
        return self.ai.position_size(balance, confidence)

    def validate_new_position(self, signal):
        if not signal:
            return False

        if "symbol" not in signal or "side" not in signal:
            return False

        return True
