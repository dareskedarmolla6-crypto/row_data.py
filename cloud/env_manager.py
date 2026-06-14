import os
import json
from dataclasses import dataclass
from typing import Optional


# =========================
# ENV LOADER CORE
# =========================
class EnvManager:
    """
    Handles all environment variables safely for cloud deployment (Oracle, AWS, etc.)
    """

    def __init__(self, env_file: Optional[str] = ".env"):
        self.env_file = env_file
        self._load_env_file()

    # -------------------------
    # Load .env if exists
    # -------------------------
    def _load_env_file(self):
        if not self.env_file:
            return

        if not os.path.exists(self.env_file):
            return

        with open(self.env_file, "r") as f:
            for line in f:
                line = line.strip()

                if not line or line.startswith("#"):
                    continue

                if "=" in line:
                    key, value = line.split("=", 1)
                    os.environ.setdefault(key.strip(), value.strip())

    # -------------------------
    # GET ENV VARIABLE
    # -------------------------
    def get(self, key: str, default=None):
        return os.getenv(key, default)

    # -------------------------
    # REQUIRED ENV VARIABLE
    # -------------------------
    def require(self, key: str):
        value = os.getenv(key)
        if value is None:
            raise EnvironmentError(f"❌ Missing required env variable: {key}")
        return value

    # -------------------------
    # BOOLEAN ENV
    # -------------------------
    def get_bool(self, key: str, default=False):
        value = os.getenv(key, str(default))
        return value.lower() in ["1", "true", "yes", "y"]

    # -------------------------
    # INT ENV
    # -------------------------
    def get_int(self, key: str, default=0):
        try:
            return int(os.getenv(key, default))
        except ValueError:
            return default

    # -------------------------
    # FLOAT ENV
    # -------------------------
    def get_float(self, key: str, default=0.0):
        try:
            return float(os.getenv(key, default))
        except ValueError:
            return default


# =========================
# CONFIG MODEL (FSE CORE SETTINGS)
# =========================
@dataclass
class FSEConfig:
    # Exchange
    binance_api_key: str
    binance_api_secret: str

    # Risk
    max_leverage: int = 3
    max_risk_per_trade: float = 0.02

    # Trading
    symbol: str = "DOGEUSDT"
    scan_interval: int = 3

    # Cloud
    environment: str = "development"
    debug_mode: bool = False

    # Telegram
    telegram_token: str = ""
    telegram_chat_id: str = ""


# =========================
# CONFIG BUILDER
# =========================
class ConfigLoader:
    def __init__(self, env: EnvManager):
        self.env = env

    def load(self) -> FSEConfig:
        return FSEConfig(
            binance_api_key=self.env.require("BINANCE_API_KEY"),
            binance_api_secret=self.env.require("BINANCE_API_SECRET"),

            max_leverage=self.env.get_int("MAX_LEVERAGE", 3),
            max_risk_per_trade=self.env.get_float("MAX_RISK_PER_TRADE", 0.02),

            symbol=self.env.get("TRADE_SYMBOL", "DOGEUSDT"),
            scan_interval=self.env.get_int("SCAN_INTERVAL", 3),

            environment=self.env.get("ENV", "development"),
            debug_mode=self.env.get_bool("DEBUG", False),

            telegram_token=self.env.get("TELEGRAM_TOKEN", ""),
            telegram_chat_id=self.env.get("TELEGRAM_CHAT_ID", "")
        )


# =========================
# GLOBAL SINGLETON (OPTIONAL)
# =========================
env_manager = EnvManager()
config = ConfigLoader(env_manager).load()


# =========================
# DEBUG PRINT (SAFE)
# =========================
def print_config():
    print("===== FSE CONFIG =====")
    print(json.dumps(config.__dict__, indent=4))
