# portfolio/pnl_calculator.py


class TradeMemory:
    def __init__(self):
        self.history = []
        self.pattern_success = {}

    def record_trade(self, signal, pnl, regime):
        key = f"{signal['side']}_{regime}"

        self.history.append({
            "symbol": signal["symbol"],
            "side": signal["side"],
            "pnl": pnl,
            "regime": regime,
            "key": key
        })

        if key not in self.pattern_success:
            self.pattern_success[key] = {"wins": 0, "losses": 0}

        if pnl > 0:
            self.pattern_success[key]["wins"] += 1
        else:
            self.pattern_success[key]["losses"] += 1


class MemorySignalBooster:
    def __init__(self, memory: TradeMemory):
        self.memory = memory

    def enhance(self, signal):
        key = f"{signal['side']}_{signal.get('regime', 'UNKNOWN')}"

        stats = self.memory.pattern_success.get(key)

        # fallback safety (avoid divide-by-zero)
        if not stats:
            score = 0.5
        else:
            total = stats["wins"] + stats["losses"]
            score = stats["wins"] / total if total > 0 else 0.5

        signal["memory_score"] = round(score, 3)

        # safe score initialization
        if "score" not in signal:
            signal["score"] = 0

        signal["score"] += int(score * 10)

        return signal
