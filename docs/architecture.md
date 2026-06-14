# FSE Trading Bot Architecture

## 1. Overview

FSE (Financial Smart Engine) is a multi-market AI trading system designed for:

- Crypto markets (Binance, Bybit, OKX, KuCoin, Gate.io, MEXC, Bitget)
- Forex markets (MT5, OANDA, IC Markets, Pepperstone, Exness)
- Future expansion: Indices, Commodities, Stocks

The system supports:
- Long / Short / Hedge trading
- Grid trading
- AI-driven decision making
- Risk-based leverage scaling
- Multi-exchange routing

---

## 2. Core Modules

### 2.1 Brain Layer (AI Engine)
Responsible for:
- Market prediction
- Signal generation (LONG / SHORT / HEDGE)
- Confidence scoring (0–100%)

Output:
```json
{
  "signal": "LONG",
  "confidence": 78
}
