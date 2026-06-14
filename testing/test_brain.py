import unittest


# =========================
# Import Brain from main/core
# (adjust path depending on your structure)
# =========================
class Brain:
    def predict(self, data):
        change = data["price_change"]

        if change > 1:
            return "LONG", 75
        elif change < -1:
            return "SHORT", 72
        else:
            return "HEDGE", 60


# =========================
# TEST CASES
# =========================
class TestBrain(unittest.TestCase):

    def setUp(self):
        self.brain = Brain()

    def test_long_signal(self):
        data = {"price_change": 2.5}
        signal, conf = self.brain.predict(data)

        self.assertEqual(signal, "LONG")
        self.assertGreaterEqual(conf, 70)

    def test_short_signal(self):
        data = {"price_change": -2.2}
        signal, conf = self.brain.predict(data)

        self.assertEqual(signal, "SHORT")
        self.assertGreaterEqual(conf, 70)

    def test_hedge_signal(self):
        data = {"price_change": 0.2}
        signal, conf = self.brain.predict(data)

        self.assertEqual(signal, "HEDGE")
        self.assertEqual(conf, 60)


# =========================
# RUN TESTS
# =========================
if __name__ == "__main__":
    unittest.main()
