class GridStrategy:
    """
    Grid trading strategy:
    Places multiple buy/sell orders at different price levels.
    """

    def __init__(self, levels=5):
        self.levels = levels

    def generate_levels(self, base_price, step_pct=0.5):
        """
        Creates grid price levels around base price.
        """
        levels = []

        for i in range(1, self.levels + 1):
            lower = base_price * (1 - (step_pct / 100) * i)
            upper = base_price * (1 + (step_pct / 100) * i)

            levels.append({"buy": lower, "sell": upper})

        return levels

    def execute(self, executor, symbol, base_size, base_price):
        """
        Executes grid orders using executor.
        """
        levels = self.generate_levels(base_price)
        orders = []

        step_size = base_size / self.levels

        for level in levels:
            buy_order = executor.open_long(symbol, step_size)
            orders.append({"type": "BUY", "price": level["buy"], "order": buy_order})

        return {
            "symbol": symbol,
            "orders": orders,
            "status": "GRID_PLACED"
        }
