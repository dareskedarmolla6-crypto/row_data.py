
# fse/dashboard/app.py
from flask import Flask, jsonify
import logging

# Logger setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# =========================
# GLOBAL SYSTEM STATE
# =========================
system_state = {
    "status": "RUNNING",
    "balance": 0.0,
    "total_trades": 0,
    "profit": 0.0,
    "market_mode": "LIVE",
    "bot_status": "ACTIVE",
    "risk_status": "MANAGED"
}

# =========================
# API ENDPOINTS
# =========================
@app.route("/status", methods=['GET'])
def status():
    return jsonify(system_state)

@app.route("/live", methods=['GET'])
def live():
    return jsonify({
        "market": system_state["market_mode"],
        "bot": system_state["bot_status"],
        "risk": system_state["risk_status"]
    })

@app.route("/health", methods=['GET'])
def health():
    return jsonify({"status": "OK", "message": "System operational"})

# =========================
# SYSTEM STATE UPDATE (SAFE)
# =========================
def safe_update_state(balance, trades, profit, status="RUNNING"):
    """የቦቱን መረጃዎች በደህንነት መለኪያ ማዘመን (መርህ #7)"""
    system_state.update({
        "status": status,
        "balance": max(0.0, float(balance)),
        "total_trades": max(0, int(trades)),
        "profit": float(profit)
    })
    logger.info("📊 Dashboard state updated.")

# =========================
# LIVE DASHBOARD CONTROLLER
# =========================
class LiveDashboard:
    def __init__(self, core):
        self.core = core

    def get_system_status(self):
        return {
            "bot": "RUNNING" if getattr(self.core, "running", False) else "STOPPED",
            "balance": getattr(self.core, "balance", 0.0)
        }

    def update_panels(self):
        return {
            "balance": getattr(self.core, "balance", 0.0),
            "positions": getattr(self.core, "positions", []),
            "risk": getattr(self.core, "last_risk", "UNKNOWN")
        }

    def control_panel(self, command):
        commands = {
            "START": "BOT_STARTED",
            "STOP": "BOT_STOPPED",
            "SAFE_MODE": "SAFE_MODE_ENABLED",
            "KILL_SWITCH": "EMERGENCY_STOP"
        }
        return commands.get(command, "INVALID_COMMAND")

if __name__ == "__main__":
    logger.info("🌐 FSE Dashboard API Server starting on port 5000...")
    app.run(host="0.0.0.0", port=5000, debug=False)
