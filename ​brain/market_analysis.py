
# fse/brain/market_analysis.py
import logging

logger = logging.getLogger("FSE.Brain.MarketAnalysis")

# ==========================================================
# MARKET ANALYSIS ENGINE (CORE)
# ==========================================================

class MarketAnalysisEngine:
    """መርህ #3: የገበያ ሁኔታን (Market Regime) የሚለይ ዋና ሞተር።"""

    def evaluate(self, market: dict) -> dict:
        """የገበያ መረጃን ወደ ስልታዊ ትንተና መቀየሪያ።"""
        try:
            return {
                "trend": self._trend(market),
                "volatility": self._volatility(market),
                "liquidity": self._liquidity(market),
                "structure": self._structure_bias(market)
            }
        except Exception as e:
            logger.error(f"Market Analysis Error: {e}")
            return {"trend": "SIDEWAYS", "volatility": 0, "liquidity": "LOW", "structure": "BEARISH"}

    def _trend(self, market: dict) -> str:
        price_now = market.get("price_now", 0)
        price_avg = market.get("price_avg", 1)
        if price_now > price_avg * 1.002: return "UP"
        if price_now < price_avg * 0.998: return "DOWN"
        return "SIDEWAYS"

    def _volatility(self, market: dict) -> float:
        """መርህ #4: የገበያ መወዛወዝ መጠን (Percentage-based)።"""
        high = market.get("high", 0)
        low = market.get("low", 0)
        price = market.get("price_now", 1)
        return abs(high - low) / price * 100 if price != 0 else 0.0

    def _liquidity(self, market: dict) -> str:
        """መርህ #11: የቮሊዩም ፍሰትን በመለካት የሊኩዊዲቲ ሁኔታ ማረጋገጫ።"""
        volume = market.get("volume", 0)
        if volume > 100000: return "HIGH"
        if volume > 50000: return "MEDIUM"
        return "LOW"

    def _structure_bias(self, market: dict) -> str:
        """የገበያ መዋቅር አድልዎ (Structure Bias)።"""
        return "BULLISH" if market.get("price_now", 0) > market.get("price_prev", 0) else "BEARISH"
