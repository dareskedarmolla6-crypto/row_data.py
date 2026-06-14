# fse/dashboard/api_server.py

class DashboardController:
    """
    Controls dashboard updates:
    - System status
    - Trade history
    - Profit/Loss statistics
    - Dashboard display
    """

    def __init__(self, status_engine, history_engine, profit_engine, dashboard_ui):
        self.status = status_engine
        self.history = history_engine
        self.profit = profit_engine
        self.dashboard = dashboard_ui

    def update(self, telegram_status, start_balance, current_balance, open_positions):
        # Current system status
        system_status = self.status.get_status(
            current_balance,
            open_positions
        )

        # Calculate PnL
        profit_report = self.profit.calculate_profit(
            start_balance,
            current_balance
        )

        # Get trade history
        trade_history = self.history.get_trades()

        # Update dashboard
        self.dashboard.show(
            telegram_status,
            system_status,
            profit_report,
            trade_history
        )

        return {
            "status": system_status,
            "profit": profit_report,
            "trades": trade_history
        }
