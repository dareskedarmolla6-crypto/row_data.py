import unittest


# =========================
# STRATEGY MODULE (mock for test)
# =========================
class Strategy:
    def build(self, signal, confidence):
        if confidence < 60:
            return "FULL_HEDGE"
        elif signal == "LONG":
            return "LONG_ONLY"
        elif signal == "SHORT":
            return "SHORT_ONLY"
        return "NO_TRADE"


# =========================
# TEST SUITE
# =========================
class TestStrategy(unittest.TestCase):

    def setUp(self):
        self.strategy = Strategy()

    # -------------------------
    # LOW CONFIDENCE => HEDGE
    # -------------------------
    def test_low_confidence_returns_hedge(self):
        result = self.strategy.build("LONG", 40)
        self.assertEqual(result, "FULL_HEDGE")

    # -------------------------
    # LONG SIGNAL
    # -------------------------
    def test_long_signal(self):
        result = self.strategy.build("LONG", 80)
        self.assertEqual(result, "LONG_ONLY")

    # -------------------------
    # SHORT SIGNAL
    # -------------------------
    def test_short_signal(self):
        result = self.strategy.build("SHORT", 85)
        self.assertEqual(result, "SHORT_ONLY")

    # -------------------------
    # UNKNOWN SIGNAL
    # -------------------------
    def test_unknown_signal(self):
        result = self.strategy.build("HOLD", 90)
        self.assertEqual(result, "NO_TRADE")


# =========================
# RUN TESTS
# =========================
if __name__ == "__main__":
    unittest.main()
