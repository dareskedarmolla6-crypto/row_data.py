import time
import psutil
import threading


# =========================
# SYSTEM HEALTH MONITOR
# =========================
class SystemHealthMonitor:
    def __init__(self, cpu_limit=80, memory_limit=80):
        self.cpu_limit = cpu_limit
        self.memory_limit = memory_limit

        self.errors = 0
        self.trades = 0
        self.start_time = time.time()

        self.latency_log = []
        self.running = False

    # -------------------------
    # METRICS UPDATE
    # -------------------------
    def record_trade(self):
        self.trades += 1

    def record_error(self):
        self.errors += 1

    def record_latency(self, latency_ms):
        self.latency_log.append(latency_ms)

        # keep last 100 only
        if len(self.latency_log) > 100:
            self.latency_log.pop(0)

    # -------------------------
    # SYSTEM STATUS CHECK
    # -------------------------
    def get_cpu_usage(self):
        return psutil.cpu_percent(interval=1)

    def get_memory_usage(self):
        return psutil.virtual_memory().percent

    def average_latency(self):
        if not self.latency_log:
            return 0
        return sum(self.latency_log) / len(self.latency_log)

    def uptime(self):
        return time.time() - self.start_time

    # -------------------------
    # HEALTH STATUS
    # -------------------------
    def system_status(self):
        cpu = self.get_cpu_usage()
        mem = self.get_memory_usage()
        avg_latency = self.average_latency()

        status = "HEALTHY"

        if cpu > self.cpu_limit:
            status = "CPU_HIGH"

        if mem > self.memory_limit:
            status = "MEMORY_HIGH"

        if self.errors > 10:
            status = "ERROR_OVERLOAD"

        if avg_latency > 1000:
            status = "HIGH_LATENCY"

        return {
            "status": status,
            "cpu": cpu,
            "memory": mem,
            "errors": self.errors,
            "trades": self.trades,
            "avg_latency_ms": round(avg_latency, 2),
            "uptime_sec": round(self.uptime(), 2)
        }

    # -------------------------
    # CONTINUOUS MONITOR LOOP
    # -------------------------
    def start_background_monitor(self, interval=5):
        self.running = True

        def loop():
            while self.running:
                status = self.system_status()
                print("📊 SYSTEM HEALTH:", status)
                time.sleep(interval)

        thread = threading.Thread(target=loop, daemon=True)
        thread.start()

    def stop(self):
        self.running = False
