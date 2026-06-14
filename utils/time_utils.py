import time
from datetime import datetime, timezone


# =========================
# TIME HELPERS
# =========================

def now_unix() -> int:
    """Current time in unix seconds"""
    return int(time.time())


def now_ms() -> int:
    """Current time in milliseconds"""
    return int(time.time() * 1000)


def utc_now() -> datetime:
    """UTC datetime object"""
    return datetime.now(timezone.utc)


def format_utc() -> str:
    """Readable UTC timestamp"""
    return utc_now().strftime("%Y-%m-%d %H:%M:%S UTC")


# =========================
# SCHEDULING HELPERS
# =========================

def sleep_seconds(seconds: float):
    """Safe sleep wrapper (can be replaced with async later)"""
    time.sleep(seconds)


def next_interval(interval_sec: int, offset: int = 0) -> float:
    """
    Calculate next aligned execution time
    Example: bot scan every 3 seconds aligned
    """
    return ((time.time() // interval_sec) + 1) * interval_sec + offset


def wait_until(target_time: float):
    """Sleep until a target unix time"""
    delay = target_time - time.time()
    if delay > 0:
        time.sleep(delay)


# =========================
# COOLDOWN / RATE CONTROL
# =========================

class Cooldown:
    def __init__(self):
        self.last_call = {}

    def allow(self, key: str, cooldown_sec: int) -> bool:
        now = time.time()
        last = self.last_call.get(key, 0)

        if now - last >= cooldown_sec:
            self.last_call[key] = now
            return True

        return False


# =========================
# TIME WINDOW UTILS
# =========================

def in_time_window(start_hour: int, end_hour: int) -> bool:
    """
    Check if current UTC hour is inside trading window
    """
    hour = utc_now().hour
    return start_hour <= hour <= end_hour
