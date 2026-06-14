import json
import time


# =========================
# TELEMETRY STREAM (EVENT BUFFER)
# =========================
class TelemetryStream:
    def __init__(self, max_size=100):
        self.buffer = []
        self.max_size = max_size

    def push(self, event_type, data):
        event = {
            "time": time.time(),
            "type": event_type,
            "data": data
        }

        self.buffer.append(event)

        # keep buffer size safe
        if len(self.buffer) > self.max_size:
            self.buffer = self.buffer[-self.max_size:]

    def flush(self):
        payload = json.dumps(self.buffer)
        self.buffer.clear()

        print("[TELEMETRY FLUSH]", payload)
        return payload


# =========================
# TELEMETRY HOOK (EVENT CONNECTOR)
# =========================
class TelemetryHook:
    def __init__(self, stream: TelemetryStream):
        self.stream = stream

    def on_trade(self, pnl, balance):
        self.stream.push("TRADE", {
            "pnl": pnl,
            "balance": balance
        })

    def on_signal(self, signal):
        self.stream.push("SIGNAL", signal)

    def on_error(self, error):
        self.stream.push("ERROR", {
            "message": str(error)
        })


# =========================
# METRICS STORE (STATE TRACKER)
# =========================
class MetricsStore:
    def __init__(self):
        self.balance = 1000
        self.trades = []

    def log_trade(self, signal, pnl):
        self.trades.append({
            "signal": signal,
            "pnl": pnl,
            "timestamp": time.time()
        })
        self.balance += pnl


# =========================
# SYSTEM MONITOR (HEALTH CHECK)
# =========================
class MetricsCollection:
    def collect(self, data):
        status = data.get("status", "UNKNOWN")
        print(f"🟢 SYSTEM HEALTH: {status}")
