# fse/brain/signal_generator.py

import time
import random
import logging
import json
import asyncio
from typing import Dict, List, Optional
from datetime import datetime

logger = logging.getLogger("FSE.Brain.SignalGen")

# ==========================================================
# CONFIDENCE → LEVERAGE MAP (FSE CORE RULE)
# ==========================================================

def calculate_leverage(confidence: int, volatility: float) -> int:
    """
    Confidence-based leverage system (FSE CORE RULE)
    """
    if confidence < 15:
        return 0
    elif confidence <= 25:
        base = 5
    elif confidence <= 35:
        base = 8
    elif confidence <= 55:
        base = 10
    elif confidence <= 75:
        base = 15
    elif confidence <= 85:
        base = 20
    else:
        base = 30

    # ---- VOLATILITY SAFETY LAYER ----
    if volatility > 0.7:
        base -= 5
    elif volatility > 0.5:
        base -= 2

    return max(base, 0)


# ==========================================================
# FUSION & CONSENSUS LAYERS
# ==========================================================

class BrainSignalGenerator:
    """Multi-model consensus-based signal generator"""
    def __init__(self, predictor, inference_engine, feature_engine):
        self.predictor = predictor
        self.inference_engine = inference_engine
        self.feature_engine = feature_engine

    def generate(self, data: Dict) -> List[Dict]:
        pred, conf1 = self.predictor.predict(data)
        inf, conf2 = self.inference_engine.analyze(data)
        mode = self.feature_engine.adjust(data.get("win_rate", 0.5))

        confidence_avg = int((conf1 + conf2) / 2)

        if pred == inf:
            side = pred
        else:
            side = pred if conf1 >= conf2 else inf

        if confidence_avg < 50:
            side = "HEDGE"

        return [{
            "symbol": data.get("symbol"),
            "side": side,
            "confidence": confidence_avg,
            "mode": mode
        }]


# ==========================================================
# MARKET REGIME ENGINE
# ==========================================================

class MarketRegimeAI:
    def classify(self, data: Dict) -> str:
        vol = data.get("volatility", 0)
        mom = data.get("momentum", 0)

        if vol > 0.75:
            return "CHAOTIC"
        if mom > 0.25:
            return "TRENDING_UP"
        if mom < -0.25:
            return "TRENDING_DOWN"
        return "SIDEWAYS"


# ==========================================================
# AI DECISION ENGINE (WITH LEVERAGE INTEGRATION)
# ==========================================================

class AIDecisionEngine:
    def __init__(self, filter_layer, position_engine, regime_ai):
        self.filter = filter_layer
        self.position_engine = position_engine
        self.regime_ai = regime_ai

    def decide(self, symbol: str, structure: Dict, market_data: Dict, wallet: float) -> Optional[Dict]:

        regime = self.regime_ai.classify(market_data)
        if regime == "CHAOTIC":
            return None

        pred = structure.get("prediction", "BUY")
        confidence = structure.get("confidence", 50)
        volatility = market_data.get("volatility", 0)

        signal = {
            "symbol": symbol,
            "side": pred,
            "score": confidence
        }

        if not self.filter.validate(structure, signal):
            return None

        signal["qty"] = self.position_engine.adjust_size(signal, wallet)
        signal["regime"] = regime

        # =========================
        # LEVERAGE INTEGRATION
        # =========================
        leverage = calculate_leverage(confidence, volatility)
        if leverage == 0:
            return None

        signal["leverage"] = leverage
        return signal


# ==========================================================
# CORE BOT ORCHESTRATION
# ==========================================================

class TradingBotCore:
    def __init__(self, data_engine, strategy_engine, risk_engine,
                 execution_engine, portfolio_engine, monitor, telegram=None):

        self.data = data_engine
        self.strategy = strategy_engine
        self.risk = risk_engine
        self.execution = execution_engine
        self.portfolio = portfolio_engine
        self.monitor = monitor
        self.telegram = telegram
        self.running = False

    async def run_once(self):
        market_data = self.data.get_snapshot()
        signals = self.strategy.generate(market_data)

        for signal in signals:
            if not self.risk.validate(signal, self.portfolio.state()):
                continue

            logger.info(f"🚀 Signal: {json.dumps(signal)}")

            result = self.execution.execute_signal(signal)
            self.portfolio.update(result)
            self.monitor.record_trade()

            if self.telegram:
                self.telegram.notify_trade(
                    signal["symbol"],
                    signal["side"],
                    result.get("pnl", 0) if result else 0
                )

    async def start(self, interval: int = 3):
        self.running = True
        logger.info("🚀 FSE BOT STARTED")

        while self.running:
            try:
                await self.run_once()
                await asyncio.sleep(interval)

            except Exception as e:
                logger.error(f"FATAL ERROR: {e}")

