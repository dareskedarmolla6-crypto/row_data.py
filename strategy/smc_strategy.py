
class Strategy:
    def build(self, signal, confidence):
        if confidence < 60:
            return "FULL_HEDGE"
        if signal == "LONG":
            return "LONG_ONLY"
        if signal == "SHORT":
            return "SHORT_ONLY"
        return "FULL_HEDGE"
