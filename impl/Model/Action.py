class Action:
    def __init__(self, action_method, symbol_bought, amount, optional_currency_used=None):
        self.action_method = action_method
        self.symbol_used = symbol_bought
        self.amount = amount
        self.optional_currency_used = optional_currency_used

    def perform(self):
        if self.action_method is None:
            print('Action has no method!')
            return
        self.action_method(self.symbol_used, self.amount, self.optional_currency_used)
