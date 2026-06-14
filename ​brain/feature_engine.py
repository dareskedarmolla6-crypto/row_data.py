
"""
FSE CORE - Feature Intelligence Engine

Purpose:
    Converts raw market information into intelligent
    trading features for the AI brain.
"""

from typing import Dict, Optional


# ==========================================================
# POSITION INTELLIGENCE
# ==========================================================

class PositionIntelligence:
    """
    Controls position sizing based on confidence,
    volatility, and portfolio exposure.
    """

    def __init__(
        self,
        base_risk: float = 0.01,
        max_exposure: float = 0.20
    ):
        self.base_risk = base_risk
        self.max_exposure = max_exposure
        self.current_exposure = 0.0


    def calculate_size(
        self,
        signal: Dict,
        wallet_balance: float
    ) -> float:

        confidence = signal.get(
            "confidence",
            0.5
        )

        volatility = signal.get(
            "volatility",
            0
        )


        # FSE prefers high volatility opportunities
        volatility_bonus = min(
            volatility / 30,
            1.0
        )

        risk_factor = (
            confidence * 0.6
            +
            volatility_bonus * 0.4
        )


        size = (
            wallet_balance
            * self.base_risk
            * (1 + risk_factor)
        )


        available = (
            wallet_balance
            * self.max_exposure
            -
            self.current_exposure
        )


        return round(
            max(0, min(size, available)),
            2
        )


    def update_exposure(
        self,
        amount: float
    ):
        self.current_exposure += amount


    def reduce_exposure(
        self,
        amount: float
    ):
        self.current_exposure = max(
            0,
            self.current_exposure - amount
        )


# ==========================================================
# WHALE INTELLIGENCE
# ==========================================================

class WhaleSignalEngine:
    """
    Detects large player activity.
    """

    def generate(
        self,
        whale_state: str,
        strength: float = 1.0
    ) -> Optional[Dict]:

        states = {
            "ACCUMULATION": "LONG",
            "DISTRIBUTION": "SHORT",
        }


        side = states.get(whale_state)


        if not side:
            return None


        return {
            "signal": side,
            "confidence": min(
                1.0,
                0.7 + strength * 0.3
            )
        }


# ==========================================================
# VOLUME SPIKE DETECTOR
# ==========================================================

class VolumeSpikeHunter:
    """
    Detects unusual volume explosions.
    """

    def detect(
        self,
        current_volume: float,
        average_volume: float
    ) -> bool:


        if average_volume <= 0:
            return False


        ratio = (
            current_volume /
            average_volume
        )


        return ratio >= 3.0


# ==========================================================
# VOLUME INTELLIGENCE SCORE
# ==========================================================

class VolumeScoreEngine:
    """
    Converts volume strength into
    an AI score from 0 to 100.
    """

    def score(
        self,
        current_volume: float,
        average_volume: float
    ) -> float:


        if average_volume <= 0:
            return 0.0


        ratio = (
            current_volume /
            average_volume
        )


        return min(
            100,
            ratio * 20
        )


# ==========================================================
# ALPHA FEATURE ENGINE
# ==========================================================

class AlphaFeatureEngine:
    """
    Builds a complete AI feature packet.
    """

    def build(
        self,
        market: Dict
    ) -> Dict:


        volume_score = VolumeScoreEngine().score(
            market.get("volume", 0),
            market.get("average_volume", 1)
        )


        volatility = market.get(
            "volatility",
            0
        )


        return {

            "volatility": volatility,

            "volume_score": volume_score,

            "high_volatility": (
                volatility >= 15
            ),

            "alpha_quality": (
                volatility * 0.7
                +
                volume_score * 0.3
            )
        }


# ==========================================================
# FSE FEATURE ENGINE END
# ==========================================================
