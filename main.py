import asyncio
import logging
import threading

# የፕሮጀክትህን የሞጁል አወቃቀር መሰረት ያደረገ ኢምፖርት
from fse.brain.signals import TradingBotCore
from fse.execution.execution_listener import run_listener
from fse.execution.engine import Execution
from fse.utils.logger import setup_logger
from fse.communication.telegram import TelegramBot

# የእርስዎን ሞጁሎች (እንደየ ፋይል ቦታቸው ያስገቡ)
from fse.data.engine import DataEngine
from fse.brain.strategy import StrategyEngine
from fse.risk.engine import RiskEngine
from fse.portfolio.engine import PortfolioEngine
from fse.monitor.engine import Monitor

setup_logger()
logger = logging.getLogger("FSE.Main")

async def main():
    logger.info("🚀 FSE SYSTEM STARTING (Cloud Ready)...")

    # 1. ሞጁሎችን ማስጀመር
    exec_engine = Execution()
    data_eng = DataEngine()
    strat_eng = StrategyEngine()
    risk_eng = RiskEngine()
    port_eng = PortfolioEngine()
    mon_eng = Monitor()
    tele_bot = TelegramBot()

    # 2. Execution Listener-ን በ background (Thread) ማስጀመር
    listener_thread = threading.Thread(
        target=run_listener,
        args=(exec_engine,),
        daemon=True
    )
    listener_thread.start()
    logger.info("📡 Execution Listener Started")

    # 3. ዋናውን የቦት ኮር ማስጀመር
    bot = TradingBotCore(
        data_engine=data_eng,
        strategy_engine=strat_eng,
        risk_engine=risk_eng,
        execution_engine=exec_engine,
        portfolio_engine=port_eng,
        monitor=mon_eng,
        telegram=tele_bot
    )

    # 4. ቦቱን ማሰራት
    await bot.start()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("System stopped by user.")
