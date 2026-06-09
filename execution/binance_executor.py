import ccxt

class BinanceExecutor:
    def __init__(self, api_key, api_secret):
        self.exchange = ccxt.binance({
            'apiKey': api_key,
            'secret': api_secret,
            'enableRateLimit': True,
        })

    def place_order(self, symbol, side, amount, order_type='market'):
        """
        Executes a trade on Binance.
        side: 'buy' or 'sell'
        """
        try:
            order = self.exchange.create_order(symbol, order_type, side, amount)
            return order
        except Exception as e:
            return f"Order failed: {e}"

    def get_balance(self):
        return self.exchange.fetch_balance()
