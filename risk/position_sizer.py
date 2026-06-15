
# fse/risk/position_sizer.py
import logging

logger = logging.getLogger(__name__)

# =========================
# POSITION SIZER
# =========================
class PositionSizer:
    """በካፒታል እና በሪስክ ደረጃ የንግድ መጠንን የሚወስን (መርህ #7)።"""

    def calculate_size(self, balance: float, risk_percentage: float, leverage: int = 1, confidence: float = 1.0):
        """
        ንግድ ከመከፈቱ በፊት የቦታ መጠንን (Position Size) በከፍተኛ ጥንቃቄ ማስላት።
        """
        try:
            # የግብዓት መረጃዎችን ደህንነት ማረጋገጥ
            bal = float(balance)
            risk = max(0.0, min(float(risk_percentage), 1.0))
            lev = max(1, int(leverage))
            conf = max(0.0, min(float(confidence), 1.0))

            # ስሌት: (ካፒታል * የሪስክ መቶኛ * የሲግናል ጥራት) * ሌቨሬጅ
            base_risk = bal * risk
            adjusted_risk = base_risk * conf
            position_size = adjusted_risk * lev

            logger.info(f"📏 Position Sized: {position_size} (Balance: {bal}, Risk: {risk}, Conf: {conf})")
            return round(position_size, 4)
            
        except Exception as e:
            logger.error(f"❌ Position sizing error: {e}")
            return 0.0
