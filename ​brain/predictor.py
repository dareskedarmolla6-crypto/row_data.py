"""
FSE Prediction Engine
Alpha Coin Market Predictor
"""


class Predictor:
    def __init__(self):
        self.min_confidence = 40
        self.target_volatility = 15

    def analyze_market(self, coin, volatility, confidence):
        result = {
            "coin": coin,
            "volatility": volatility,
            "confidence": confidence,
            "trade_allowed": False
        }

        if confidence >= self.min_confidence:
            result["trade_allowed"] = True

        return result

    def is_alpha_coin(self, volatility):
        return volatility >= self.target_volatility
