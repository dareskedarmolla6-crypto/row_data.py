"""
FSE CORE - AI Inference Engine

Purpose:
    Central intelligence system for FSE Hedge + Grid Alpha Trading Bot.

Philosophy:
    FSE does not predict price direction only.
    The primary objective is finding high volatility
    alpha opportunities and exploiting both market directions
    using Hedge and Grid systems.
"""

from __future__ import annotations

import time
import math
import logging
from typing import (
    Dict,
    List,
    Optional,
    Any,
)
from dataclasses import dataclass, field


# ==========================================================
# LOGGER
# ==========================================================

logger = logging.getLogger("FSE.InferenceEngine")


# ==========================================================
# DATA MODELS
# ==========================================================

@dataclass
class MarketSnapshot:
    """
    Standard market information packet.
    """

    symbol: str

    price_now: float
    price_previous: float

    high: float
    low: float

    volume: float
    liquidity: float

    timestamp: float = field(default_factory=time.time)


@dataclass
class TradeRecord:
    """
    Historical trade information used
    for AI learning.
    """

    symbol: str
    strategy: str

    profit: float

    win: bool

    volatility: float

    timestamp: float = field(default_factory=time.time)


@dataclass
class AlphaCoinScore:
    """
    Ranking result for alpha opportunities.
    """

    symbol: str

    volatility_score: float

    liquidity_score: float

    final_score: float


# ==========================================================
# MEMORY SYSTEM
# ==========================================================

class MemoryEngine:
    """
    Stores historical trade data
    for self-learning modules.
    """

    def __init__(self, max_records: int = 10000):

        self.max_records = max_records

        self.records: List[TradeRecord] = []


    def store(self, trade: TradeRecord) -> None:

        self.records.append(trade)

        if len(self.records) > self.max_records:
            self.records.pop(0)


    def get_recent(
        self,
        limit: int = 200
    ) -> List[TradeRecord]:

        return self.records[-limit:]


    def win_rate(self) -> float:

        if not self.records:
            return 0.0

        wins = sum(
            1 for trade in self.records
            if trade.win
        )

        return wins / len(self.records)


# ==========================================================
# VOLATILITY INTELLIGENCE
# ==========================================================

class VolatilityEngine:
    """
    FSE main market filter.

    FSE risk is not direction.
    The biggest risk is low volatility.
    """

    # FSE preferred volatility level
    TARGET_VOLATILITY = 15.0

    # Exit zone
    MIN_VOLATILITY = 10.0


    def calculate(
        self,
        market: MarketSnapshot
    ) -> float:
        """
        Returns volatility percentage.
        """

        if market.price_now <= 0:
            return 0

        volatility = (
            (market.high - market.low)
            /
            market.price_now
        ) * 100

        return volatility


    def is_tradeable(
        self,
        market: MarketSnapshot
    ) -> bool:
        """
        True if coin has enough movement.
        """

        volatility = self.calculate(market)

        return volatility >= self.TARGET_VOLATILITY


    def should_exit(
        self,
        market: MarketSnapshot
    ) -> bool:
        """
        Exit low volatility markets.
        """

        volatility = self.calculate(market)

        return volatility <= self.MIN_VOLATILITY


# ==========================================================
# ALPHA COIN INTELLIGENCE
# ==========================================================

class AlphaCoinScanner:
    """
    Finds the strongest alpha opportunities.
    """

    def __init__(
        self,
        minimum_liquidity: float = 100_000
    ):

        self.minimum_liquidity = minimum_liquidity

        self.volatility_engine = VolatilityEngine()


    def scan(
        self,
        markets: List[MarketSnapshot]
    ) -> List[AlphaCoinScore]:

        results = []

        for market in markets:

            volatility = (
                self.volatility_engine
                .calculate(market)
            )

            if volatility < 15:
                continue

            if market.liquidity < self.minimum_liquidity:
                continue


            volatility_score = min(
                volatility / 30,
                1.0
            )

            liquidity_score = min(
                market.liquidity / 1_000_000,
                1.0
            )


            final_score = (
                volatility_score * 0.70
                +
                liquidity_score * 0.30
            )


            results.append(
                AlphaCoinScore(
                    symbol=market.symbol,
                    volatility_score=volatility_score,
                    liquidity_score=liquidity_score,
                    final_score=final_score,
                )
            )


        results.sort(
            key=lambda coin: coin.final_score,
            reverse=True
        )

        return results


# ==========================================================
# PART 1 END
# ==========================================================
# ==========================================================
# FEATURE EXTRACTION ENGINE
# ==========================================================

class FeatureBuilder:
    """
    Converts raw market information into AI-friendly features.
    """

    def build(
        self,
        market: MarketSnapshot
    ) -> Dict[str, float]:

        volatility = VolatilityEngine().calculate(market)

        momentum = 0.0
        if market.price_previous > 0:
            momentum = (
                (market.price_now - market.price_previous)
                / market.price_previous
            )

        return {
            "volatility": volatility,
            "momentum": momentum,
            "volume": market.volume,
            "liquidity": market.liquidity,
        }


# ==========================================================
# BASIC CANDLE MODEL
# ==========================================================

@dataclass
class Candle:
    """
    Standard candle structure.
    """

    open: float
    high: float
    low: float
    close: float
    volume: float


# ==========================================================
# MARKET STRUCTURE INTELLIGENCE
# ==========================================================

class StructureEngine:
    """
    Detects market structure changes.
    """

    def detect_bos(
        self,
        candles: List[Candle]
    ) -> Optional[str]:

        if len(candles) < 3:
            return None

        previous_high = max(
            candle.high for candle in candles[:-1]
        )

        previous_low = min(
            candle.low for candle in candles[:-1]
        )

        current = candles[-1]

        if current.close > previous_high:
            return "BOS_UP"

        if current.close < previous_low:
            return "BOS_DOWN"

        return None


    def detect_choch(
        self,
        candles: List[Candle]
    ) -> Optional[str]:

        if len(candles) < 5:
            return None

        old_direction = (
            candles[0].close < candles[2].close
        )

        new_direction = (
            candles[-3].close < candles[-1].close
        )

        if old_direction and not new_direction:
            return "CHOCH_BEARISH"

        if not old_direction and new_direction:
            return "CHOCH_BULLISH"

        return None


# ==========================================================
# LIQUIDITY ENGINE
# ==========================================================

class LiquidityEngine:
    """
    Finds areas where stop losses and
    large orders may be concentrated.
    """

    def find_zones(
        self,
        candles: List[Candle]
    ) -> List[Dict[str, float]]:

        zones = []

        for index in range(
            1,
            len(candles)
        ):

            current = candles[index]
            previous = candles[index - 1]

            if (
                abs(current.high - previous.high)
                / current.high
            ) < 0.001:

                zones.append({
                    "type": "SELL_SIDE",
                    "price": current.high,
                })

            if (
                abs(current.low - previous.low)
                / current.low
            ) < 0.001:

                zones.append({
                    "type": "BUY_SIDE",
                    "price": current.low,
                })

        return zones


# ==========================================================
# FAIR VALUE GAP ENGINE
# ==========================================================

class FVGEngine:
    """
    Detects market imbalance zones.
    """

    def detect(
        self,
        first: Candle,
        middle: Candle,
        last: Candle
    ) -> Optional[Dict[str, Any]]:


        if last.low > first.high:

            return {
                "type": "BULLISH_FVG",
                "zone": (
                    first.high,
                    last.low,
                ),
            }


        if first.low > last.high:

            return {
                "type": "BEARISH_FVG",
                "zone": (
                    last.high,
                    first.low,
                ),
            }


        return None


# ==========================================================
# SIGNAL DATA PACKET
# ==========================================================

@dataclass
class SignalPacket:
    """
    Unified intelligence packet passed
    to the AI fusion layer.
    """

    structure: float = 0.0

    liquidity: float = 0.0

    fvg: float = 0.0

    bos: float = 0.0

    choch: float = 0.0

    ml: float = 0.0


# ==========================================================
# MARKET INTELLIGENCE AGGREGATOR
# ==========================================================

class MarketIntelligence:
    """
    Combines multiple market analyses
    into a single AI packet.
    """

    def __init__(self):

        self.structure = StructureEngine()

        self.liquidity = LiquidityEngine()

        self.fvg = FVGEngine()


    def evaluate(
        self,
        candles: List[Candle]
    ) -> SignalPacket:

        packet = SignalPacket()


        if self.structure.detect_bos(candles):

            packet.bos = 1.0


        if self.structure.detect_choch(candles):

            packet.choch = 1.0


        if self.liquidity.find_zones(candles):

            packet.liquidity = 1.0


        if len(candles) >= 3:

            gap = self.fvg.detect(
                candles[-3],
                candles[-2],
                candles[-1],
            )

            if gap:

                packet.fvg = 1.0


        # Structure confidence
        packet.structure = (
            packet.bos * 0.5
            +
            packet.choch * 0.5
        )


        return packet


# ==========================================================
# PART 2 END
# ==========================================================
# ==========================================================
# AI FUSION DECISION ENGINE
# ==========================================================

class AIFusionEngine:
    """
    Combines all AI intelligence layers and
    produces a unified confidence score.
    """

    def __init__(self):

        self.weights = {
            "structure": 0.15,
            "liquidity": 0.20,
            "fvg": 0.15,
            "bos": 0.15,
            "choch": 0.10,
            "ml": 0.25,
        }

        self.trade_threshold = 0.70


    def evaluate(
        self,
        packet: SignalPacket
    ) -> Dict[str, Any]:

        score = (
            packet.structure * self.weights["structure"] +
            packet.liquidity * self.weights# ==========================================================
# FSE DECISION ENGINE
# ==========================================================

class FSEDecisionEngine:
    """
    Final decision layer following FSE philosophy.

    FSE does not chase direction.
    The goal is finding high-volatility
    markets and deploying Hedge + Grid
    strategies appropriately.
    """

    def __init__(
        self,
        volatility_engine: VolatilityEngine
    ):

        self.volatility_engine = volatility_engine


    def decide(
        self,
        market: MarketSnapshot,
        ai_result: Dict[str, Any]
    ) -> Dict[str, Any]:

        volatility = self.volatility_engine.calculate(
            market
        )

        # Low volatility markets are avoided
        if self.volatility_engine.should_exit(
            market
        ):
            return {
                "action": "EXIT",
                "reason": "LOW_VOLATILITY",
                "volatility": volatility,
            }


        # High volatility alpha opportunity
        if self.volatility_engine.is_tradeable(
            market
        ):

            return {
                "action": "HEDGE_GRID",
                "long": True,
                "short": True,
                "grid": True,
                "confidence": ai_result.get(
                    "confidence",
                    0.0
                ),
                "volatility": volatility,
            }


        # Market has movement but not enough
        return {
            "action": "WAIT",
            "reason": "VOLATILITY_NOT_READY",
            "volatility": volatility,
        }


# ==========================================================
# SIGNAL GENERATOR
# ==========================================================

class SignalEngine:
    """
    Creates standardized trading signals.
    """

    def generate(
        self,
        symbol: str,
        decision: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:


        if decision["action"] == "HEDGE_GRID":

            return {
                "symbol": symbol,

                "strategy": "FSE_ALPHA_GRID",

                "positions": [
                    {
                        "side": "LONG",
                        "enabled": True,
                    },

                    {
                        "side": "SHORT",
                        "enabled": True,
                    },
                ],

                "grid_enabled": True,
                "volatility": decision["volatility"],
            }


        if decision["action"] == "EXIT":

            return {
                "symbol": symbol,
                "action": "CLOSE_ALL",
                "reason": decision["reason"],
            }


        return None


# ==========================================================
# RELIABILITY ENGINE
# ==========================================================

class ReliabilityEngine:
    """
    Keeps AI state consistent after failures.
    """

    def __init__(self):

        self.last_checkpoint = None


    def save_state(
        self,
        state: Dict[str, Any]
    ) -> None:

        self.last_checkpoint = state


    def recover(
        self
    ) -> Optional[Dict[str, Any]]:

        return self.last_checkpoint


# ==========================================================
# MAIN INFERENCE CONTROLLER
# ==========================================================

class InferenceController:
    """
    Central brain coordinator.

    Flow:
    Market Data
         ↓
    Volatility Check
         ↓
    AI Market Intelligence
         ↓
    AI Fusion Confidence
         ↓
    FSE Decision
         ↓
    Hedge + Grid Signal
    """

    def __init__(self):

        self.memory = MemoryEngine()

        self.volatility = VolatilityEngine()

        self.market_intelligence = (
            MarketIntelligence()
        )

        self.fusion = AIFusionEngine()

        self.decision = FSEDecisionEngine(
            self.volatility
        )

        self.signal_engine = SignalEngine()

        self.reliability = ReliabilityEngine()


    def process(
        self,
        market: MarketSnapshot,
        candles: List[Candle]
    ) -> Optional[Dict[str, Any]]:


        # Analyze market structure
        packet = self.market_intelligence.evaluate(
            candles
        )


        # AI confidence score
        ai_result = self.fusion.evaluate(
            packet
        )


        # Final FSE decision
        decision = self.decision.decide(
            market,
            ai_result
        )


        # Generate execution signal
        signal = self.signal_engine.generate(
            market.symbol,
            decision
        )


        # Store system snapshot
        self.reliability.save_state(
            {
                "symbol": market.symbol,
                "decision": decision,
                "timestamp": time.time(),
            }
        )


        return signal


# ==========================================================
# FSE INFERENCE ENGINE COMPLETE
# ==========================================================
