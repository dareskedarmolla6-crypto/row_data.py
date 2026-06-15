
# main.py
import asyncio
import logging
from fse.brain.predictor import AIBrain # ቀደም ሲል የሰራነውን AI አዕምሮ መጠቀም
from fse.utils.logger import setup_logger # የሎገር ስራህን እዚህ ማቀናጀት

# ሎገርን ማስጀመር
setup_logger()
logger = logging.getLogger("FSE.Main")

# =========================
# CORE SYSTEM EXECUTION
# =========================

class FSECore:
    def __init__(self, brain, risk, execution, telegram):
        self.brain = brain
        self.risk = risk
        self.execution = execution
        self.telegram = telegram
        self.balance = 1000.0
        self.running = False

    async def trade_cycle(self, symbol="DOGEUSDT"):
        """መርህ #9: የእያንዳንዱ የንግድ ዑደት አስተዳዳሪ።"""
        try:
            # 1. መረጃ ማግኘት (Market Feed)
            data = {"price_change": 1.5, "volume": 150000} # ምሳሌ መረጃ
            
            # 2. የ AI ውሳኔ
            signal, confidence = self.brain.predict(data)

            # 3. የሪስክ ማጣሪያ
            approved, reason = self.risk.approve_trade(signal, confidence)
            if not approved:
                await self.telegram.send_message(f"🛑 BLOCKED: {reason}")
                return

            # 4. የንግድ መጠን ስሌት
            size = self.risk.position_size(self.balance, confidence)

            # 5. አፈጻጸም
            if signal == "LONG": self.execution.open_long(symbol, size)
            elif signal == "SHORT": self.execution.open_short(symbol, size)
            else: # HEDGE
                self.execution.open_long(symbol, size / 2)
                self.execution.open_short(symbol, size / 2)

            await self.telegram.send_message(f"📊 TRADE EXECUTED | SIGNAL: {signal} | CONF: {confidence}")

        except Exception as e:
            logger.error(f"Trade cycle failed: {e}")

    async def run(self):
        self.running = True
        logger.info("🚀 FSE SYSTEM STARTING...")
        await self.telegram.send_message("🚀 FSE SYSTEM STARTED")

        while self.running:
            await self.trade_cycle()
            await asyncio.sleep(3) # መርህ #6: የ 3 ሰከንድ ቅኝት (Scanner)

    def stop(self):
        self.running = False

# =========================
# ENTRY POINT
# =========================
async def main():
    # በፕሮጀክቱ ውስጥ የገነባናቸውን ሞጁሎች እዚህ እናቀናጅ
    system = FSECore(
        brain=AIBrain(), # AI Brain
        risk=RiskAI(),   # Risk Engine
        execution=Execution(),
        telegram=TelegramBot()
    )
    await system.run()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("System manually stopped by user.")
