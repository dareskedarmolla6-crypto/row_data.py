# fse/strategy/alpha_strategy.py
import random
import logging

logger = logging.getLogger(__name__)

# =========================
# ALPHA SCORING & DISCOVERY
# =========================
class AlphaScorer:
    """የገበያ መረጃን ወደ Alpha Score የሚቀይር።"""
    def score(self, data):
        return (
            data.get("volatility", 0.0) * 50.0 +
            data.get("momentum", 0.0) * 20.0 +
            data.get("volume", 0.0) * 0.0001
        )

class AlphaCoinDiscoveryEngine:
    """ከፍተኛ የAlpha Score ያላቸውን ንብረቶች የሚቃኝ።"""
    def __init__(self, feed, scorer, min_score=60.0):
        self.feed = feed
        self.scorer = scorer
        self.min_score = min_score

    def scan(self):
        snapshot = self.feed.get_all()
        results = []
        for symbol, data in snapshot.items():
            score = self.scorer.score(data)
            if score >= self.min_score:
                results.append({"symbol": symbol, "score": score, **data})
        return sorted(results, key=lambda x: x["score"], reverse=True)

# =========================
# SMART MONEY & VOLUME ANALYSIS
# =========================
class SmartMoneyDetector:
    """የWhale ግብይቶችን በመተንተን አቅጣጫን የሚለይ።"""
    def analyze(self, whales):
        buy_val = sum(w["value"] for w in whales if w["side"] == "BUY")
        sell_val = sum(w["value"] for w in whales if w["side"] == "SELL")
        
        if buy_val > sell_val: return "ACCUMULATION"
        if sell_val > buy_val: return "DISTRIBUTION"
        return "NEUTRAL"

class VolumeSpikeDetector:
    """ድንገተኛ የገበያ እንቅስቃሴን (Volume Spike) የሚለይ።"""
    def detect(self, current, average):
        return (current / average) >= 3.0 if average > 0 else False

# =========================
# MASTER ALPHA HUNTER
# =========================
class MasterAlphaHunter:
    """የ Alpha ስልትን የሚያስተባብር ዋና ክፍል (መርህ #1)።"""
    def __init__(self, feed):
        self.discovery = AlphaCoinDiscoveryEngine(feed, AlphaScorer())
        self.detector = SmartMoneyDetector()
        logger.info("🎯 Alpha Hunter initialized.")

    def execute(self, market_data):
        """ስልቱን የሚያስፈጽም ዋና ተግባር።"""
        candidates = self.discovery.scan()
        if not candidates:
            return {"strategy": "ALPHA", "action": "HOLD"}
        
        # ከፍተኛ ውጤት ያለው ሳንቲም ላይ ማተኮር
        top_coin = candidates[0]
        action = "LONG" if top_coin["momentum"] > 0 else "SHORT"
        
        logger.info(f"🔍 Alpha Found: {top_coin['symbol']} | Score: {top_coin['score']}")
        return {
            "strategy": "ALPHA",
            "action": action,
            "symbol": top_coin["symbol"],
            "confidence": min(top_coin["score"], 100)
        }
