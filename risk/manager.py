class RiskManager:

    def __init__(
        self,
        balance,
        risk_percentage=0.02,
        max_daily_loss=0.10,
        max_position_percentage=0.10
    ):
        self.balance = balance
        self.risk_percentage = risk_percentage
        self.max_daily_loss = max_daily_loss
        self.max_position_percentage = max_position_percentage

        self.daily_loss = 0

    def calculate_position_size(self, stop_loss_distance):

        if stop_loss_distance <= 0:
            return 0

        risk_amount = self.balance * self.risk_percentage

        position_size = risk_amount / stop_loss_distance

        return round(position_size, 4)

    def check_risk_limit(self, trade_value):

        return trade_value <= (
            self.balance * self.max_position_percentage
        )

    def can_open_trade(
        self,
        confidence,
        leverage
    ):

        if confidence < 40:
            return False

        if leverage > 5:
            return False

        if self.daily_loss >= (
            self.balance * self.max_daily_loss
        ):
            return False

        return True

    def update_daily_loss(self, loss_amount):
        self.daily_loss += loss_amount
