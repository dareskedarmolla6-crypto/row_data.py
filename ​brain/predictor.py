
# fse/brain/predictor.py
import numpy as np
from sklearn.linear_model import LogisticRegression
from collections import defaultdict
import logging

logger = logging.getLogger("FSE.Brain")

# ==========================================================
# ML-BASED AI BRAIN (LEARNING LAYER)
# ==========================================================

class AIBrain:
    """መርህ #1: የገበያ መረጃን ተንትኖ Alpha እድሎችን የሚለይ ሞዴል።"""
    def __init__(self):
        self.model = LogisticRegression()
        self.trained = False

    def train(self):
        X = np.random.uniform(-3, 3, (1000, 2))
        y = np.where(X[:, 0] > 1, 1, np.where(X[:, 0] < -1, -1, 0))
        self.model.fit(X, y)
        self.trained = True

    def predict(self, data: dict):
        if not self.trained: self.train()
        X = np.array([[data.get("price_change", 0), data.get("volume", 0)]])
        
        pred = self.model.predict(X)[0]
        prob = np.max(self.model.predict_proba(X))
        
        mapping = {1: "LONG", -1: "SHORT", 0: "HEDGE"}
        return mapping[pred], round(prob * 100, 2)

# ==========================================================
# FSE CORE DECISION GATE
# ==========================================================

class FSECore:
    """መርህ #4 እና #7: ከሪስክ ሞተር ጋር ተቀናጅቶ ውሳኔ የሚሰጥ ዋና በረኛ።"""
    def __init__(self, brain, risk):
        self.brain = brain
        self.risk = risk

    def decide(self, market: dict, balance: float, pos_size: float, open_pos: list, drawdown: float):
        if self.risk.emergency_stop(drawdown):
            return "SYSTEM_STOP"

        # AI ውሳኔ
        side, conf = self.brain.predict(market)
        
        if self.risk.check_trade(balance, pos_size, open_pos) != "APPROVED":
            return "TRADE_BLOCKED"

        if conf < 60: return "HEDGE"
        return side

# ==========================================================
# CONSENSUS & RL POLICY NETWORK
# ==========================================================

class SmartConsensusEngine:
    """መርህ #9: የብዙ ሲግናሎችን ድምር ውጤት የሚወስን ሞተር።"""
    def process(self, signals: list):
        votes = defaultdict(lambda: {"buy": 0, "sell": 0})
        for s in signals:
            if s["side"] == "BUY": votes[s["symbol"]]["buy"] += s.get("score", 10)
            elif s["side"] == "SELL": votes[s["symbol"]]["sell"] += s.get("score", 10)
        
        consensus = []
        for symbol, v in votes.items():
            total = v["buy"] + v["sell"]
            if total == 0: continue
            bias = (v["buy"] - v["sell"]) / total
            if abs(bias) > 0.3:
                consensus.append({"symbol": symbol, "side": "BUY" if bias > 0 else "SELL", "strength": round(abs(bias), 2)})
        return consensus

class PolicyNetwork:
    """መርህ #8: በተጠናከረ ትምህርት (Reinforcement Learning) ላይ የተመሰረተ ውሳኔ ሰጪ።"""
    def __init__(self, state_size=5):
        self.weights = np.random.randn(state_size)
        self.lr = 0.01

    def act(self, state: np.array):
        score = np.dot(self.weights, state)
        if score > 0.5: return "LONG"
        if score < -0.5: return "SHORT"
        return "HOLD"

    def learn(self, state: np.array, reward: float):
        self.weights += self.lr * reward * state
