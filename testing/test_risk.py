
# fse/tests/test_risk.py
import unittest
from risk.risk_manager import RiskEngine, PositionSizer # ዋናዎቹን ክፍሎች ከሪስክ ሞጁል በመጠቀም

# =========================
# TEST SUITE
# =========================
class TestRiskEngine(unittest.TestCase):
    """የሪስክ ሞጁሉን ትክክለኛነት የሚያረጋግጡ የሙከራ ትዕዛዞች (መርህ #10)።"""

    def setUp(self):
        self.engine = RiskEngine(max_risk=0.02, max_exposure=0.3)
        self.sizer = PositionSizer(max_risk=0.02)

    def test_risk_limits(self):
        """ከፍተኛ የሪስክ መጠን ያላቸው ንግዶች መታገዳቸውን ማረጋገጥ።"""
        # balance: 1000, size: 50 (5% risk - should be blocked)
        approved, reason = self.engine.validate_new_position("LONG", 1000, 50, [])
        self.assertFalse(approved)
        self.assertEqual(reason, "RISK_TOO_HIGH")

    def test_safe_trade_approval(self):
        """ደህንነቱ የተጠበቀ ንግድ መፈቀዱን ማረጋገጥ።"""
        approved, reason = self.engine.validate_new_position("LONG", 1000, 10, [])
        self.assertTrue(approved)
        self.assertEqual(reason, "APPROVED")

    def test_position_sizing(self):
        """የንግድ መጠን ስሌት ትክክለኛነት ማረጋገጥ።"""
        size = self.sizer.calculate(1000, 80) # 1000 * 0.02 * 0.8
        self.assertEqual(size, 16.0)

    def test_invalid_signal(self):
        """የማይታወቁ ሲግናሎች መታገዳቸውን ማረጋገጥ።"""
        approved, reason = self.engine.validate_new_position("SELL_ALL", 1000, 10, [])
        self.assertFalse(approved)
        self.assertEqual(reason, "INVALID_SIGNAL")

if __name__ == "__main__":
    unittest.main()
