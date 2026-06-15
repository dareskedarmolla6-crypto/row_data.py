
# fse/brain/optimization_core.py
from typing import Dict, List, Any, Optional
import logging

logger = logging.getLogger("FSE.Brain.Optimization")

# ==========================================================
# AI FUSION & EVOLUTION ENGINES
# ==========================================================

class AIFusionEngine:
    """መርህ #4 (Confidence Scoring): የውሳኔ አሰጣጥ ማዕከል (Weighted Scoring)።"""
    def __init__(self):
        self.weights = {"structure": 0.15, "liquidity": 0.20, "fvg": 0.15, "bos": 0.15, "choch": 0.10, "ml": 0.25}
        self.trade_threshold = 0.70

    def evaluate(self, packet: Any) -> Dict[str, Any]:
        score = sum(getattr(packet, key, 0) * weight for key, weight in self.weights.items())
        return {"confidence": round(score, 4), "approved": score >= self.trade_threshold}

class EvolutionEngine:
    """መርህ #1 እና #8: ስልቶችን በየጊዜው በማሻሻል (Evolution) የሪስክ መጠን ማስተካከያ።"""
    def __init__(self, memory, analyzer):
        self.memory = memory
        self.analyzer = analyzer
        self.parameters = {"grid_distance": 1.0, "capital_risk": 1.0, "volatility_requirement": 15.0}

    def evolve(self) -> Dict[str, float]:
        history = self.memory.get_recent(200)
        if len(history) < 20: return self.parameters
        
        result = self.analyzer.analyze(history)
        if result["win_rate"] < 0.45: self.parameters["capital_risk"] *= 0.90
        elif result["win_rate"] > 0.65: self.parameters["capital_risk"] *= 1.05
        return self.parameters

# ==========================================================
# DEEP AI & ADAPTIVE CONTROL
# ==========================================================

class DeepAIEngine:
    """መርህ #10 (Reliability): በ Reinforcement Learning ላይ የተመሰረተ ውሳኔ ሰጪ።"""
    def __init__(self, policy, reward_engine, state_builder):
        self.policy, self.reward_engine, self.state_builder = policy, reward_engine, state_builder

    def execute(self, market_data: Dict[str, Any]) -> Dict[str, Any]:
        state = self.state_builder.build(market_data)
        action = self.policy.act(state)
        reward = self.reward_engine.calculate(action, market_data)
        self.policy.learn(state, reward)
        return {"action": action, "reward": reward}

class AdaptiveMode:
    """መርህ #7: እንደ ዊን ሬት (Win Rate) የቦቱን ጠባይ መቀያየሪያ።"""
    def select(self, win_rate: float) -> str:
        if win_rate < 0.40: return "DEFENSIVE"
        if win_rate < 0.65: return "BALANCED"
        return "AGGRESSIVE"
