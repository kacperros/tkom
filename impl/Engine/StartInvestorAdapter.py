from Model.Event import EventType
from Model.StartCondition import StartCondition


class StartInvestorAdapter:
    def __init__(self, investor):
        self.investor = investor

    def add_start_cond(self, start_condition):
        if start_condition.cond_type == EventType.CURRENCY:
            self.__add_currency_cond(start_condition)
        elif start_condition.cond_type == EventType.STOCK:
            self.__add_stock_cond(start_condition)
        else:
            raise ValueError("Event type is not present in system, Sir")

    def __add_currency_cond(self, cond):
        self.investor.add_currency(cond.symbol_id, cond.amount)

    def __add_stock_cond(self, cond):
        self.investor.add_stock(cond.symbol_id, cond.amount)
