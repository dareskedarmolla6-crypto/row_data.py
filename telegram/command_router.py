
# fse/telegram/command_router.py
import logging

logger = logging.getLogger(__name__)

# =========================
# CONTROL CENTER (DASHBOARD)
# =========================
class ControlCenter:
    """የቦቱን አጠቃላይ ሁኔታ በዳሽቦርድ መልክ የሚያሳውቅ (መርህ #8)።"""
    
    def __init__(self, telegram):
        self.telegram = telegram

    async def update_all(self, state: dict):
        """የስርዓቱን ሁኔታ በቴሌግራም መላክ።"""
        msg = (
            f"📊 FSE DASHBOARD UPDATE\n\n"
            f"💰 Balance: {state.get('balance', 0):.2f}\n"
            f"📈 Trades: {state.get('trades', 0)}\n"
            f"💹 Profit: {state.get('profit', 0):.2f}\n"
            f"⚙️ Status: {state.get('status', 'UNKNOWN')}"
        )
        await self.telegram.send_message(msg)
        logger.info("📡 Dashboard update sent to Telegram.")

# =========================
# SIGNAL DISTRIBUTOR (MULTI-CHANNEL)
# =========================
class SignalDistributor:
    """ሲግናሎችን በተለያዩ የኮሙዩኒኬሽን መስመሮች ማሰራጨት።"""
    
    def __init__(self, telegram=None, discord=None, email=None):
        self.telegram = telegram
        self.discord = discord
        self.email = email

    async def broadcast(self, signal: dict):
        """ሲግናሉን ወደ ተመረጡት መስመሮች መላክ።"""
        msg = self._format(signal)

        if self.telegram:
            await self.telegram.send_message(msg)
        
        if self.discord:
            # Discord መላኪያ ትዕዛዝ እዚህ ይገባል
            logger.info("🎮 Discord broadcast triggered.")
            
        if self.email:
            # Email መላኪያ ትዕዛዝ እዚህ ይገባል
            logger.info("📧 Email broadcast triggered.")

    def _format(self, signal: dict) -> str:
        """ሲግናልን ለንባብ በሚመች ሁኔታ መቅረጽ።"""
        return (
            "📡 FSE SIGNAL ALERT\n\n"
            f"Symbol: {signal.get('symbol', 'N/A')}\n"
            f"Action: {signal.get('action', 'N/A')}\n"
            f"Confidence: {signal.get('confidence', 0)}%"
        )
