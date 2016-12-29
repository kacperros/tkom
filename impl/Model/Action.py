class Action:
    def __init__(self):
        self.action_method = None
        self.symbol_bought = None
        self.amount = None
        self.optional_currency_used = None

    def perform(self):
        if self.action_method is None:
            return
        self.action_method(self.symbol_bought, self.amount, self.optional_currency_used)
