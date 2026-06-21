# fse/execution/execution_listener.py

import json
import logging
import asyncio
from utils.message_bus import MessageBus

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("FSE.ExecutionListener")


class ExecutionListener:
    def __init__(self, execution_engine):
        self.execution_engine = execution_engine
        self.bus = MessageBus()

    async def start(self):
        pubsub = self.bus.subscribe("TRADE_CHANNEL")
        logger.info("👂 Execution Listener started and waiting for signals...")

        while True:
            try:
                signal = self.bus.listen(pubsub)

                if not signal:
                    await asyncio.sleep(0.5)
                    continue

                # =========================
                # Safety parsing layer
                # =========================
                if isinstance(signal, str):
                    signal = json.loads(signal)

                symbol = signal.get("symbol")
                side = signal.get("side")

                if not symbol or not side:
                    logger.warning("⚠️ Invalid signal skipped")
                    continue

                logger.info(f"⚡ Signal received: {symbol} - {side}")

                # =========================
                # Execution layer
                # =========================
                result = await self.execution_engine.execute_signal(signal)

                logger.info(f"✅ Trade Executed: {result}")

            except Exception as e:
                logger.error(f"❌ Execution error: {e}")
                await asyncio.sleep(1)


# =========================
# Runner
# =========================
if __name__ == "__main__":
    from fse.execution.engine import ExecutionEngine

    engine = ExecutionEngine()
    listener = ExecutionListener(engine)

    asyncio.run(listener.start())
