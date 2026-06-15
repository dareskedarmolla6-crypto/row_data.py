
# fse/brain/confidence.py
import logging

logger = logging.getLogger("FSE.Brain.Confidence")

# ==========================================================
# FSE CONFIDENCE ENGINE (CORE)
# ==========================================================

class ConfidenceEngine:
    """መርህ #4: የሲግናል አስተማማኝነትን በሳይንሳዊ መንገድ መለኪያ።"""

    def evaluate(self, analysis: dict, ml_score: float = 0.5, history_score: float = 0.5) -> float:
        """መርህ #4 እና #11: የገበያ መረጃን መሰረት አድርጎ የኮንፊደንስ ነጥብ ማስያ።"""
        try:
            volatility = analysis.get("volatility", 0)
            liquidity = analysis.get("liquidity", "LOW")
            structure = analysis.get("structure", "BEARISH")

            score = 0.5  # መሰረታዊ አስተማማኝነት (Base)

            # የቮላቲሊቲ ተፅእኖ (መርህ #4)
            if volatility < 10: score -= 0.2
            elif volatility > 15: score += 0.2

            # የሊኩዊዲቲ ተፅእኖ (መርህ #11)
            if liquidity == "HIGH": score += 0.2
            elif liquidity == "LOW": score -= 0.2

            # የመዋቅር ትንተና
            score += 0.1 if structure == "BULLISH" else 0.05

            # የ ML እና የታሪክ ድብልቅ (መርህ #1)
            score += (ml_score * 0.2) + (history_score * 0.2)

            # የቁጥር መቆጣጠሪያ (Clamp 0-1)
            return round(max(0.0, min(1.0, score)), 3)
            
        except Exception as e:
            logger.error(f"Confidence Evaluation Error: {e}")
            return 0.0
