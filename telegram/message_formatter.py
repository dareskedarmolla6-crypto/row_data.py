
# fse/telegram/message_formatter.py
import datetime

class SignalFormatter:
    """ሲግናሎችን ለቴሌግራም ንባብ በሚመች ሁኔታ የሚያቀርብ (መርህ #8)።"""

    def format(self, signal: dict) -> str:
        """የሲግናል መረጃን ወደ ቆንጆ ጽሁፍ መለወጥ።"""
        symbol = signal.get("symbol", "UNKNOWN").upper()
        side = signal.get("side", "UNKNOWN").upper()
        score = signal.get("score", signal.get("strength", 0))
        strategy = signal.get("strategy_id", "N/A")
        price = signal.get("price", "N/A")
        
        # የጊዜ ማህተም (Timestamp)
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        return (
            "🚀 **FSE SIGNAL DETECTED**\n"
            f"━━━━━━━━━━━━━━━━━━\n"
            f"📅 Time     : {timestamp}\n"
            f"💎 Symbol   : {symbol}\n"
            f"📈 Side     : {side}\n"
            f"🎯 Score    : {score}\n"
            f"💰 Price    : {price}\n"
            f"⚙️ Strategy : {strategy}\n"
            f"━━━━━━━━━━━━━━━━━━"
        )
