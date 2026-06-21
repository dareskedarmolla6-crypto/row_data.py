import logging
import json
import asyncio
from typing import Dict, List, Optional

from utils.message_bus import MessageBus

logger = logging.getLogger("FSE.Brain.Signals")

# ==========================================================
# CONFIDENCE → LEVERAGE MAP
# ==========================================================

def calculate_leverage(confidence: int, volatility: float) -> int:
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

    # volatility adjustment
    if volatility > 0.7:
        base -= 5
    elif volatility > 0.5:
        base -= 2

    return max(base, 0)


# ==========================================================
# TRADING BOT CORE (DISTRIBUTED VERSION)
# ==========================================================

class TradingBotCore:
    def __init__(
        self,
        data_engine,
        strategy_engine,
        risk_engine,
        execution_engine,
        portfolio_engine,
        monitor,
        telegram=None
    ):
        self.data = data_engine
        self.strategy = strategy_engine
        self.risk = risk_engine
        self.execution = execution_engine
        self.portfolio = portfolio_engine
        self.monitor = monitor
        self.telegram = telegram

        self.running = False
        self.bus = MessageBus()

    async def run_once(self):
        market_data = self.data.get_snapshot()
        signals = self.strategy.generate(market_data)

        for signal in signals:

            if not self.risk.validate(signal, self.portfolio.state()):
                continue

            logger.info(f"📡 Publishing Signal: {json.dumps(signal)}")

            # 🔁 Distributed layer (message bus)
            self.bus.publish_signal("TRADE_CHANNEL", signal)

            result = self.execution.execute_signal(signal)

            # portfolio update uses execution result if available
            self.portfolio.update(result if result else signal)

            self.monitor.record_trade()

            if self.telegram:
                self.telegram.notify_trade(
                    signal["symbol"],
                    signal["side"],
                    result.get("pnl", 0) if result else 0
                )

    async def start(self, interval: int = 3):
        self.running = True
        logger.info("🚀 FSE BOT STARTED (Distributed Ready)")

        while self.running:
            try:
                await self.run_once()
                await asyncio.sleep(interval)

            except Exception as e:
                logger.error(f"FATAL ERROR: {e}")
