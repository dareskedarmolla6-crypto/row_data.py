
# FSE Trading Bot - System Design

## 1. Overview
FSE (Flexible Smart Engine) is a hybrid AI-driven crypto/forex trading system designed to:
- Analyze market volatility (Alpha filter)
- Generate trading signals (LONG / SHORT / HEDGE)
- Dynamically adjust leverage based on confidence
- Manage risk and liquidation exposure
- Execute trades across multiple exchanges

---

## 2. Core Architecture
The system is divided into 5 main layers:

### 2.1 Data Layer
- **Ingestion:** Market data from Crypto (Binance/Bybit/etc.) and Forex (MT5/OANDA/etc.) brokers.
- **Processing:** Normalization, caching, and raw data buffering for backtesting.

### 2.2 Brain Layer (AI Engine)
- **Signal Generation:** Predicts market direction (LONG/SHORT/HEDGE).
- **Confidence Engine:** Outputs confidence levels (0-100%) to drive adaptive leverage.

### 2.3 Risk Management Layer (The Guard)
- **Compliance:** Enforces `MIN_CONFIDENCE`, `MAX_LEVERAGE`, and `MAX_OPEN_POSITIONS`.
- **Protection:** Stop-loss, Trailing-stop, and Partial-TP execution logic.
- **Liquidation Guard:** Emergency stop-loss triggers based on `MAX_DAILY_LOSS`.

### 2.4 Execution Layer
- **Router:** Smart order routing across different exchanges/brokers.
- **Order State Manager:** Tracking CREATED, OPEN, FILLED, and CLOSED states.

### 2.5 Dashboard Layer (Monitoring)
- **API Server:** Flask-based REST API for system status.
- **Metrics View:** Real-time logging of PnL, Win-rate, and Drawdown.
- **Visualization:** WebSocket-based live data broadcasting.

---

## 3. Communication Flow
1. **Collector:** Fetches market raw data.
2. **Normalizer:** Prepares features for the Brain.
3. **Brain:** Analyzes features and emits a signal.
4. **Risk Manager:** Validates signal against safety constraints.
5. **Executor:** Places the order if valid.
6. **Dashboard:** Reports outcome to the user.
