import time


# =========================
# DRAWDOWN TRACKER
# =========================
class DrawdownControl:
    def __init__(self):
        self.peak_balance = 0

    def update_peak(self, balance):
        if balance > self.peak_balance:
            self.peak_balance = balance

    def get_drawdown(self, balance):
        if self.peak_balance == 0:
            return 0
        return (self.peak_balance - balance) / self.peak_balance


# =========================
# MAX DRAWDOWN GUARD
# =========================
class MaxDrawdownControl:
    def __init__(self, max_drawdown=0.20):
        self.max_drawdown = max_drawdown
        self.tracker = DrawdownControl()

    def allow_trade(self, balance):
        self.tracker.update_peak(balance)
        dd = self.tracker.get_drawdown(balance)

        if dd >= self.max_drawdown:
            return False, dd

        return True, dd


# =========================
# KILL SWITCH (GLOBAL SAFETY)
# =========================
class KillSwitch:
    def __init__(self, hard_limit=0.25):
        self.hard_limit = hard_limit

    def check(self, drawdown):
        if drawdown >= self.hard_limit:
            return True
        return False


# =========================
# AUTONOMY SAFETY CORE (OPTIONAL WRAPPER)
# =========================
class FullAutonomyCore:
    def __init__(self, execution_engine, kill_switch: KillSwitch):
        self.execution = execution_engine
        self.kill = kill_switch

    def run(self, decision, drawdown):
        if self.kill.check(drawdown):
            return "SYSTEM_HALTED"

        return self.execution.execute_trade(decision)
