
# FSE API REFERENCE - LEVERAGE & RISK SYSTEM

## 1. Overview
This document defines the confidence-based adaptive leverage system used in the FSE trading engine to optimize risk-adjusted returns.

---

## 2. Confidence → Leverage Mapping (Core Logic)
The system determines trade strength based on AI-calculated confidence levels.

| Confidence Range | Leverage |
| :--- | :--- |
| < 15% | NO TRADE (Safety Cutoff) |
| 15 – 25% | 5x |
| 26 – 35% | 8x |
| 36 – 55% | 10x |
| 56 – 75% | 15x |
| 76 – 85% | 20x |
| 86%+ | 30x |

---

## 3. Volatility & Risk Adjustment Rules
Leverage is dynamically adjusted based on market environment:
- **High Volatility (≥ 0.8):** Leverage reduced by 50% to mitigate liquidation risk.
- **Low Volatility (≤ 0.3):** Leverage increased by 10-20% to boost opportunity capture.
- **Hedge Mode:** Leverage is automatically capped to maintain dual-position safety.

---

## 4. Execution Scope (Supported Markets)
FSE operates across diverse asset classes:
- **Crypto:** Binance, Bybit, OKX, KuCoin, Gate.io, MEXC, Bitget.
- **Forex:** MT5, OANDA, IC Markets, Pepperstone, Exness.
- **Future Markets:** Indices, Commodities (Gold, Silver, Oil), Stocks.

---

## 5. Risk Control & Safety Protocol
- **Hard Limit:** Confidence below 15% results in immediate trade rejection.
- **Exposure Cap:** Maximum allowable leverage is strictly 30x.
- **Validation:** Every signal must pass the "Risk Engine" safety check before any order is routed to an exchange.

---

## 6. Safety Warning
FSE is built for high-alpha environment exploitation.
* **Caution:** High leverage significantly increases liquidation probability.
* **Recommendation:** Always ensure stop-loss parameters are pre-configured before enabling high-leverage modes.
