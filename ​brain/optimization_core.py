# ==========================================================
# AI FUSION DECISION ENGINE
# ==========================================================

class AIFusionEngine:
    """
    Combines all AI intelligence layers and
    produces a unified confidence score.
    """

    def __init__(self):

        self.weights = {
            "structure": 0.15,
            "liquidity": 0.20,
            "fvg": 0.15,
            "bos": 0.15,
            "choch": 0.10,
            "ml": 0.25,
        }

        self.trade_threshold = 0.70


    def evaluate(
        self,
        packet: SignalPacket
    ) -> Dict[str, Any]:

        score = (
            packet.structure * self.weights["structure"] +
            packet.liquidity * self.weights["liquidity"] +
            packet.fvg * self.weights["fvg"] +
            packet.bos * self.weights["bos"] +
            packet.choch * self.weights["choch"] +
            packet.ml * self.weights["ml"]
        )

        return {
            "confidence": round(score, 4),
            "approved": score >= self.trade_threshold,
        }


# ==========================================================
# STRATEGY MEMORY & PERFORMANCE ANALYZER
# ==========================================================

class PerformanceAnalyzer:
    """
    Analyzes historical trading performance.
    """

    def analyze(
        self,
        trades: List[TradeRecord]
    ) -> Dict[str, float]:

        if not trades:
            return {
                "win_rate": 0.0,
                "average_profit": 0.0,
            }


        wins = sum(
            1 for trade in trades
            if trade.profit > 0
        )

        total_profit = sum(
            trade.profit
            for trade in trades
        )

        return {
            "win_rate": wins / len(trades),
            "average_profit": (
                total_profit / len(trades)
            )
        }


# ==========================================================
# SELF LEARNING ENGINE
# ==========================================================

class SelfLearningEngine:
    """
    Learns which strategy performs better
    in different market conditions.
    """

    def __init__(self):

        self.strategy_scores: Dict[str, float] = {}


    def update(
        self,
        strategy: str,
        profit: float
    ) -> None:

        current = self.strategy_scores.get(
            strategy,
            0.0
        )

        self.strategy_scores[strategy] = (
            current + profit
        )


    def best_strategy(
        self
    ) -> Optional[str]:

        if not self.strategy_scores:
            return None


        return max(
            self.strategy_scores,
            key=self.strategy_scores.get
        )


# ==========================================================
# EVOLUTION ENGINE
# ==========================================================

class EvolutionEngine:
    """
    Gradually improves strategy parameters
    based on historical performance.
    """

    def __init__(
        self,
        memory: MemoryEngine,
        analyzer: PerformanceAnalyzer
    ):

        self.memory = memory

        self.analyzer = analyzer


        self.parameters = {

            "grid_distance": 1.0,

            "capital_risk": 1.0,

            "volatility_requirement": 15.0,
        }


    def evolve(
        self
    ) -> Dict[str, float]:


        history = self.memory.get_recent(200)


        if len(history) < 20:

            return self.parameters


        result = self.analyzer.analyze(history)


        if result["win_rate"] < 0.45:

            self.parameters["capital_risk"] *= 0.90


        elif result["win_rate"] > 0.65:

            self.parameters["capital_risk"] *= 1.05


        return self.parameters


# ==========================================================
# DEEP AI POLICY ENGINE
# ==========================================================

class DeepAIEngine:
    """
    Reinforcement learning style decision engine.
    """

    def __init__(
        self,
        policy,
        reward_engine,
        state_builder
    ):

        self.policy = policy

        self.reward_engine = reward_engine

        self.state_builder = state_builder


    def execute(
        self,
        market_data: Dict[str, Any]
    ) -> Dict[str, Any]:


        state = self.state_builder.build(
            market_data
        )


        action = self.policy.act(
            state
        )


        reward = self.reward_engine.calculate(
            action,
            market_data
        )


        self.policy.learn(
            state,
            reward
        )


        return {
            "action": action,
            "reward": reward,
        }


# ==========================================================
# AI STATE BUILDER
# ==========================================================

class StateBuilder:
    """
    Converts market data into AI state vectors.
    """

    def build(
        self,
        data: Dict[str, Any]
    ) -> List[float]:


        return [

            float(data.get(
                "volatility",
                0.0
            )),

            float(data.get(
                "volume",
                0.0
            )),

            float(data.get(
                "liquidity",
                0.0
            )),

            float(data.get(
                "momentum",
                0.0
            )),
        ]


# ==========================================================
# ADAPTIVE TRADING MODE
# ==========================================================

class AdaptiveMode:
    """
    Changes internal aggressiveness based
    on performance.
    """

    def select(
        self,
        win_rate: float
    ) -> str:


        if win_rate < 0.40:

            return "DEFENSIVE"


        if win_rate < 0.65:

            return "BALANCED"


        return "AGGRESSIVE"


# ==========================================================
# PART 3 END
# ==========================================================
