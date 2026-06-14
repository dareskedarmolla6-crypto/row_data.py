import unittest
import random

# =========================
# MOCK EXECUTION (same logic as main system)
# =========================
class Execution:
    def __init__(self):
        self.trades = []

    def open_long(self, symbol, size):
        trade = {
            "symbol": symbol,
            "side": "LONG",
            "size": size
        }
        self.trades.append(trade)
        return trade

    def open_short(self, symbol, size):
        trade = {
            "symbol": symbol,
            "side": "SHORT",
            "size": size
        }
        self.trades.append(trade)
        return trade


# =========================
# SIMPLE RISK MOCK
# =========================
class RiskAI:
    def approve_trade(self, signal, confidence):
        return confidence >= 50, "OK"

    def position_size(self, balance, confidence):
        return balance * (confidence / 1000)


# =========================
# SIMPLE BRAIN MOCK
# =========================
class Brain:
    def predict(self, data):
        if data["price_change"] > 0:
            return "LONG", 70
        return "SHORT", 60


# =========================
# TEST CASES
# =========================
class TestExecution(unittest.TestCase):

    def setUp(self):
        self.execution = Execution()
        self.risk = RiskAI()
        self.brain = Brain()
        self.balance = 1000

    def test_open_long(self):
        trade = self.execution.open_long("DOGEUSDT", 10)

        self.assertEqual(trade["side"], "LONG")
        self.assertEqual(trade["symbol"], "DOGEUSDT")
        self.assertEqual(trade["size"], 10)

    def test_open_short(self):
        trade = self.execution.open_short("DOGEUSDT", 5)

        self.assertEqual(trade["side"], "SHORT")
        self.assertEqual(trade["size"], 5)

    def test_trade_flow_long(self):
        data = {"price_change": 2.5}

        signal, confidence = self.brain.predict(data)
        approved, _ = self.risk.approve_trade(signal, confidence)

        size = self.risk.position_size(self.balance, confidence)

        if approved and signal == "LONG":
            trade = self.execution.open_long("DOGEUSDT", size)

            self.assertEqual(trade["side"], "LONG")
            self.assertTrue(trade["size"] > 0)
